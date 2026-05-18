import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import SourceType, WatchStatus  # noqa: E402
from scripts.export import export_obsidian  # noqa: E402


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
        "abstract": "Un résumé sur la radio.",
        "tags": [],
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


def test_export_creates_markdown_file(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload()])

    result = export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )

    export_path = Path(result["export_path"])
    assert export_path.exists()
    assert export_path.name == "veille-2026-21.md"


def test_export_contains_expected_sections(tmp_path):
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

    result = export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    content = Path(result["export_path"]).read_text(encoding="utf-8")

    assert "type: veille-radio" in content
    assert 'week: "2026-21"' in content
    assert "items_to_read: 1" in content
    assert "items_candidate: 1" in content
    assert "## À lire" in content
    assert "## Candidats" in content
    assert "## Ignorés intéressants" not in content
    assert "Podcast candidat" in content
    assert "Bruit technique" not in content


def test_include_ignored_adds_optional_section(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(db_path, [item_payload(id="manual:ignored", title="Bruit technique", status=WatchStatus.ignored.value)])

    result = export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        include_ignored=True,
        generated_at=GENERATED_AT,
    )
    content = Path(result["export_path"]).read_text(encoding="utf-8")

    assert "## Ignorés intéressants" in content
    assert "Bruit technique" in content


def test_japanese_characters_remain_readable(tmp_path):
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

    result = export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )
    content = Path(result["export_path"]).read_text(encoding="utf-8")

    assert "ラジオ研究とコミュニティFM" in content
    assert "音と聴取についてのメモ。" in content


def test_default_export_does_not_change_statuses(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    items = [item_payload(id="manual:to-read", status=WatchStatus.to_read.value)]
    write_db(db_path, items)

    export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        generated_at=GENERATED_AT,
    )

    saved = json.loads(db_path.read_text(encoding="utf-8"))
    assert saved == items


def test_mark_exported_only_marks_to_read_items(tmp_path):
    db_path = tmp_path / "db.json"
    export_dir = tmp_path / "exports"
    write_db(
        db_path,
        [
            item_payload(id="manual:to-read", status=WatchStatus.to_read.value),
            item_payload(id="manual:candidate", title="Podcast candidat", status=WatchStatus.candidate.value),
        ],
    )

    result = export_obsidian.export_weekly_report(
        db_path=db_path,
        export_dir=export_dir,
        mark_exported=True,
        generated_at=GENERATED_AT,
    )
    saved = json.loads(db_path.read_text(encoding="utf-8"))

    assert result["marked_exported"] == 1
    assert saved[0]["status"] == WatchStatus.exported.value
    assert saved[1]["status"] == WatchStatus.candidate.value
