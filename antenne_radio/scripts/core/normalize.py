from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dateutil import parser as date_parser
from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, read_json, utc_now_iso, write_json  # noqa: E402
from scripts.core.models import (  # noqa: E402
    RadioWatchItem,
    SourceType,
    WatchStatus,
    generate_stable_id,
    normalize_doi,
    normalize_url,
)


DEFAULT_RSS_RAW = ROOT / "data" / "raw" / "rss_latest.json"
DEFAULT_HAL_RAW = ROOT / "data" / "raw" / "hal_latest.json"
DEFAULT_CROSSREF_RAW = ROOT / "data" / "raw" / "crossref_latest.json"
DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "api.log"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _compact_text(value: Any) -> str | None:
    if value is None:
        return None

    compacted = " ".join(str(value).strip().split())
    return compacted or None


def _first_text(value: Any) -> str | None:
    if isinstance(value, list):
        for item in value:
            text = _compact_text(item)
            if text:
                return text
        return None

    return _compact_text(value)


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []

    values = value if isinstance(value, list) else [value]
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = _compact_text(item)
        key = text.casefold() if text else None
        if text and key not in seen:
            deduped.append(text)
            seen.add(key)

    return deduped


def _parse_datetime(value: Any) -> datetime | None:
    text = _first_text(value)
    if text is None:
        return None

    try:
        parsed = date_parser.parse(text)
    except (TypeError, ValueError, OverflowError):
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def _year_datetime(value: Any) -> datetime | None:
    if value is None:
        return None

    try:
        year = int(value)
    except (TypeError, ValueError):
        return None

    if year < 1:
        return None

    return datetime(year, 1, 1, tzinfo=timezone.utc)


def _date_parts_datetime(value: Any) -> datetime | None:
    if not isinstance(value, dict):
        return None

    date_parts = value.get("date-parts")
    if not isinstance(date_parts, list) or not date_parts:
        return None

    first_parts = date_parts[0]
    if not isinstance(first_parts, list) or not first_parts:
        return None

    try:
        year = int(first_parts[0])
        month = int(first_parts[1]) if len(first_parts) > 1 else 1
        day = int(first_parts[2]) if len(first_parts) > 2 else 1
    except (TypeError, ValueError):
        return None

    try:
        return datetime(year, month, day, tzinfo=timezone.utc)
    except ValueError:
        return None


def _item_to_dict(item: RadioWatchItem) -> dict[str, Any]:
    return item.model_dump(mode="json")


def _sort_key(indexed_item: tuple[int, RadioWatchItem]) -> tuple[str, int]:
    index, item = indexed_item
    sort_date = item.published_at or item.discovered_at
    return (sort_date.isoformat(), -index)


def sort_items(items: list[RadioWatchItem]) -> list[RadioWatchItem]:
    indexed = list(enumerate(items))
    return [item for _, item in sorted(indexed, key=_sort_key, reverse=True)]


def normalize_rss_entry(
    entry: dict[str, Any],
    *,
    discovered_at: datetime | None = None,
) -> RadioWatchItem:
    published_at = _parse_datetime(entry.get("published")) or _parse_datetime(entry.get("updated"))
    title = _first_text(entry.get("title"))
    url = _first_text(entry.get("link"))
    doi = normalize_doi(_first_text(entry.get("doi")) or _first_text(entry.get("dc_identifier")) or url)
    source_name = _first_text(entry.get("source_name")) or "RSS"
    item_id = generate_stable_id(
        doi=doi,
        url=url,
        title=title,
        published_at=published_at,
        source_name=source_name,
    )

    return RadioWatchItem(
        id=item_id,
        title=title or "",
        source_name=source_name,
        source_type=SourceType.blog,
        language="und",
        status=WatchStatus.new,
        discovered_at=discovered_at or _now(),
        authors=_text_list(entry.get("authors")),
        published_at=published_at,
        url=url,
        doi=doi,
        abstract=_first_text(entry.get("summary")),
        source_feed=_first_text(entry.get("source_feed")),
        source_api="rss",
        raw=entry.get("raw") if isinstance(entry.get("raw"), dict) else entry,
    )


