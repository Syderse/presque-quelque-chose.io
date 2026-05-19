from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import read_json, utc_now_iso, write_json  # noqa: E402
from scripts.core.models import RadioWatchItem, SourceType, WatchStatus  # noqa: E402


DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_EXPORT_DIR = ROOT / "data" / "exports"
WHITESPACE_RE = re.compile(r"\s+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
EMPTY_ABSTRACT_RE = re.compile(r"^[\s\W_]+$", re.UNICODE)


CSL_TYPE_BY_SOURCE_TYPE = {
    SourceType.journal_article: "article-journal",
    SourceType.book: "book",
    SourceType.chapter: "chapter",
    SourceType.thesis: "thesis",
    SourceType.cfp: "paper-conference",
    SourceType.blog: "webpage",
    SourceType.archive: "webpage",
    SourceType.unknown: "webpage",
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _generated_at_value(generated_at: datetime | str | None = None) -> tuple[datetime, str]:
    if generated_at is None:
        now = _now()
        return now, utc_now_iso()
    if isinstance(generated_at, datetime):
        value = generated_at
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        value = value.astimezone(timezone.utc)
        return value, value.isoformat(timespec="seconds").replace("+00:00", "Z")

    parsed = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc)
    return parsed, parsed.isoformat(timespec="seconds").replace("+00:00", "Z")


def _iso_week(value: datetime) -> str:
    iso_year, iso_week, _ = value.isocalendar()
    return f"{iso_year}-{iso_week:02d}"


def _extract_items_payload(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]

    raise ValueError("db.json must be a list or an object with an items list")


def _load_items(db_path: str | Path) -> list[dict[str, Any]]:
    payload = read_json(db_path, default=[])
    raw_items = _extract_items_payload(payload)
    return [item for item in raw_items if isinstance(item, dict)]


def _valid_items(raw_items: list[dict[str, Any]]) -> list[RadioWatchItem]:
    items: list[RadioWatchItem] = []
    for raw_item in raw_items:
        try:
            items.append(RadioWatchItem(**raw_item))
        except (TypeError, ValidationError):
            continue

    return items


def _sort_items(items: list[RadioWatchItem]) -> list[RadioWatchItem]:
    def sort_key(item: RadioWatchItem) -> tuple[float, str, str]:
        score = item.relevance_score if item.relevance_score is not None else float("-inf")
        date_value = item.published_at or item.discovered_at
        return (score, date_value.isoformat(), item.id)

    return sorted(items, key=sort_key, reverse=True)


def _compact_text(value: str | None) -> str:
    if value is None:
        return ""
    return WHITESPACE_RE.sub(" ", value.strip())


def _plain_text(value: str | None) -> str:
    if value is None:
        return ""

    unescaped = html.unescape(value)
    without_tags = HTML_TAG_RE.sub(" ", unescaped)
    compacted = _compact_text(without_tags)
    if not compacted or EMPTY_ABSTRACT_RE.match(compacted):
        return ""

    return compacted


def _date_parts(value: datetime) -> dict[str, list[list[int]]]:
    return {"date-parts": [[value.year, value.month, value.day]]}


def _author_variables(authors: list[str]) -> list[dict[str, str]]:
    return [{"literal": author} for author in authors if _compact_text(author)]


def _keywords(item: RadioWatchItem) -> str:
    seen: set[str] = set()
    values: list[str] = []
    for keyword in [*item.tags, *item.keywords_matched]:
        compacted = _compact_text(keyword)
        if compacted and compacted not in seen:
            seen.add(compacted)
            values.append(compacted)

    return ", ".join(values)


def _item_to_csl(item: RadioWatchItem) -> dict[str, Any]:
    csl_item: dict[str, Any] = {
        "id": item.id,
        "type": CSL_TYPE_BY_SOURCE_TYPE.get(item.source_type, "webpage"),
        "title": item.title,
        "container-title": item.source_name,
        "issued": _date_parts(item.published_at or item.discovered_at),
        "accessed": _date_parts(item.discovered_at),
    }

    authors = _author_variables(item.authors)
    if authors:
        csl_item["author"] = authors
    if item.url:
        csl_item["URL"] = item.url
    if item.doi:
        csl_item["DOI"] = item.doi
    if item.language and item.language != "und":
        csl_item["language"] = item.language

    abstract = _plain_text(item.abstract)
    if abstract:
        csl_item["abstract"] = abstract

    keywords = _keywords(item)
    if keywords:
        csl_item["keyword"] = keywords

    return csl_item


def _items_for_export(items: list[RadioWatchItem], include_ignored: bool = False) -> list[RadioWatchItem]:
    included_statuses = {WatchStatus.to_read, WatchStatus.candidate}
    if include_ignored:
        included_statuses.add(WatchStatus.ignored)

    return [item for item in items if item.status in included_statuses]


def export_csl_json(
    *,
    db_path: str | Path = DEFAULT_DB,
    export_dir: str | Path = DEFAULT_EXPORT_DIR,
    include_ignored: bool = False,
    generated_at: datetime | str | None = None,
) -> dict[str, Any]:
    generated_dt, generated_at_text = _generated_at_value(generated_at)
    week = _iso_week(generated_dt)
    raw_items = _load_items(db_path)
    items = _valid_items(raw_items)
    exported_items = _items_for_export(items, include_ignored=include_ignored)
    csl_items = [_item_to_csl(item) for item in _sort_items(exported_items)]

    export_path = Path(export_dir) / f"zotero-veille-{week}.csl.json"
    write_json(export_path, csl_items)

    return {
        "generated_at": generated_at_text,
        "week": week,
        "export_path": str(export_path),
        "items_exported": len(csl_items),
        "items_ignored_included": len([item for item in exported_items if item.status is WatchStatus.ignored]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export radio-watch items to a manual Zotero CSL JSON file.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to data/normalized/db.json.")
    parser.add_argument("--export-dir", default=str(DEFAULT_EXPORT_DIR), help="Directory for zotero-veille-YYYY-WW.csl.json.")
    parser.add_argument("--include-ignored", action="store_true", help="Include ignored items in the CSL JSON export.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = export_csl_json(
        db_path=args.db,
        export_dir=args.export_dir,
        include_ignored=args.include_ignored,
    )
    print(f"Exported {result['items_exported']} items to {result['export_path']}")


if __name__ == "__main__":
    main()
