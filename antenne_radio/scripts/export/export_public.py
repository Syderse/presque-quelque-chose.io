from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import read_json, utc_now_iso, write_json  # noqa: E402
from scripts.core.models import RadioWatchItem, WatchStatus  # noqa: E402


DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_OUTPUT = SITE_ROOT / "static" / "antenne-radio" / "index.json"
SCHEMA_VERSION = "antenne-radio-public-v0"

PUBLIC_ITEM_KEYS = {
    "id",
    "title",
    "url",
    "doi",
    "published_at",
    "source_name",
    "source_type",
    "language",
    "source_family",
    "attribution_id",
}

FORBIDDEN_PUBLIC_KEYS = {
    "raw",
    "abstract",
    "logs",
    "notes",
    "status",
    "relevance_score",
    "score_explanation",
    "keywords_matched",
    "negative_keywords_matched",
    "discovered_at",
    "source_feed",
    "source_api",
    "title_original",
    "errors",
    "raw_responses",
    "authors",
    "tags",
}

AUDITED_ATTRIBUTIONS: dict[str, dict[str, str]] = {
    "radio_survivor": {
        "name": "Radio Survivor",
        "url": "https://www.radiosurvivor.com/",
        "source_family": "rss",
        "attribution_text": "Source: Radio Survivor - lien vers l'article original.",
    },
    "journal_radio_audio_media": {
        "name": "Journal of Radio & Audio Media / Taylor & Francis Online",
        "url": "https://www.tandfonline.com/journals/hjrs20",
        "source_family": "rss",
        "attribution_text": "Source: Journal of Radio & Audio Media / Taylor & Francis Online - lien vers la notice originale.",
    },
    "radio_journal": {
        "name": "Radio Journal: International Studies in Broadcast & Audio Media",
        "url": "https://intellectdiscover.com/content/journals/rj",
        "source_family": "crossref",
        "attribution_text": "Source: Radio Journal: International Studies in Broadcast & Audio Media - lien vers la notice originale.",
    },
    "sound_studies_journal": {
        "name": "Sound Studies: An Interdisciplinary Journal",
        "url": "https://www.tandfonline.com/journals/rfso20",
        "source_family": "crossref",
        "attribution_text": "Source: Sound Studies: An Interdisciplinary Journal - lien vers la notice originale.",
    },
    "journal_sonic_studies": {
        "name": "Journal of Sonic Studies",
        "url": "https://www.researchcatalogue.net/view/558606/558607",
        "source_family": "openalex",
        "attribution_text": "Source: Journal of Sonic Studies - lien vers la notice originale.",
    },
    "resonance_journal": {
        "name": "Resonance: The Journal of Sound and Culture",
        "url": "https://online.ucpress.edu/res",
        "source_family": "crossref",
        "attribution_text": "Source: Resonance: The Journal of Sound and Culture - lien vers la notice originale.",
    },
    "sounding_out": {
        "name": "Sounding Out!",
        "url": "https://soundstudiesblog.com/",
        "source_family": "rss",
        "attribution_text": "Source: Sounding Out! - lien vers l'article original.",
    },
    "radiomorphoses": {
        "name": "Radiomorphoses / OpenEdition Journals",
        "url": "https://journals.openedition.org/radiomorphoses/",
        "source_family": "rss",
        "attribution_text": "Source: Radiomorphoses / OpenEdition Journals - lien vers la notice originale.",
    },
    "radio_fanch": {
        "name": "Radio Fañch",
        "url": "https://radiofanch.blogspot.com/",
        "source_family": "rss",
        "attribution_text": "Source: Radio Fañch - lien vers le billet original.",
    },
    "les_radios_libres": {
        "name": "Les Radios Libres",
        "url": "https://lesradioslibres.wordpress.com/",
        "source_family": "rss",
        "attribution_text": "Source: Les Radios Libres - lien vers le billet original.",
    },
    "la_radio_du_futur": {
        "name": "La Radio du Futur",
        "url": "https://radiodufutur.wordpress.com/",
        "source_family": "rss",
        "attribution_text": "Source: La Radio du Futur - lien vers le billet original.",
    },
    "la_lettre_pro": {
        "name": "La Lettre Pro de la Radio & du Podcast",
        "url": "https://www.lalettre.pro/",
        "source_family": "rss",
        "attribution_text": "Source: La Lettre Pro de la Radio & du Podcast - lien vers l'article original.",
    },
    "meccsa_radio_audio_studies": {
        "name": "MeCCSA Radio and Audio Studies",
        "url": "https://radiostudiesnetworkreadinggroup.wordpress.com/",
        "source_family": "rss",
        "attribution_text": "Source: MeCCSA Radio and Audio Studies - lien vers le billet original.",
    },
    "nieman_storyboard": {
        "name": "Nieman Storyboard",
        "url": "https://niemanstoryboard.org/",
        "source_family": "rss",
        "attribution_text": "Source: Nieman Storyboard - lien vers l'article original.",
    },
    "transom": {
        "name": "Transom",
        "url": "https://transom.org/",
        "source_family": "rss",
        "attribution_text": "Source: Transom - lien vers l'article original.",
    },
    "hal": {
        "name": "HAL open archive",
        "url": "https://hal.science/",
        "source_family": "hal",
        "attribution_text": "Source: HAL open archive - lien vers la notice HAL.",
    },
    "openalex": {
        "name": "OpenAlex",
        "url": "https://openalex.org/",
        "source_family": "openalex",
        "attribution_text": "Source: OpenAlex - lien vers la notice originale.",
    },
}