def normalize_hal_entry(
    entry: dict[str, Any],
    *,
    source_name: str = "HAL",
    source_api: str = "hal",
    discovered_at: datetime | None = None,
) -> RadioWatchItem:
    title = _first_text(entry.get("title_s"))
    url = _first_text(entry.get("uri_s"))
    doi = normalize_doi(_first_text(entry.get("doiId_s")) or _first_text(entry.get("doi_s")))
    published_at = _parse_datetime(entry.get("producedDate_tdate")) or _year_datetime(entry.get("producedDateY_i"))
    item_id = generate_stable_id(
        doi=doi,
        url=url,
        title=title,
        published_at=published_at,
        source_name=source_name,
    )

    return RadioWatchItem(
        id=item_id,
        title=title or "",
        source_name=source_name,
        source_type=SourceType.journal_article,
        language=_first_text(entry.get("language_s")) or "und",
        status=WatchStatus.new,
        discovered_at=discovered_at or _now(),
        title_original=_first_text(entry.get("title_s")),
        authors=_text_list(entry.get("authorFullName_s")),
        published_at=published_at,
        url=url,
        doi=doi,
        abstract=_first_text(entry.get("abstract_s")),
        tags=_text_list(entry.get("keyword_s")),
        source_api=source_api,
        raw=entry,
    )


def _crossref_date(entry: dict[str, Any]) -> datetime | None:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        parsed = _date_parts_datetime(entry.get(key))
        if parsed is not None:
            return parsed

    created = entry.get("created")
    if isinstance(created, dict):
        parsed = _parse_datetime(created.get("date-time")) or _parse_datetime(created.get("timestamp"))
        if parsed is not None:
            return parsed

    return None


