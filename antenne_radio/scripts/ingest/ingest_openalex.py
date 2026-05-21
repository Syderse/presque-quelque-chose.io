from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, utc_now_iso, write_json  # noqa: E402


DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "openalex_latest.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "api.log"
DEFAULT_BASE_URL = "https://api.openalex.org"
DEFAULT_ENDPOINT = "/works"
DEFAULT_PER_PAGE = 20
DEFAULT_MAX_PAGES_PER_PROFILE = 1
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_DELAY_SECONDS = 1.0
DEFAULT_WINDOW_MONTHS = 18
DEFAULT_SORT = "relevance_score:desc"
DEFAULT_USER_AGENT = "radio-watch/0.1 (https://presque-quelque-chose.io)"
SECRET_QUERY_RE = re.compile(r"([?&](?:mailto|api_key)=)[^&\s'\"]+")


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML mapping: {path}")

    return data


def _as_positive_int(value: Any, default: int, *, maximum: int | None = None) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default

    if parsed <= 0:
        parsed = default

    if maximum is not None:
        return min(parsed, maximum)

    return parsed


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


def _safe_error_message(value: Any) -> str:
    return SECRET_QUERY_RE.sub(r"\1<redacted>", str(value))


def _selected_profiles(openalex_config: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = openalex_config.get("profiles", [])
    if not isinstance(profiles, list):
        return []

    selected: list[dict[str, Any]] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        if profile.get("enabled") is False:
            continue
        if _compact_text(profile.get("search")):
            selected.append(profile)

    return selected


def _contact_mailto(openalex_config: dict[str, Any]) -> str | None:
    configured = _compact_text(openalex_config.get("mailto"))
    if configured:
        return configured

    env_name = _compact_text(openalex_config.get("mailto_env"))
    if env_name:
        return _compact_text(os.getenv(env_name))

    return None


def _api_key(openalex_config: dict[str, Any]) -> str | None:
    configured = _compact_text(openalex_config.get("api_key"))
    if configured:
        return configured

    env_name = _compact_text(openalex_config.get("api_key_env"))
    if env_name:
        return _compact_text(os.getenv(env_name))

    return None


def _subtract_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 - months
    year = month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, _days_in_month(year, month))
    return date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    if month == 2:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return 29
        return 28

    return 30 if month in {4, 6, 9, 11} else 31


def _window_start(openalex_config: dict[str, Any], *, today: date | None = None) -> str:
    months = _as_positive_int(openalex_config.get("window_months"), DEFAULT_WINDOW_MONTHS)
    reference = today or datetime.now(timezone.utc).date()
    return _subtract_months(reference, months).isoformat()


def _quote_search_term(term: str) -> str:
    escaped = term.replace('"', '\\"')
    if any(character.isspace() for character in escaped):
        return f'"{escaped}"'

    return escaped


def _search_with_exclusions(openalex_config: dict[str, Any], profile: dict[str, Any]) -> str:
    search = _compact_text(profile.get("search"))
    if search is None:
        raise ValueError("OpenAlex profile has no search query")

    exclusions = openalex_config.get("noise_exclusions", [])
    if not isinstance(exclusions, list):
        return search

    negative_terms = [_quote_search_term(term) for term in (_compact_text(item) for item in exclusions) if term]
    if not negative_terms:
        return search

    return f"({search}) NOT (" + " OR ".join(negative_terms) + ")"


def _filter_parts(openalex_config: dict[str, Any], *, today: date | None = None) -> list[str]:
    filters = openalex_config.get("filters", {})
    filters = filters if isinstance(filters, dict) else {}

    parts: list[str] = [f"from_publication_date:{_window_start(openalex_config, today=today)}"]

    source_type = _compact_text(filters.get("type"))
    if source_type:
        parts.append(f"type:{source_type}")

    languages = filters.get("language")
    if isinstance(languages, list):
        values = [_compact_text(language) for language in languages]
        compacted = [value for value in values if value]
        if compacted:
            parts.append("language:" + "|".join(compacted))

    for key in ("is_retracted", "is_paratext"):
        if key in filters:
            value = str(filters[key]).lower()
            if value in {"true", "false"}:
                parts.append(f"{key}:{value}")

    return parts


def _select_fields(openalex_config: dict[str, Any]) -> str | None:
    fields = openalex_config.get("select", [])
    forbidden = openalex_config.get("forbidden_select", [])
    if not isinstance(fields, list):
        return None

    forbidden_set = {str(field).strip() for field in forbidden if str(field).strip()} if isinstance(forbidden, list) else set()
    selected: list[str] = []
    seen: set[str] = set()
    for field in fields:
        field_text = _compact_text(field)
        if field_text is None or field_text in forbidden_set or field_text in seen:
            continue
        selected.append(field_text)
        seen.add(field_text)

    return ",".join(selected) if selected else None


