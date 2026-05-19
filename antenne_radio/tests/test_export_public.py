import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import SourceType, WatchStatus  # noqa: E402
from scripts.export import export_public  # noqa: E402


GENERATED_AT = datetime(2026, 5, 19, 12, 0, tzinfo=timezone.utc)
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
FORBIDDEN_KEYS = {
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


def item_payload(**overrides):
    payload = {
        "id": "manual:test",
        "title": "Radio libre et archives",
        "source_name": "Radio Survivor",
        "source_type": SourceType.blog.value,
        "language": "fr",
        "status": WatchStatus.to_read.value,
        "discovered_at": GENERATED_AT.isoformat(),
        "authors": ["A. Fixture"],
        "published_at": GENERATED_AT.isoformat(),
        "url": "https://example.org/radio",
        "doi": "10.1234/radio.2026",
        "abstract": "<p>Un résumé privé.</p>",
        "tags": ["radio"],
        "keywords_matched": ["radio libre"],
        "negative_keywords_matched": [],
        "relevance_score": 8,
        "score_explanation": "+6 radio libre dans title; score final 8",
        "source_feed": "https://example.org/feed.xml",
        "source_api": "rss",
        "title_original": "Radio libre et archives",
        "raw": {"entry": "private"},
    }
    payload.update(overrides)
    return payload


def write_db(path, items):
    path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def forbidden_keys(value):
    found = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_KEYS:
                found.add(key)
            found.update(forbidden_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(forbidden_keys(nested))
    return found


def test_public_export_creates_whitelisted_json(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload()])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )

    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["items_exported"] == 1
    assert exported["schema_version"] == "antenne-radio-public-v0"
    assert exported["generated_at"] == "2026-05-19T12:00:00Z"
    assert exported["item_count"] == 1
    assert set(exported["items"][0]) == PUBLIC_ITEM_KEYS
    assert exported["items"][0] == {
        "attribution_id": "radio_survivor",
        "doi": "10.1234/radio.2026",
        "id": "manual:test",
        "language": "fr",
        "published_at": "2026-05-19T12:00:00Z",
        "source_family": "rss",
        "source_name": "Radio Survivor",
        "source_type": "blog",
        "title": "Radio libre et archives",
        "url": "https://example.org/radio",
    }


def test_public_export_excludes_private_fields_recursively(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload()])

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert forbidden_keys(exported) == set()
    content = output_path.read_text(encoding="utf-8")
    assert "Un résumé privé" not in content
    assert "private" not in content
    assert "score final" not in content
    assert "https://example.org/feed.xml" not in content


def test_public_export_keeps_only_public_statuses_and_audited_sources(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(id="manual:to-read", status=WatchStatus.to_read.value),
            item_payload(id="manual:candidate", status=WatchStatus.candidate.value),
            item_payload(id="manual:exported", status=WatchStatus.exported.value),
            item_payload(id="manual:ignored", status=WatchStatus.ignored.value),
            item_payload(id="manual:new", status=WatchStatus.new.value),
            item_payload(id="manual:crossref", source_name="Crossref radio journals", source_api="crossref"),
        ],
    )

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["items_exported"] == 3
    assert {item["id"] for item in exported["items"]} == {
        "manual:to-read",
        "manual:candidate",
        "manual:exported",
    }


def test_public_export_adds_source_attributions(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(id="manual:rss", source_name="Sounding Out!"),
            item_payload(
                id="manual:hal",
                source_name="HAL radio studies search",
                source_type=SourceType.journal_article.value,
                source_api="hal",
            ),
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert {source["attribution_id"] for source in exported["sources"]} == {"hal", "sounding_out"}
    assert {item["attribution_id"] for item in exported["items"]} == {"hal", "sounding_out"}
    assert {item["source_name"] for item in exported["items"]} == {"HAL open archive", "Sounding Out!"}
    assert all(source["attribution_text"].startswith("Source: ") for source in exported["sources"])


def test_public_export_uses_doi_url_fallback(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(url=None, doi="10.1234/radio.2026")])

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert exported["items"][0]["url"] == "https://doi.org/10.1234/radio.2026"


def test_public_export_skips_items_without_public_link(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(url=None, doi=None)])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["items_exported"] == 0
    assert exported["items"] == []
    assert exported["sources"] == []


def test_public_export_does_not_modify_db(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    items = [item_payload()]
    write_db(db_path, items)

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )

    assert json.loads(db_path.read_text(encoding="utf-8")) == items