def _crossref_authors(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    authors: list[str] = []
    seen: set[str] = set()
    for author in value:
        if not isinstance(author, dict):
            continue

        given = _compact_text(author.get("given"))
        family = _compact_text(author.get("family"))
        literal = _compact_text(author.get("name")) or _compact_text(author.get("literal"))
        name = " ".join(part for part in (given, family) if part) or literal
        key = name.casefold() if name else None
        if name and key not in seen:
            authors.append(name)
            seen.add(key)

    return authors


def normalize_crossref_entry(
    entry: dict[str, Any],
    *,
    discovered_at: datetime | None = None,
) -> RadioWatchItem:
    source = entry.get("_crossref_source") if isinstance(entry.get("_crossref_source"), dict) else {}
    title = _first_text(entry.get("title"))
    doi = normalize_doi(_first_text(entry.get("DOI")))
    url = _first_text(entry.get("URL"))
    published_at = _crossref_date(entry)
    source_name = _first_text(entry.get("container-title")) or _first_text(source.get("journal_name")) or "Crossref"
    item_id = generate_stable_id(
        doi=doi,
        url=url,
        title=title,
        published_at=published_at,
        source_name=source_name,
    )

    return RadioWatchItem(
        id=item_id,
        title=title or "",
        source_name=source_name,
        source_type=SourceType.journal_article,
        language=_first_text(entry.get("language")) or "und",
        status=WatchStatus.new,
        discovered_at=discovered_at or _now(),
        title_original=title,
        authors=_crossref_authors(entry.get("author")),
        published_at=published_at,
        url=url,
        doi=doi,
        abstract=_first_text(entry.get("abstract")),
        tags=_text_list(entry.get("subject")),
        source_feed=_first_text(source.get("endpoint")),
        source_api="crossref",
        raw=entry,
    )


def load_existing_db(path: str | Path = DEFAULT_DB, *, log_path: str | Path = DEFAULT_LOG) -> list[RadioWatchItem]:
    payload = read_json(path, default=[])
    if payload is None:
        return []

    raw_items = payload.get("items", []) if isinstance(payload, dict) else payload
    if not isinstance(raw_items, list):
        append_log(log_path, f"Invalid db format at {path}; expected list or object with items", level="ERROR")
        return []

    items: list[RadioWatchItem] = []
    for raw_item in raw_items:
        try:
            items.append(RadioWatchItem(**raw_item))
        except (TypeError, ValidationError) as exc:
            append_log(log_path, f"Invalid db item skipped: {exc}", level="ERROR")

    return items


TITLE_KEY_RE = re.compile(r"\W+")


def _normalized_title_key(title: str | None) -> str | None:
    text = _compact_text(title)
    if text is None:
        return None

    normalized = TITLE_KEY_RE.sub(" ", text.casefold()).strip()
    return normalized or None


def _identity_keys(item: RadioWatchItem) -> set[str]:
    keys = {f"id:{item.id}"}
    doi = normalize_doi(item.doi) or normalize_doi(item.url)
    normalized_url = normalize_url(item.url)

    if doi:
        keys.add(f"doi:{doi}")
    if normalized_url:
        keys.add(f"url:{normalized_url}")
    if doi is None and normalized_url is None and item.published_at is not None:
        title_key = _normalized_title_key(item.title)
        if title_key:
            keys.add(f"title-date:{title_key}|{item.published_at.date().isoformat()}")

    return keys


def _merge_text_lists(existing_values: list[str], incoming_values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value in [*existing_values, *incoming_values]:
        text = _compact_text(value)
        key = text.casefold() if text else None
        if text and key not in seen:
            merged.append(text)
            seen.add(key)

    return merged


def _merge_raw_metadata(existing: RadioWatchItem, incoming: RadioWatchItem) -> dict[str, Any]:
    if not existing.raw:
        return dict(incoming.raw)
    if not incoming.raw:
        return dict(existing.raw)

    raw = dict(existing.raw)
    merged_sources = raw.get("_merged_sources")
    if not isinstance(merged_sources, list):
        merged_sources = []

    source_metadata = {
        "id": incoming.id,
        "source_name": incoming.source_name,
        "source_api": incoming.source_api,
        "doi": normalize_doi(incoming.doi) or normalize_doi(incoming.url),
        "url": normalize_url(incoming.url),
    }
    if source_metadata not in merged_sources:
        merged_sources.append(source_metadata)

    raw["_merged_sources"] = merged_sources
    return raw


def _merge_duplicate_item(existing: RadioWatchItem, incoming: RadioWatchItem) -> RadioWatchItem:
    incoming_doi = normalize_doi(incoming.doi) or normalize_doi(incoming.url)
    existing_doi = normalize_doi(existing.doi) or normalize_doi(existing.url)

    return existing.model_copy(
        update={
            "id": existing.id,
            "status": existing.status,
            "doi": incoming_doi or existing_doi,
            "url": existing.url or incoming.url,
            "published_at": existing.published_at or incoming.published_at,
            "title_original": existing.title_original or incoming.title_original,
            "language": incoming.language if existing.language == "und" and incoming.language != "und" else existing.language,
            "authors": _merge_text_lists(existing.authors, incoming.authors),
            "abstract": existing.abstract or incoming.abstract,
            "tags": _merge_text_lists(existing.tags, incoming.tags),
            "keywords_matched": existing.keywords_matched,
            "negative_keywords_matched": existing.negative_keywords_matched,
            "relevance_score": existing.relevance_score,
            "score_explanation": existing.score_explanation,
            "source_feed": existing.source_feed or incoming.source_feed,
            "source_api": existing.source_api,
            "raw": _merge_raw_metadata(existing, incoming),
        }
    )


def _remember_identity_keys(key_to_index: dict[str, int], item: RadioWatchItem, index: int) -> None:
    for key in _identity_keys(item):
        key_to_index[key] = index


def merge_items_without_duplicates(
    existing_items: list[RadioWatchItem],
    new_items: list[RadioWatchItem],
) -> list[RadioWatchItem]:
    merged: list[RadioWatchItem] = []
    key_to_index: dict[str, int] = {}

    for item in [*existing_items, *new_items]:
        duplicate_index = next((key_to_index[key] for key in _identity_keys(item) if key in key_to_index), None)
        if duplicate_index is None:
            duplicate_index = len(merged)
            merged.append(item)
        else:
            merged[duplicate_index] = _merge_duplicate_item(merged[duplicate_index], item)

        _remember_identity_keys(key_to_index, merged[duplicate_index], duplicate_index)
        _remember_identity_keys(key_to_index, item, duplicate_index)

    return sort_items(merged)


def save_db(path: str | Path = DEFAULT_DB, items: list[RadioWatchItem] | None = None) -> Path:
    return write_json(path, [_item_to_dict(item) for item in sort_items(items or [])])


def _normalize_entries(
    raw_entries: list[dict[str, Any]],
    normalizer: Any,
    *,
    log_path: str | Path,
    label: str,
    **kwargs: Any,
) -> list[RadioWatchItem]:
    items: list[RadioWatchItem] = []
    for index, entry in enumerate(raw_entries):
        try:
            items.append(normalizer(entry, **kwargs))
        except (TypeError, ValidationError, ValueError) as exc:
            append_log(log_path, f"Invalid {label} entry skipped at index {index}: {exc}", level="ERROR")

    return items


def normalize_latest_dumps(
    *,
    rss_raw_path: str | Path = DEFAULT_RSS_RAW,
    hal_raw_path: str | Path = DEFAULT_HAL_RAW,
    crossref_raw_path: str | Path = DEFAULT_CROSSREF_RAW,
    db_path: str | Path = DEFAULT_DB,
    log_path: str | Path = DEFAULT_LOG,
) -> dict[str, Any]:
    existing_items = load_existing_db(db_path, log_path=log_path)
    discovered_at = _now()
    new_items: list[RadioWatchItem] = []

    rss_payload = read_json(rss_raw_path, default={}) or {}
    rss_entries = rss_payload.get("entries", []) if isinstance(rss_payload, dict) else []
    if isinstance(rss_entries, list):
        new_items.extend(
            _normalize_entries(
                rss_entries,
                normalize_rss_entry,
                log_path=log_path,
                label="RSS",
                discovered_at=discovered_at,
            )
        )
    else:
        append_log(log_path, f"Invalid RSS dump at {rss_raw_path}; entries is not a list", level="ERROR")

    hal_payload = read_json(hal_raw_path, default={}) or {}
    hal_entries = hal_payload.get("docs", []) if isinstance(hal_payload, dict) else []
    hal_source_name = _first_text(hal_payload.get("source_name")) if isinstance(hal_payload, dict) else None
    if isinstance(hal_entries, list):
        new_items.extend(
            _normalize_entries(
                hal_entries,
                normalize_hal_entry,
                log_path=log_path,
                label="HAL",
                discovered_at=discovered_at,
                source_name=hal_source_name or "HAL",
                source_api="hal",
            )
        )
    else:
        append_log(log_path, f"Invalid HAL dump at {hal_raw_path}; docs is not a list", level="ERROR")

    crossref_payload = read_json(crossref_raw_path, default={}) or {}
    crossref_entries = crossref_payload.get("items", []) if isinstance(crossref_payload, dict) else []
    if isinstance(crossref_entries, list):
        new_items.extend(
            _normalize_entries(
                crossref_entries,
                normalize_crossref_entry,
                log_path=log_path,
                label="Crossref",
                discovered_at=discovered_at,
            )
        )
    else:
        append_log(log_path, f"Invalid Crossref dump at {crossref_raw_path}; items is not a list", level="ERROR")

    merged_items = merge_items_without_duplicates(existing_items, new_items)
    save_db(db_path, merged_items)

    return {
        "generated_at": utc_now_iso(),
        "existing_count": len(existing_items),
        "normalized_count": len(new_items),
        "saved_count": len(merged_items),
        "added_count": len(merged_items) - len(existing_items),
        "db_path": str(db_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize latest raw RSS/HAL/Crossref dumps into db.json.")
    parser.add_argument("--rss", default=str(DEFAULT_RSS_RAW), help="Path to data/raw/rss_latest.json.")
    parser.add_argument("--hal", default=str(DEFAULT_HAL_RAW), help="Path to data/raw/hal_latest.json.")
    parser.add_argument("--crossref", default=str(DEFAULT_CROSSREF_RAW), help="Path to data/raw/crossref_latest.json.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to data/normalized/db.json.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = normalize_latest_dumps(
        rss_raw_path=args.rss,
        hal_raw_path=args.hal,
        crossref_raw_path=args.crossref,
        db_path=args.db,
    )
    print(f"Saved {result['saved_count']} items to {args.db} ({result['added_count']} added)")


if __name__ == "__main__":
    main()