def build_params(
    openalex_config: dict[str, Any],
    profile: dict[str, Any],
    *,
    mailto: str,
    api_key: str | None = None,
    page: int = 1,
    today: date | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "search": _search_with_exclusions(openalex_config, profile),
        "filter": ",".join(_filter_parts(openalex_config, today=today)),
        "per_page": _as_positive_int(openalex_config.get("per_page"), DEFAULT_PER_PAGE, maximum=100),
        "page": _as_positive_int(page, 1),
        "mailto": mailto,
    }

    sort = _compact_text(openalex_config.get("sort")) or DEFAULT_SORT
    if sort:
        params["sort"] = sort

    select = _select_fields(openalex_config)
    if select:
        params["select"] = select

    if api_key:
        params["api_key"] = api_key

    return params


def works_endpoint(base_url: str, endpoint: str = DEFAULT_ENDPOINT) -> str:
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


def fetch_openalex(
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
        raise ValueError("OpenAlex response is not a JSON object")

    results = payload.get("results")
    if not isinstance(results, list):
        raise ValueError("OpenAlex response has no results list")

    meta = payload.get("meta", {})
    if meta is not None and not isinstance(meta, dict):
        raise ValueError("OpenAlex response meta is not a JSON object")

    return {
        "meta": meta or {},
        "items": results,
        "raw": payload,
    }


def _error_entry(
    *,
    error_type: str,
    message: str,
    profile_id: str | None = None,
    profile_label: str | None = None,
    status_code: int | None = None,
) -> dict[str, Any]:
    error: dict[str, Any] = {"type": error_type, "message": message}
    if profile_id:
        error["profile_id"] = profile_id
    if profile_label:
        error["profile_label"] = profile_label
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
    openalex_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "connector": "openalex",
        "generated_at": utc_now_iso(),
        "config": str(config_path),
        "source_name": source_name,
        "source_api": source_api,
        "result_count": 0,
        "items": [],
        "profiles": [],
        "raw_responses": [],
        "errors": [_error_entry(error_type=error_type, message=message)],
    }
    if openalex_config is not None:
        payload["mailto_env"] = openalex_config.get("mailto_env")
        payload["api_key_env"] = openalex_config.get("api_key_env")
        payload["per_page"] = _as_positive_int(openalex_config.get("per_page"), DEFAULT_PER_PAGE, maximum=100)
        payload["max_pages_per_profile"] = _as_positive_int(
            openalex_config.get("max_pages_per_profile"),
            DEFAULT_MAX_PAGES_PER_PROFILE,
            maximum=10,
        )

    return payload


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
    profile: dict[str, Any],
    endpoint: str,
) -> dict[str, Any]:
    enriched = dict(item)
    enriched["_openalex_source"] = {
        "profile_id": _compact_text(profile.get("id")),
        "profile_label": _compact_text(profile.get("label")),
        "endpoint": endpoint,
    }
    return enriched


