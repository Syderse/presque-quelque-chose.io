from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import httpx
import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, utc_now_iso, write_json  # noqa: E402


DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
DEFAULT_KEYWORDS = ROOT / "config" / "keywords.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "hal_latest.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "api.log"
DEFAULT_BASE_URL = "https://api.archives-ouvertes.fr/search/"
DEFAULT_LIMIT = 20
DEFAULT_TIMEOUT_SECONDS = 20
DEFAULT_KEYWORD_LIMIT = 6
DEFAULT_KEYWORD_CATEGORIES = ("radio_core", "radio_free", "podcast")


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


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        compacted = " ".join(str(value).strip().split())
        key = compacted.casefold()
        if compacted and key not in seen:
            deduped.append(compacted)
            seen.add(key)

    return deduped


def _quote_term(term: str) -> str:
    escaped = term.replace('"', '\\"')
    if any(character.isspace() for character in escaped):
        return f'"{escaped}"'

    return escaped


def _select_keywords(
    keywords_config: dict[str, Any],
    *,
    categories: list[str] | tuple[str, ...] = DEFAULT_KEYWORD_CATEGORIES,
    limit: int = DEFAULT_KEYWORD_LIMIT,
) -> list[str]:
    pools = []
    for category in categories:
        values = keywords_config.get(category, [])
        if isinstance(values, list):
            pools.append(_dedupe([str(value) for value in values]))

    selected: list[str] = []
    seen: set[str] = set()
    index = 0
    while len(selected) < limit:
        progressed = False
        for pool in pools:
            if index >= len(pool):
                continue

            keyword = pool[index]
            key = keyword.casefold()
            if key not in seen:
                selected.append(keyword)
                seen.add(key)
                if len(selected) >= limit:
                    break
            progressed = True

        if not progressed:
            break
        index += 1

    return selected


def build_query(
    keywords_config: dict[str, Any],
    *,
    categories: list[str] | tuple[str, ...] = DEFAULT_KEYWORD_CATEGORIES,
    keyword_limit: int = DEFAULT_KEYWORD_LIMIT,
) -> str:
    keywords = _select_keywords(keywords_config, categories=categories, limit=keyword_limit)
    if not keywords:
        raise ValueError("No HAL keywords available")

    return "(" + " OR ".join(_quote_term(keyword) for keyword in keywords) + ")"


def _field_list(fields: Any) -> str | None:
    if not isinstance(fields, list):
        return None

    selected = [str(field).strip() for field in fields if str(field).strip()]
    return ",".join(selected) if selected else None


def _filter_queries(filters: Any) -> list[str]:
    if not isinstance(filters, dict):
        return []

    queries: list[str] = []
    languages = filters.get("language")
    if isinstance(languages, list):
        values = [str(language).strip() for language in languages if str(language).strip()]
        if values:
            queries.append("language_s:(" + " OR ".join(values) + ")")

    return queries


def build_params(hal_config: dict[str, Any], keywords_config: dict[str, Any]) -> dict[str, Any]:
    keyword_categories = hal_config.get("keyword_categories", DEFAULT_KEYWORD_CATEGORIES)
    if not isinstance(keyword_categories, list):
        keyword_categories = list(DEFAULT_KEYWORD_CATEGORIES)

    keyword_limit = _as_positive_int(hal_config.get("keyword_limit"), DEFAULT_KEYWORD_LIMIT)
    params: dict[str, Any] = {
        "q": build_query(
            keywords_config,
            categories=keyword_categories,
            keyword_limit=keyword_limit,
        ),
        "rows": _as_positive_int(hal_config.get("limit"), DEFAULT_LIMIT),
        "wt": "json",
    }

    fields = _field_list(hal_config.get("fields"))
    if fields:
        params["fl"] = fields

    sort = hal_config.get("sort")
    if isinstance(sort, str) and sort.strip():
        params["sort"] = sort.strip()

    filter_queries = _filter_queries(hal_config.get("filters"))
    if filter_queries:
        params["fq"] = filter_queries

    return params


def fetch_hal(
    base_url: str,
    params: dict[str, Any],
    *,
    timeout: int | float = DEFAULT_TIMEOUT_SECONDS,
    client: httpx.Client | None = None,
) -> httpx.Response:
    if client is not None:
        response = client.get(base_url, params=params)
        response.raise_for_status()
        return response

    with httpx.Client(timeout=timeout) as owned_client:
        response = owned_client.get(base_url, params=params)
        response.raise_for_status()
        return response


