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

from scripts.core.io import ensure_parent_dir, read_json, utc_now_iso, write_json  # noqa: E402
from scripts.core.models import RadioWatchItem, WatchStatus  # noqa: E402


DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_EXPORT_DIR = ROOT / "data" / "exports"
WHITESPACE_RE = re.compile(r"\s+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
EMPTY_ABSTRACT_RE = re.compile(r"^[\s\W_]+$", re.UNICODE)


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


def _extract_items_payload(payload: Any) -> tuple[list[Any], bool]:
    if isinstance(payload, list):
        return payload, False
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"], True

    raise ValueError("db.json must be a list or an object with an items list")


def _load_items(db_path: str | Path) -> tuple[Any, list[dict[str, Any]], bool]:
    payload = read_json(db_path, default=[])
    raw_items, is_wrapped = _extract_items_payload(payload)
    return payload, [item for item in raw_items if isinstance(item, dict)], is_wrapped


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


def _format_number(value: float | None) -> str:
    if value is None:
        return "non scoré"
    if value.is_integer():
        return str(int(value))
    return f"{value:g}"


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


def _format_date(item: RadioWatchItem) -> str:
    value = item.published_at or item.discovered_at
    return value.date().isoformat()


def _format_authors(authors: list[str]) -> str:
    return ", ".join(authors) if authors else "Non renseigné"


def _quote_block(text: str) -> str:
    compacted = _plain_text(text)
    if not compacted:
        return ""

    lines = compacted.splitlines() or [compacted]
    return "\n".join(f"> {line}" if line else ">" for line in lines)


def _render_item(item: RadioWatchItem) -> str:
    link = item.url or (f"https://doi.org/{item.doi}" if item.doi else "Non renseigné")
    lines = [
        f"### {item.title}",
        "",
        f"- Auteurs : {_format_authors(item.authors)}",
        f"- Source : {item.source_name}",
        f"- Date : {_format_date(item)}",
        f"- Lien : {link}",
        f"- Score : {_format_number(item.relevance_score)}",
        f"- Explication : {item.score_explanation or 'Non renseignée'}",
    ]

    if item.doi:
        lines.insert(6, f"- DOI : {item.doi}")

    abstract = _quote_block(item.abstract or "")
    if abstract:
        lines.extend(["", "**Abstract**", "", abstract])

    return "\n".join(lines).rstrip()


def _render_section(title: str, items: list[RadioWatchItem]) -> str:
    lines = [f"## {title}", ""]
    if not items:
        lines.append("_Aucun item._")
    else:
        lines.append("\n\n".join(_render_item(item) for item in _sort_items(items)))

    return "\n".join(lines).rstrip()


def _render_frontmatter(
    *,
    generated_at: str,
    week: str,
    items_to_read: int,
    items_candidate: int,
) -> str:
    return "\n".join(
        [
            "---",
            "type: veille-radio",
            f'generated_at: "{generated_at}"',
            f'week: "{week}"',
            f"items_to_read: {items_to_read}",
            f"items_candidate: {items_candidate}",
            "---",
        ]
    )


def render_report(
    *,
    items: list[RadioWatchItem],
    generated_at: str,
    week: str,
    include_ignored: bool = False,
) -> str:
    to_read = [item for item in items if item.status is WatchStatus.to_read]
    candidates = [item for item in items if item.status is WatchStatus.candidate]
    ignored = [item for item in items if item.status is WatchStatus.ignored]

    sections = [
        _render_frontmatter(
            generated_at=generated_at,
            week=week,
            items_to_read=len(to_read),
            items_candidate=len(candidates),
        ),
        "",
        f"# Veille radio - semaine {week}",
        "",
        _render_section("À lire", to_read),
        "",
        _render_section("Candidats", candidates),
    ]
    if include_ignored:
        sections.extend(["", _render_section("Ignorés intéressants", ignored)])

    return "\n".join(sections).rstrip() + "\n"


def _mark_exported_items(
    raw_items: list[dict[str, Any]],
    exported_ids: set[str],
) -> list[dict[str, Any]]:
    updated_items: list[dict[str, Any]] = []
    for raw_item in raw_items:
        item = dict(raw_item)
        if item.get("id") in exported_ids and item.get("status") == WatchStatus.to_read.value:
            item["status"] = WatchStatus.exported.value
        updated_items.append(item)

    return updated_items


def export_weekly_report(
    *,
    db_path: str | Path = DEFAULT_DB,
    export_dir: str | Path = DEFAULT_EXPORT_DIR,
    include_ignored: bool = False,
    mark_exported: bool = False,
    generated_at: datetime | str | None = None,
) -> dict[str, Any]:
    generated_dt, generated_at_text = _generated_at_value(generated_at)
    week = _iso_week(generated_dt)
    payload, raw_items, is_wrapped = _load_items(db_path)
    items = _valid_items(raw_items)
    to_read = [item for item in items if item.status is WatchStatus.to_read]
    candidates = [item for item in items if item.status is WatchStatus.candidate]

    export_path = Path(export_dir) / f"veille-{week}.md"
    report = render_report(
        items=items,
        generated_at=generated_at_text,
        week=week,
        include_ignored=include_ignored,
    )
    target = ensure_parent_dir(export_path)
    target.write_text(report, encoding="utf-8")

    if mark_exported:
        exported_ids = {item.id for item in to_read}
        updated_items = _mark_exported_items(raw_items, exported_ids)
        output: Any = updated_items
        if is_wrapped:
            output = dict(payload)
            output["items"] = updated_items
        write_json(db_path, output)

    return {
        "generated_at": generated_at_text,
        "week": week,
        "export_path": str(export_path),
        "items_to_read": len(to_read),
        "items_candidate": len(candidates),
        "marked_exported": len(to_read) if mark_exported else 0,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export scored radio-watch items to an Obsidian-friendly Markdown report.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to data/normalized/db.json.")
    parser.add_argument("--export-dir", default=str(DEFAULT_EXPORT_DIR), help="Directory for veille-YYYY-WW.md.")
    parser.add_argument("--include-ignored", action="store_true", help="Include an Ignorés intéressants section.")
    parser.add_argument("--mark-exported", action="store_true", help="Mark exported to_read items as exported in db.json.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = export_weekly_report(
        db_path=args.db,
        export_dir=args.export_dir,
        include_ignored=args.include_ignored,
        mark_exported=args.mark_exported,
    )
    print(
        f"Exported {result['items_to_read']} to_read and {result['items_candidate']} candidate items "
        f"to {result['export_path']}"
    )


if __name__ == "__main__":
    main()