def ingest_openalex(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    output_path: str | Path = DEFAULT_OUTPUT,
    log_path: str | Path = DEFAULT_LOG,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    source_config = load_yaml(config_path)
    openalex_config = source_config.get("openalex") if isinstance(source_config.get("openalex"), dict) else {}

    source_name = str(openalex_config.get("name") or "OpenAlex")
    source_api = str(openalex_config.get("base_url") or DEFAULT_BASE_URL)

    if openalex_config.get("enabled") is not True:
        payload = _error_payload(
            config_path=config_path,
            source_name=source_name,
            source_api=source_api,
            error_type="disabled",
            message="OpenAlex source is disabled",
            openalex_config=openalex_config,
        )
        write_json(output_path, payload)
        return payload

    mailto = _contact_mailto(openalex_config)
    if mailto is None:
        message = "OpenAlex requires a mailto value or a configured mailto_env environment variable"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            source_name=source_name,
            source_api=source_api,
            error_type="missing_mailto",
            message=message,
            openalex_config=openalex_config,
        )
        write_json(output_path, payload)
        return payload

    api_key = _api_key(openalex_config)
    profiles = _selected_profiles(openalex_config)
    endpoint = works_endpoint(source_api, str(openalex_config.get("endpoint") or DEFAULT_ENDPOINT))
    user_agent = str(openalex_config.get("user_agent") or DEFAULT_USER_AGENT)
    timeout = _as_positive_int(openalex_config.get("timeout_seconds"), DEFAULT_TIMEOUT_SECONDS)
    delay = _as_non_negative_float(openalex_config.get("polite_delay_seconds"), DEFAULT_DELAY_SECONDS)
    max_pages = _as_positive_int(
        openalex_config.get("max_pages_per_profile"),
        DEFAULT_MAX_PAGES_PER_PROFILE,
        maximum=10,
    )
    per_page = _as_positive_int(openalex_config.get("per_page"), DEFAULT_PER_PAGE, maximum=100)

    items: list[dict[str, Any]] = []
    profile_results: list[dict[str, Any]] = []
    raw_responses: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    request_count = 0

    for profile in profiles:
        profile_id = _compact_text(profile.get("id"))
        profile_label = _compact_text(profile.get("label")) or profile_id or "OpenAlex profile"
        profile_items: list[dict[str, Any]] = []
        profile_errors: list[dict[str, Any]] = []
        profile_meta: dict[str, Any] | None = None

        for page in range(1, max_pages + 1):
            if request_count > 0 and delay:
                time.sleep(delay)

            params = build_params(openalex_config, profile, mailto=mailto, api_key=api_key, page=page)
            request_count += 1

            try:
                response = fetch_openalex(endpoint, params, user_agent=user_agent, timeout=timeout, client=client)
                parsed = parse_response(response)
                profile_meta = parsed["meta"]
                source_items = [
                    _item_with_source_metadata(item, profile=profile, endpoint=endpoint)
                    for item in parsed["items"]
                    if isinstance(item, dict)
                ]
                profile_items.extend(source_items)
                raw_responses.append(
                    {
                        "profile_id": profile_id,
                        "profile_label": profile_label,
                        "page": page,
                        "raw": parsed["raw"],
                    }
                )
                if len(source_items) < per_page:
                    break
            except httpx.TimeoutException as exc:
                error_message = _safe_error_message(exc)
                message = f"OpenAlex request timed out for {profile_label}: {error_message}"
                append_log(log_path, message, level="ERROR")
                error = _error_entry(
                    error_type="timeout",
                    message=error_message,
                    profile_id=profile_id,
                    profile_label=profile_label,
                )
                errors.append(error)
                profile_errors.append(error)
                break
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                error_type = _status_error_type(status_code)
                error_message = _safe_error_message(exc)
                message = f"OpenAlex HTTP error {status_code} for {profile_label}: {error_message}"
                append_log(log_path, message, level="ERROR")
                error = _error_entry(
                    error_type=error_type,
                    message=error_message,
                    profile_id=profile_id,
                    profile_label=profile_label,
                    status_code=status_code,
                )
                errors.append(error)
                profile_errors.append(error)
                break
            except httpx.RequestError as exc:
                error_message = _safe_error_message(exc)
                message = f"OpenAlex request failed for {profile_label}: {error_message}"
                append_log(log_path, message, level="ERROR")
                error = _error_entry(
                    error_type="request",
                    message=error_message,
                    profile_id=profile_id,
                    profile_label=profile_label,
                )
                errors.append(error)
                profile_errors.append(error)
                break
            except (ValueError, TypeError) as exc:
                message = f"OpenAlex unexpected response for {profile_label}: {exc}"
                append_log(log_path, message, level="ERROR")
                error = _error_entry(
                    error_type="unexpected_response",
                    message=str(exc),
                    profile_id=profile_id,
                    profile_label=profile_label,
                )
                errors.append(error)
                profile_errors.append(error)
                break

        if not profile_items and not profile_errors:
            error = _error_entry(
                error_type="empty_response",
                message="OpenAlex returned no items",
                profile_id=profile_id,
                profile_label=profile_label,
            )
            append_log(log_path, f"OpenAlex returned no items for {profile_label}", level="ERROR")
            errors.append(error)
            profile_errors.append(error)

        items.extend(profile_items)
        profile_results.append(
            {
                "profile_id": profile_id,
                "profile_label": profile_label,
                "result_count": len(profile_items),
                "meta": profile_meta,
                "errors": profile_errors,
            }
        )

    payload = {
        "connector": "openalex",
        "generated_at": utc_now_iso(),
        "config": str(config_path),
        "source_name": source_name,
        "source_api": source_api,
        "endpoint": endpoint,
        "mailto_env": openalex_config.get("mailto_env"),
        "api_key_env": openalex_config.get("api_key_env"),
        "per_page": per_page,
        "max_pages_per_profile": max_pages,
        "request_count": request_count,
        "result_count": len(items),
        "items": items,
        "profiles": profile_results,
        "raw_responses": raw_responses,
        "errors": errors,
    }
    write_json(output_path, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest OpenAlex Works into a raw JSON dump.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to sources.yaml.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to the raw OpenAlex JSON dump.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = ingest_openalex(config_path=args.config, output_path=args.output)
    print(f"Wrote {payload['result_count']} OpenAlex items to {args.output}")


if __name__ == "__main__":
    main()