def parse_response(response_or_payload: httpx.Response | dict[str, Any]) -> dict[str, Any]:
    if isinstance(response_or_payload, httpx.Response):
        payload = response_or_payload.json()
    else:
        payload = response_or_payload

    if not isinstance(payload, dict):
        raise ValueError("HAL response is not a JSON object")

    response = payload.get("response")
    if not isinstance(response, dict):
        raise ValueError("HAL response has no response object")

    docs = response.get("docs")
    if not isinstance(docs, list):
        raise ValueError("HAL response has no docs list")

    return {
        "num_found": response.get("numFound"),
        "start": response.get("start"),
        "docs": docs,
        "raw": payload,
    }


def _error_payload(
    *,
    config_path: str | Path,
    keywords_path: str | Path,
    source_name: str,
    source_api: str,
    query: str | None,
    limit: int,
    error_type: str,
    message: str,
) -> dict[str, Any]:
    return {
        "connector": "hal",
        "generated_at": utc_now_iso(),
        "config": str(config_path),
        "keywords": str(keywords_path),
        "source_name": source_name,
        "source_api": source_api,
        "query": query,
        "limit": limit,
        "result_count": 0,
        "num_found": None,
        "docs": [],
        "raw": None,
        "errors": [{"type": error_type, "message": message}],
    }


def ingest_hal(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    keywords_path: str | Path = DEFAULT_KEYWORDS,
    output_path: str | Path = DEFAULT_OUTPUT,
    log_path: str | Path = DEFAULT_LOG,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    source_config = load_yaml(config_path)
    keywords_config = load_yaml(keywords_path)
    hal_config = source_config.get("hal") if isinstance(source_config.get("hal"), dict) else {}

    source_name = str(hal_config.get("name") or "HAL")
    source_api = str(hal_config.get("base_url") or DEFAULT_BASE_URL)
    query: str | None = None
    limit = _as_positive_int(hal_config.get("limit"), DEFAULT_LIMIT)

    if hal_config.get("enabled") is not True:
        payload = _error_payload(
            config_path=config_path,
            keywords_path=keywords_path,
            source_name=source_name,
            source_api=source_api,
            query=None,
            limit=limit,
            error_type="disabled",
            message="HAL source is disabled",
        )
        write_json(output_path, payload)
        return payload

    try:
        params = build_params(hal_config, keywords_config)
        query = str(params["q"])
        limit = int(params["rows"])
        response = fetch_hal(source_api, params, timeout=DEFAULT_TIMEOUT_SECONDS, client=client)
        parsed = parse_response(response)

        payload = {
            "connector": "hal",
            "generated_at": utc_now_iso(),
            "config": str(config_path),
            "keywords": str(keywords_path),
            "source_name": source_name,
            "source_api": source_api,
            "query": query,
            "limit": limit,
            "result_count": len(parsed["docs"]),
            "num_found": parsed["num_found"],
            "start": parsed["start"],
            "docs": parsed["docs"],
            "raw": parsed["raw"],
            "errors": [],
        }
    except httpx.TimeoutException as exc:
        message = f"HAL request timed out: {exc}"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            keywords_path=keywords_path,
            source_name=source_name,
            source_api=source_api,
            query=query,
            limit=limit,
            error_type="timeout",
            message=str(exc),
        )
    except httpx.HTTPStatusError as exc:
        message = f"HAL HTTP error {exc.response.status_code}: {exc}"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            keywords_path=keywords_path,
            source_name=source_name,
            source_api=source_api,
            query=query,
            limit=limit,
            error_type="http",
            message=str(exc),
        )
    except httpx.RequestError as exc:
        message = f"HAL request failed: {exc}"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            keywords_path=keywords_path,
            source_name=source_name,
            source_api=source_api,
            query=query,
            limit=limit,
            error_type="request",
            message=str(exc),
        )
    except (ValueError, TypeError) as exc:
        message = f"HAL unexpected response: {exc}"
        append_log(log_path, message, level="ERROR")
        payload = _error_payload(
            config_path=config_path,
            keywords_path=keywords_path,
            source_name=source_name,
            source_api=source_api,
            query=query,
            limit=limit,
            error_type="unexpected_response",
            message=str(exc),
        )

    write_json(output_path, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest HAL search results into a raw JSON dump.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to sources.yaml.")
    parser.add_argument("--keywords", default=str(DEFAULT_KEYWORDS), help="Path to keywords.yaml.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to the raw HAL JSON dump.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = ingest_hal(config_path=args.config, keywords_path=args.keywords, output_path=args.output)
    print(f"Wrote {payload['result_count']} HAL docs to {args.output}")


if __name__ == "__main__":
    main()
