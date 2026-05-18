from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path
from time import struct_time
from typing import Any

import feedparser
import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, utc_now_iso, write_json  # noqa: E402


DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
DEFAULT_OUTPUT = ROOT / "data" / "raw" / "rss_latest.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "api.log"
RSS_KINDS = {"rss", "atom"}
NETWORK_TIMEOUT_SECONDS = 20


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid sources config: {path}")

    return data


def _source_kind(source: dict[str, Any]) -> str | None:
    value = source.get("type", source.get("kind"))
    if value is None:
        return None

    return str(value).strip().lower()


def _candidate_sources(config: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(config.get("sources"), list):
        return [source for source in config["sources"] if isinstance(source, dict)]

    if isinstance(config.get("rss_atom"), list):
        return [source for source in config["rss_atom"] if isinstance(source, dict)]

    return []


def select_rss_sources(config: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        source
        for source in _candidate_sources(config)
        if source.get("enabled") is True and _source_kind(source) in RSS_KINDS
    ]


def _jsonable(value: Any) -> Any:
    if isinstance(value, struct_time):
        return list(value)

    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return str(value)


def _authors(entry: dict[str, Any]) -> list[str]:
    authors: list[str] = []

    for author in _entry_value(entry, "authors", []) or []:
        if isinstance(author, dict) and author.get("name"):
            authors.append(str(author["name"]).strip())
        elif isinstance(author, str):
            authors.append(author.strip())

    author = _entry_value(entry, "author")
    if isinstance(author, str) and author.strip():
        authors.append(author.strip())

    author_detail = _entry_value(entry, "author_detail")
    if isinstance(author_detail, dict) and author_detail.get("name"):
        authors.append(str(author_detail["name"]).strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for author_name in authors:
        if author_name and author_name not in seen:
            deduped.append(author_name)
            seen.add(author_name)

    return deduped


def _entry_value(entry: dict[str, Any], key: str, default: Any = None) -> Any:
    return dict.get(entry, key, default)


def _parse_feed(feed_url: str) -> Any:
    local_path = Path(feed_url)
    if local_path.exists():
        return feedparser.parse(local_path.read_bytes())

    previous_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(NETWORK_TIMEOUT_SECONDS)
    try:
        return feedparser.parse(feed_url)
    finally:
        socket.setdefaulttimeout(previous_timeout)


def _extract_entry(entry: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    source_name = source.get("name") or source.get("id") or "unknown"
    source_feed = source.get("url")

    return {
        "title": _entry_value(entry, "title"),
        "link": _entry_value(entry, "link"),
        "published": _entry_value(entry, "published"),
        "updated": _entry_value(entry, "updated"),
        "authors": _authors(entry),
        "summary": _entry_value(entry, "summary") or _entry_value(entry, "description"),
        "source_name": source_name,
        "source_feed": source_feed,
        "raw": _jsonable(entry),
    }


def ingest_sources(
    sources: list[dict[str, Any]],
    *,
    log_path: str | Path = DEFAULT_LOG,
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    source_results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for source in sources:
        source_name = str(source.get("name") or source.get("id") or "unknown")
        source_feed = str(source.get("url") or "")

        if not source_feed:
            message = f"RSS source {source_name} has no url"
            append_log(log_path, message, level="ERROR")
            errors.append({"source_name": source_name, "error": message})
            continue

        try:
            parsed = _parse_feed(source_feed)
            if getattr(parsed, "bozo", False):
                bozo_exception = getattr(parsed, "bozo_exception", "unknown feedparser error")
                warning = f"parse warning: {bozo_exception}"
                append_log(
                    log_path,
                    f"RSS source {source_name} reported a {warning}",
                    level="ERROR",
                )
                errors.append({"source_name": source_name, "source_feed": source_feed, "error": warning})

            source_entries = [_extract_entry(entry, source) for entry in parsed.entries]
            entries.extend(source_entries)
            source_results.append(
                {
                    "source_name": source_name,
                    "source_feed": source_feed,
                    "entry_count": len(source_entries),
                    "status": getattr(parsed, "status", None),
                }
            )
        except Exception as exc:  # noqa: BLE001 - ingestion must continue source by source.
            message = f"RSS source {source_name} failed: {exc}"
            append_log(log_path, message, level="ERROR")
            errors.append({"source_name": source_name, "source_feed": source_feed, "error": str(exc)})

    return {
        "connector": "rss",
        "generated_at": utc_now_iso(),
        "entry_count": len(entries),
        "entries": entries,
        "sources": source_results,
        "errors": errors,
    }


def ingest_rss(
    *,
    config_path: str | Path = DEFAULT_CONFIG,
    output_path: str | Path = DEFAULT_OUTPUT,
    log_path: str | Path = DEFAULT_LOG,
) -> dict[str, Any]:
    config = load_config(config_path)
    sources = select_rss_sources(config)
    payload = ingest_sources(sources, log_path=log_path)
    payload["config"] = str(config_path)
    write_json(output_path, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest enabled RSS/Atom sources into a raw JSON dump.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to sources.yaml.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to the raw RSS JSON dump.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = ingest_rss(config_path=args.config, output_path=args.output)
    print(f"Wrote {payload['entry_count']} RSS/Atom entries to {args.output}")


if __name__ == "__main__":
    main()
