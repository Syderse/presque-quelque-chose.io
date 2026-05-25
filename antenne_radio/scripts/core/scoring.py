from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import read_json, utc_now_iso, write_json  # noqa: E402
from scripts.core.models import RadioWatchItem, WatchStatus  # noqa: E402


DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_KEYWORDS = ROOT / "config" / "keywords.yaml"
DEFAULT_SCORING = ROOT / "config" / "scoring.yaml"
WORDISH_RE = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]")


@dataclass(frozen=True)
class KeywordPattern:
    category: str
    keyword: str
    weight: float
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class MatchContribution:
    category: str
    keyword: str
    field: str
    contribution: float
    weight: float
    multiplier: float


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    if not isinstance(payload, dict):
        raise ValueError(f"Invalid YAML object at {path}")

    return payload


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    escaped = re.escape(keyword.strip())
    if WORDISH_RE.search(keyword):
        escaped = escaped.replace(r"\ ", r"\s+")
        return re.compile(rf"(?<![\w-]){escaped}(?![\w-])", re.IGNORECASE)

    return re.compile(escaped, re.IGNORECASE)


def compile_keyword_patterns(
    keywords_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> list[KeywordPattern]:
    weights = scoring_config.get("weights", {})
    if not isinstance(weights, dict):
        raise ValueError("scoring.yaml must define a weights mapping")

    patterns: list[KeywordPattern] = []
    for category, keywords in keywords_config.items():
        if category == "version":
            continue
        if category not in weights:
            continue
        if not isinstance(keywords, list):
            continue

        for keyword in keywords:
            text = str(keyword).strip()
            if not text:
                continue
            patterns.append(
                KeywordPattern(
                    category=category,
                    keyword=text,
                    weight=float(weights[category]),
                    pattern=_keyword_pattern(text),
                )
            )

    return patterns


def _field_text(item: RadioWatchItem, field: str) -> str:
    value = getattr(item, field, None)
    if value is None:
        return ""
    if isinstance(value, list):
        return " ; ".join(str(part) for part in value if str(part).strip())

    return str(value)


def _unique_keywords(contributions: list[MatchContribution]) -> list[str]:
    seen: set[tuple[str, str]] = set()
    keywords: list[str] = []
    for contribution in contributions:
        key = (contribution.category, contribution.keyword.casefold())
        if key in seen:
            continue
        seen.add(key)
        keywords.append(contribution.keyword)

    return keywords


def _format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:g}"


def _status_for_score(score: float, scoring_config: dict[str, Any]) -> WatchStatus:
    thresholds = scoring_config.get("thresholds", {})
    to_read_gte = float(thresholds.get("to_read", {}).get("gte", 6))
    candidate_gte = float(thresholds.get("candidate", {}).get("gte", 2))

    if score >= to_read_gte:
        return WatchStatus.to_read
    if score >= candidate_gte:
        return WatchStatus.candidate

    return WatchStatus.ignored


def _apply_academic_floor(
    source_api: str | None,
    score: float,
    status: WatchStatus,
    scoring_config: dict[str, Any],
) -> tuple[WatchStatus, bool]:
    """Applies a minimum 'candidate' status for academic sources with non-negative score."""
    floor_config = scoring_config.get("academic_source_floor")
    if not isinstance(floor_config, dict):
        return status, False

    source_apis = set(floor_config.get("source_apis", []))
    if not source_apis or source_api not in source_apis:
        return status, False

    min_score = float(floor_config.get("min_score", 0))
    if score < min_score:
        return status, False

    if status is WatchStatus.ignored:
        return WatchStatus.candidate, True

    return status, False


def _status_reason(score: float, scoring_config: dict[str, Any], status: WatchStatus) -> str:
    thresholds = scoring_config.get("thresholds", {})
    to_read_gte = float(thresholds.get("to_read", {}).get("gte", 6))
    candidate_gte = float(thresholds.get("candidate", {}).get("gte", 2))
    score_text = _format_number(score)

    if status is WatchStatus.to_read:
        return f"statut to_read car score {score_text} >= {to_read_gte:g}"
    if status is WatchStatus.candidate:
        return f"statut candidate car {candidate_gte:g} <= score {score_text} < {to_read_gte:g}"

    return f"statut ignored car score {score_text} < {candidate_gte:g}"


