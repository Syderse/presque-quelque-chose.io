import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import SourceType, WatchStatus  # noqa: E402
from scripts.export import export_csl  # noqa: E402


GENERATED_AT = datetime(2026, 5, 18, 12, 0, tzinfo=timezone.utc)


def item_payload(**overrides):
    payload = {
        "id": "manual:test",
        "title": "Radio libre et archives",
        "source_name": "Fixture source",
        "source_type": SourceType.journal_article.value,
        "language": "fr",
        "status": WatchStatus.to_read.value,
        "discovered_at": GENERATED_AT.isoformat(),
        "authors": ["A. Fixture"],
        "published_at": GENERATED_AT.isoformat(),
        "url": "https://example.org/radio",
        "doi": "10.1234/radio.2026",
        "abstract": "<p>Un résumé sur la radio &amp; l'écoute.</p>",
        "tags": ["radio"],
        "keywords_matched": ["radio libre"],
        "negative_keywords_matched": [],
        "relevance_score": 8,
        "score_explanation": "+6 radio libre dans title; score final 8",
        "raw": {},
    }
    payload.update(overrides)
    return payload


def write_db(path, items):
    path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def test_csl_export_creates_manual_zotero_file(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload()])

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )

    export_path = Path(result["export_path"])
    assert export_path.exists()
    assert export_path.name == "zotero-veille-2026-21.csl.json"
    assert result["items_exported"] == 1


def test_csl_export_maps_core_fields(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload()])

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(Path(result["export_path"]).read_text(encoding="utf-8"))

    assert exported == [
        {
            "DOI": "10.1234/radio.2026",
            "URL": "https://example.org/radio",
            "abstract": "Un résumé sur la radio & l'écoute.",
            "accessed": {"date-parts": [[2026, 5, 18]]},
            "author": [{"literal": "A. Fixture"}],
            "container-title": "Fixture source",
            "id": "manual:test",
            "issued": {"date-parts": [[2026, 5, 18]]},
            "keyword": "radio, radio libre",
            "language": "fr",
            "title": "Radio libre et archives",
            "type": "article-journal",
        }
    ]


def test_csl_export_keeps_utf8_readable(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(
        db_path,
        [
            item_payload(
                title="ラジオ研究とコミュニティFM",
                abstract="音と聴取についてのメモ。",
                tags=["ラジオ研究"],
            )
        ],
    )

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    content = Path(result["export_path"]).read_text(encoding="utf-8")

    assert "ラジオ研究とコミュニティFM" in content
    assert "音と聴取についてのメモ。" in content


def test_csl_export_defaults_to_to_read_and_candidate(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(
        db_path,
        [
            item_payload(id="manual:to-read", status=WatchStatus.to_read.value),
            item_payload(id="manual:candidate", title="Podcast candidat", status=WatchStatus.candidate.value),
            item_payload(id="manual:ignored", title="Bruit technique", status=WatchStatus.ignored.value),
        ],
    )

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(Path(result["export_path"]).read_text(encoding="utf-8"))

    assert result["items_exported"] == 2
    assert {item["id"] for item in exported} == {"manual:to-read", "manual:candidate"}


def test_csl_export_can_include_ignored(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload(id="manual:ignored", status=WatchStatus.ignored.value)])

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        include_ignored=True,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(Path(result["export_path"]).read_text(encoding="utf-8"))

    assert result["items_exported"] == 1
    assert result["items_ignored_included"] == 1
    assert exported[0]["id"] == "manual:ignored"


def test_csl_export_does_not_modify_db(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    items = [item_payload(id="manual:to-read", status=WatchStatus.to_read.value)]
    write_db(db_path, items)

    export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )

    saved = json.loads(db_path.read_text(encoding="utf-8"))
    assert saved == items


def test_csl_export_uses_approximate_type_for_blog_items(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload(source_type=SourceType.blog.value)])

    result = export_csl.export_csl_json(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(Path(result["export_path"]).read_text(encoding="utf-8"))

    assert exported[0]["type"] == "webpage"
