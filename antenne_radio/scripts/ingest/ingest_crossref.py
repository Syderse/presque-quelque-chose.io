from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx
import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, utc_now_iso, write_json  # noqa: E402


DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "crossref_latest.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "api.log"
DEFAULT_BASE_URL = "https://api.crossref.org"
DEFAULT_ROWS = 20
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_DELAY_SECONDS = 1.0
DEFAULT_USER_AGENT = "radio-watch/0.1 (https://presque-quelque-chose.io)"


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML mapping: {path}")

    return data


def _as_positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    return parsed if parsed > 0 else default


def _as_non_negative_float(value: Any, default: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default

    return parsed if parsed >= 0 else default


def _compact_text(value: Any) -> str | None:
    if value is None:
        return None

    compacted = " ".join(str(value).strip().split())
    return compacted or None


def _error_entry(
    *,
    error_type: str,
    message: str,
    journal_id: str | None = None,
    journal_name: str | None = None,
    issn: str | None = None,
    status_code: int | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {"type": error_type, "message": message}
    if journal_id:
        error["journal_id"] = journal_id
    if journal_name:
        error["journal_name"] = journal_name
    if issn:
        error["issn"] = issn
    if status_code is not None:
        error["status_code"] = status_code
    return error


def _error_payload(
    *,
    config_path: str | Path,
    source_name: str,
    source_api: str,
    error_type: str,
    message: str,
) -> dict[str, Any]:
    return {
        "connector": "crossref",
        "generated_at": utc_now_iso(),
        "config": str(config_path),
        "source_name": source_name,
        "source_api": source_api,
        "result_count": 0,
        "items": [],
        "journals": [],
        "raw_responses": [],
        "errors": [_error_entry(error_type=error_type, message=message)],
    }


def _selected_journals(crossref_config: dict[str, Any]) -> list[dict[str, Any]]:
    journals = crossref_config.get("journals", [])
    if not isinstance(journals, list):
        return []

    return [journal for journal in journals if isinstance(journal, dict) and journal.get("enabled") is True]


def _journal_issns(journal: dict[str, Any]) -> list[str]:
    value = journal.get("issn", journal.get("issns", []))
    values = value if isinstance(value, list) else [value]
    issns: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = _compact_text(item)
        if text and text not in seen:
            issns.append(text)
            seen.add(text)

    return issns


def _mailto(crossref_config: dict[str, Any]) -> str | None:
    configured = _compact_text(crossref_config.get("mailto"))
    if configured:
        return configured

    env_name = _compact_text(crossref_config.get("mailto_env"))
    if env_name:
        return _compact_text(os.getenv(env_name))

    return None


def _filters(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None

    filters: list[str] = []
    for key, item in value.items():
        key_text = _compact_text(key)
        value_text = _compact_text(item)
        if key_text and value_text:
            filters.append(f"{key_text}:{value_text}")

    return ",".join(filters) if filters else None


def build_params(crossref_config: dict[str, Any], *, mailto: str) -> dict[str, Any]:
    params: dict[str, Any] = {
        "rows": _as_positive_int(crossref_config.get("rows"), DEFAULT_ROWS),
        "mailto": mailto,
    }

    sort = _compact_text(crossref_config.get("sort"))
    if sort:
        params["sort"] = sort

    order = _compact_text(crossref_config.get("order"))
    if order:
        params["order"] = order

    filters = _filters(crossref_config.get("filters"))
    if filters:
        params["filter"] = filters

    return params


def journal_endpoint(base_url: str, issn: str) -> str:
    return f"{base_url.rstrip('/')}/journals/{issn}/works"


def fetch_crossref(
    endpoint: str,
    params: dict[str, Any],
    *,
    user_agent: str = DEFAULT_USER_AGENT,
    timeout: int | float = DEFAULT_TIMEOUT_SECONDS,
    client: httpx.Client | None = None,
) -> httpx.Response:
    headers = {"User-Agent": user_agent}
    if client is not None:
        response = client.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response

    with httpx.Client(timeout=timeout, headers=headers) as owned_client:
        response = owned_client.get(endpoint, params=params)
        response.raise_for_status()
        return response


def parse_response(response_or_payload: httpx.Response | dict[str, Any]) -> dict[str, Any]:
    if isinstance(response_or_payload, httpx.Response):
        payload = response_or_payload.json()
    else:
        payload = response_or_payload

    if not isinstance(payload, dict):
        raise ValueError("Crossref response is not a JSON object")

    message = payload.get("message")
    if not isinstance(message, dict):
        raise ValueError("Crossref response has no message object")

    items = message.get("items")
    if not isinstance(items, list):
        raise ValueError("Crossref response has no items list")

    return {
        "total_results": message.get("total-results"),
        "items": items,
        "raw": payload,
    }


def _status_error_type(status_code: int) -> str:
    if status_code == 403:
        return "forbidden"
    if status_code == 429:
        return "rate_limited"
    if status_code >= 500:
        return "server_error"
    return "http"


def _item_with_source_metadata(
    item: dict[str, Any],
    *,
    journal: dict[str, Any],
    issn: str,
    endpoint: str,
) -> dict[str, Any]:
    enriched = dict(item)
    enriched["_crossref_source"] = {
        "journal_id": _compact_text(journal.get("id")),
        "journal_name": _compact_text(journal.get("name")),
        "issn": issn,
        "endpoint": endpoint,
    }
    return enriched


def ingest_crossref(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    output_path: str | Path = DEFAULT_OUTPUT,
    log_path: str | Path = DEFAULT_LOG,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    source_config = load_yaml(config_path)
    crossref_config = source_config.get("crossref") if isinstance(source_config.get("crossref"), dict) else {}

    source_name = str(crossref_config.get("name") or "Crossref")
    source_api = str(crossref_config.get("base_url") or DEFAULT_BASE_URL)

    if crossref_config.get("enabled") is not True:
        payload = _error_payload(
            config_path=config_path,
            source_name=source_name,
            source_api=source_api,
            error_type="disabled",
            message="Crossref source is disabled",
        )
        write_json(output_path, payload)
        return payload

    mailto = _mailto(crossref_config)
    if mailto is None:
        message = "Crossref requires a mailto value or a configured mailto_env environment variable"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            source_name=source_name,
            source_api=source_api,
            error_type="missing_mailto",
            message=message,
        )
        write_json(output_path, payload)
        return payload

    journals = _selected_journals(crossref_config)
    params = build_params(crossref_config, mailto=mailto)
    user_agent = str(crossref_config.get("user_agent") or DEFAULT_USER_AGENT)
    timeout = _as_positive_int(crossref_config.get("timeout_seconds"), DEFAULT_TIMEOUT_SECONDS)
    delay = _as_non_negative_float(crossref_config.get("polite_delay_seconds"), DEFAULT_DELAY_SECONDS)

    items: list[dict[str, Any]] = []
    journal_results: list[dict[str, Any]] = []
    raw_responses: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for index, journal in enumerate(journals):
        journal_id = _compact_text(journal.get("id"))
        journal_name = _compact_text(journal.get("name")) or journal_id or "Crossref journal"
        issns = _journal_issns(journal)
        primary_issn = issns[0] if issns else None

        if not primary_issn:
            error = _error_entry(
                error_type="missing_issn",
                message="Crossref journal has no ISSN",
                journal_id=journal_id,
                journal_name=journal_name,
            )
            append_log(log_path, f"Crossref journal {journal_name} has no ISSN", level="ERROR")
            errors.append(error)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": None,
                    "result_count": 0,
                    "errors": [error],
                }
            )
            continue

        if index > 0 and delay:
            time.sleep(delay)

        endpoint = journal_endpoint(source_api, primary_issn)
        try:
            response = fetch_crossref(endpoint, params, user_agent=user_agent, timeout=timeout, client=client)
            parsed = parse_response(response)
            source_items = [
                _item_with_source_metadata(item, journal=journal, issn=primary_issn, endpoint=endpoint)
                for item in parsed["items"]
                if isinstance(item, dict)
            ]
            journal_errors: list[dict[str, Any]] = []
            if not source_items:
                error = _error_entry(
                    error_type="empty_response",
                    message="Crossref returned no items",
                    journal_id=journal_id,
                    journal_name=journal_name,
                    issn=primary_issn,
                )
                append_log(log_path, f"Crossref returned no items for {journal_name}", level="ERROR")
                errors.append(error)
                journal_errors.append(error)

            items.extend(source_items)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "issns": issns,
                    "endpoint": endpoint,
                    "result_count": len(source_items),
                    "total_results": parsed["total_results"],
                    "errors": journal_errors,
                }
            )
            raw_responses.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "raw": parsed["raw"],
                }
            )
        except httpx.TimeoutException as exc:
            message = f"Crossref request timed out for {journal_name}: {exc}"
            append_log(log_path, message, level="ERROR")
            error = _error_entry(
                error_type="timeout",
                message=str(exc),
                journal_id=journal_id,
                journal_name=journal_name,
                issn=primary_issn,
            )
            errors.append(error)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "endpoint": endpoint,
                    "result_count": 0,
                    "errors": [error],
                }
            )
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            error_type = _status_error_type(status_code)
            message = f"Crossref HTTP error {status_code} for {journal_name}: {exc}"
            append_log(log_path, message, level="ERROR")
            error = _error_entry(
                error_type=error_type,
                message=str(exc),
                journal_id=journal_id,
                journal_name=journal_name,
                issn=primary_issn,
                status_code=status_code,
            )
            errors.append(error)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "endpoint": endpoint,
                    "result_count": 0,
                    "errors": [error],
                }
            )
        except httpx.RequestError as exc:
            message = f"Crossref request failed for {journal_name}: {exc}"
            append_log(log_path, message, level="ERROR")
            error = _error_entry(
                error_type="request",
                message=str(exc),
                journal_id=journal_id,
                journal_name=journal_name,
                issn=primary_issn,
            )
            errors.append(error)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "endpoint": endpoint,
                    "result_count": 0,
                    "errors": [error],
                }
            )
        except (ValueError, TypeError) as exc:
            message = f"Crossref unexpected response for {journal_name}: {exc}"
            append_log(log_path, message, level="ERROR")
            error = _error_entry(
                error_type="unexpected_response",
                message=str(exc),
                journal_id=journal_id,
                journal_name=journal_name,
                issn=primary_issn,
            )
            errors.append(error)
            journal_results.append(
                {
                    "journal_id": journal_id,
                    "journal_name": journal_name,
                    "issn": primary_issn,
                    "endpoint": endpoint,
                    "result_count": 0,
                    "errors": [error],
                }
            )

    payload = {
        "connector": "crossref",
        "generated_at": utc_now_iso(),
        "config": str(config_path),
        "source_name": source_name,
        "source_api": source_api,
        "mailto_env": crossref_config.get("mailto_env"),
        "rows": params["rows"],
        "result_count": len(items),
        "items": items,
        "journals": journal_results,
        "raw_responses": raw_responses,
        "errors": errors,
    }
    write_json(output_path, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Crossref journal works into a raw JSON dump.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to sources.yaml.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to the raw Crossref JSON dump.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = ingest_crossref(config_path=args.config, output_path=args.output)
    print(f"Wrote {payload['result_count']} Crossref items to {args.output}")


if __name__ == "__main__":
    main()