def build_score_explanation(
    contributions: list[MatchContribution],
    score: float,
    status: WatchStatus,
    scoring_config: dict[str, Any],
) -> str:
    parts: list[str] = []
    for contribution in contributions:
        sign = "+" if contribution.contribution >= 0 else ""
        parts.append(
            (
                f"{sign}{_format_number(contribution.contribution)} "
                f"{contribution.keyword} dans {contribution.field} "
                f"({contribution.category}: {_format_number(contribution.weight)}"
                f" x {_format_number(contribution.multiplier)})"
            )
        )

    if not parts:
        parts.append("aucun mot-clé configuré détecté")

    parts.append(f"score final {_format_number(score)}; {_status_reason(score, scoring_config, status)}")
    return "; ".join(parts)


def score_item(
    item: RadioWatchItem,
    keywords_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> RadioWatchItem:
    fields = scoring_config.get("fields", {})
    if not isinstance(fields, dict):
        raise ValueError("scoring.yaml must define a fields mapping")

    patterns = compile_keyword_patterns(keywords_config, scoring_config)
    contributions: list[MatchContribution] = []

    for pattern in patterns:
        for field, multiplier in fields.items():
            text = _field_text(item, str(field))
            if not text:
                continue
            if not pattern.pattern.search(text):
                continue

            contributions.append(
                MatchContribution(
                    category=pattern.category,
                    keyword=pattern.keyword,
                    field=str(field),
                    contribution=pattern.weight * float(multiplier),
                    weight=pattern.weight,
                    multiplier=float(multiplier),
                )
            )

    score = sum(contribution.contribution for contribution in contributions)
    raw_status = _status_for_score(score, scoring_config)
    floored_status, floor_applied = _apply_academic_floor(item.source_api, score, raw_status, scoring_config)
    positive_contributions = [contribution for contribution in contributions if contribution.contribution > 0]
    negative_contributions = [contribution for contribution in contributions if contribution.contribution < 0]

    explanation = build_score_explanation(contributions, score, raw_status, scoring_config)
    if floor_applied:
        explanation += f"; plancher académique: statut élevé de ignored à candidate (source_api={item.source_api})"

    return item.model_copy(
        update={
            "keywords_matched": _unique_keywords(positive_contributions),
            "negative_keywords_matched": _unique_keywords(negative_contributions),
            "relevance_score": score,
            "score_explanation": explanation,
            "status": floored_status,
        }
    )


def _extract_items_payload(payload: Any) -> tuple[list[Any], bool]:
    if isinstance(payload, list):
        return payload, False
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"], True

    raise ValueError("db.json must be a list or an object with an items list")


def score_db(
    *,
    db_path: str | Path = DEFAULT_DB,
    keywords_path: str | Path = DEFAULT_KEYWORDS,
    scoring_path: str | Path = DEFAULT_SCORING,
) -> dict[str, Any]:
    payload = read_json(db_path, default=[])
    raw_items, is_wrapped = _extract_items_payload(payload)
    keywords_config = load_yaml(keywords_path)
    scoring_config = load_yaml(scoring_path)

    scored_items: list[Any] = []
    scored_count = 0
    skipped_count = 0
    invalid_count = 0
    status_counts: dict[str, int] = {}

    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            scored_items.append(raw_item)
            invalid_count += 1
            continue

        if raw_item.get("status") != WatchStatus.new.value:
            scored_items.append(dict(raw_item))
            skipped_count += 1
            status = str(raw_item.get("status", "unknown"))
            status_counts[status] = status_counts.get(status, 0) + 1
            continue

        try:
            item = RadioWatchItem(**raw_item)
        except (TypeError, ValidationError):
            scored_items.append(dict(raw_item))
            invalid_count += 1
            continue

        scored = score_item(item, keywords_config, scoring_config)
        scored_items.append(scored.model_dump(mode="json"))
        scored_count += 1
        status_counts[scored.status.value] = status_counts.get(scored.status.value, 0) + 1

    output: Any = scored_items
    if is_wrapped:
        output = dict(payload)
        output["items"] = scored_items

    write_json(db_path, output)
    return {
        "generated_at": utc_now_iso(),
        "db_path": str(db_path),
        "items_count": len(raw_items),
        "scored_count": scored_count,
        "skipped_count": skipped_count,
        "invalid_count": invalid_count,
        "status_counts": dict(sorted(status_counts.items())),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score normalized radio-watch items.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to data/normalized/db.json.")
    parser.add_argument("--keywords", default=str(DEFAULT_KEYWORDS), help="Path to config/keywords.yaml.")
    parser.add_argument("--scoring", default=str(DEFAULT_SCORING), help="Path to config/scoring.yaml.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = score_db(db_path=args.db, keywords_path=args.keywords, scoring_path=args.scoring)
    counts = ", ".join(f"{status}={count}" for status, count in result["status_counts"].items())
    print(f"Scored {result['scored_count']} items in {args.db} ({counts})")


if __name__ == "__main__":
    main()