ATTRIBUTION_BY_SOURCE_NAME = {
    "Radio Survivor": "radio_survivor",
    "Journal of Radio & Audio Media": "journal_radio_audio_media",
    "Radio Journal: International Studies in Broadcast & Audio Media": "radio_journal",
    "Radio Journal:International Studies in Broadcast & Audio Media": "radio_journal",
    "The Radio Journal: International Studies in Broadcast & Audio Media": "radio_journal",
    "Sound Studies": "sound_studies_journal",
    "Sound Studies: An Interdisciplinary Journal": "sound_studies_journal",
    "Journal of Sonic Studies": "journal_sonic_studies",
    "Resonance: The Journal of Sound and Culture": "resonance_journal",
    "Resonance The Journal of Sound and Culture": "resonance_journal",
    "Sounding Out!": "sounding_out",
    "Radiomorphoses": "radiomorphoses",
    "Radio Fañch": "radio_fanch",
    "Les Radios Libres": "les_radios_libres",
    "La Radio du Futur": "la_radio_du_futur",
    "La Lettre Pro de la Radio": "la_lettre_pro",
    "MeCCSA Radio & Audio Studies": "meccsa_radio_audio_studies",
    "Nieman Storyboard": "nieman_storyboard",
    "Transom": "transom",
    "HAL radio studies search": "hal",
    "OpenAlex": "openalex",
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


def _public_status(item: RadioWatchItem) -> bool:
    return item.status in {WatchStatus.to_read, WatchStatus.candidate, WatchStatus.exported}


def _attribution_id(item: RadioWatchItem) -> str | None:
    return ATTRIBUTION_BY_SOURCE_NAME.get(item.source_name)


def _source_family(item: RadioWatchItem, attribution_id: str) -> str:
    return AUDITED_ATTRIBUTIONS[attribution_id]["source_family"]


def _public_url(item: RadioWatchItem) -> str | None:
    if item.url:
        return item.url
    if item.doi:
        return f"https://doi.org/{item.doi}"
    return None


def _iso_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _is_publishable(item: RadioWatchItem) -> bool:
    if not _public_status(item):
        return False
    if _attribution_id(item) is None:
        return False
    return _public_url(item) is not None


def _sort_items(items: list[RadioWatchItem]) -> list[RadioWatchItem]:
    def sort_key(item: RadioWatchItem) -> tuple[str, str, str]:
        date_value = item.published_at or item.discovered_at
        return (date_value.isoformat(), item.source_name, item.id)

    return sorted(items, key=sort_key, reverse=True)


def _item_to_public(item: RadioWatchItem) -> dict[str, Any]:
    attribution_id = _attribution_id(item)
    if attribution_id is None:
        raise ValueError(f"Unaudited source cannot be exported: {item.source_name}")

    attribution = AUDITED_ATTRIBUTIONS[attribution_id]
    public_item = {
        "id": item.id,
        "title": item.title,
        "url": _public_url(item),
        "doi": item.doi,
        "published_at": _iso_datetime(item.published_at),
        "source_name": attribution["name"],
        "source_type": item.source_type.value,
        "language": item.language,
        "source_family": attribution["source_family"],
        "attribution_id": attribution_id,
    }

    if set(public_item) != PUBLIC_ITEM_KEYS:
        raise ValueError("Public item does not match the strict whitelist")

    return public_item


def _sources_payload(attribution_ids: set[str]) -> list[dict[str, str]]:
    sources = []
    for attribution_id in sorted(attribution_ids):
        source = dict(AUDITED_ATTRIBUTIONS[attribution_id])
        source["attribution_id"] = attribution_id
        sources.append(source)

    return sources


def _assert_no_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_PUBLIC_KEYS:
                raise ValueError(f"Forbidden public key found: {key}")
            _assert_no_forbidden_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_no_forbidden_keys(nested)


def build_public_payload(
    *,
    items: list[RadioWatchItem],
    generated_at: datetime | str | None = None,
) -> dict[str, Any]:
    _, generated_at_text = _generated_at_value(generated_at)
    publishable_items = [item for item in items if _is_publishable(item)]
    public_items = [_item_to_public(item) for item in _sort_items(publishable_items)]
    attribution_ids = {item["attribution_id"] for item in public_items}

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at_text,
        "item_count": len(public_items),
        "items": public_items,
        "sources": _sources_payload(attribution_ids),
    }
    _assert_no_forbidden_keys(payload)
    return payload


def export_public_json(
    *,
    db_path: str | Path = DEFAULT_DB,
    output_path: str | Path = DEFAULT_OUTPUT,
    generated_at: datetime | str | None = None,
) -> dict[str, Any]:
    raw_items = _load_items(db_path)
    items = _valid_items(raw_items)
    payload = build_public_payload(items=items, generated_at=generated_at)
    export_path = write_json(output_path, payload)

    return {
        "generated_at": payload["generated_at"],
        "export_path": str(export_path),
        "items_exported": payload["item_count"],
        "sources_exported": len(payload["sources"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a strict public radio-watch JSON index for Hugo.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to data/normalized/db.json.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output path for the public JSON index.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = export_public_json(db_path=args.db, output_path=args.output)
    print(f"Exported {result['items_exported']} public items to {result['export_path']}")


if __name__ == "__main__":
    main()
