import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core import normalize  # noqa: E402
from scripts.ingest import ingest_rss  # noqa: E402


RSS_FIXTURE = ROOT / "tests" / "fixtures" / "sample_rss.xml"
HAL_FIXTURE = ROOT / "tests" / "fixtures" / "hal_response.json"
DISCOVERED_AT = datetime(2026, 5, 18, 12, 0, tzinfo=timezone.utc)


def rss_fixture_entry():
    payload = ingest_rss.ingest_sources(
        [
            {
                "id": "fixture",
                "name": "Fixture Radio",
                "enabled": True,
                "type": "rss",
                "url": str(RSS_FIXTURE),
            }
        ]
    )
    return payload["entries"][0]


def hal_fixture_doc():
    payload = json.loads(HAL_FIXTURE.read_text(encoding="utf-8"))
    return payload["response"]["docs"][0]


def test_normalize_rss_entry_from_fixture():
    item = normalize.normalize_rss_entry(rss_fixture_entry(), discovered_at=DISCOVERED_AT)

    assert item.title == "Community radio archives open again"
    assert item.url == "https://example.org/radio/archive-open"
    assert item.source_name == "Fixture Radio"
    assert item.source_api == "rss"
    assert item.raw["title"] == "Community radio archives open again"


def test_normalize_hal_entry_from_fixture():
    item = normalize.normalize_hal_entry(
        hal_fixture_doc(),
        source_name="HAL fixture",
        source_api="hal",
        discovered_at=DISCOVERED_AT,
    )

    assert item.title == "Radio libre et archives sonores"
    assert item.url == "https://hal.science/hal-0123456"
    assert item.source_name == "HAL fixture"
    assert item.source_api == "hal"
    assert item.authors == ["Fixture Author"]
    assert item.raw["docid"] == 123456


def test_identical_passes_do_not_create_duplicates(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(json.dumps({"entries": [rss_fixture_entry()]}), encoding="utf-8")
    hal_dump.write_text(
        json.dumps({"source_name": "HAL fixture", "source_api": "hal", "docs": [hal_fixture_doc()]}),
        encoding="utf-8",
    )

    first = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        db_path=db_path,
        log_path=log_path,
    )
    second = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        db_path=db_path,
        log_path=log_path,
    )
    saved = normalize.load_existing_db(db_path, log_path=log_path)

    assert first["added_count"] == 2
    assert second["added_count"] == 0
    assert len(saved) == 2


def test_invalid_entry_is_logged_and_valid_entries_continue(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(
        json.dumps({"entries": [{"title": "", "link": "", "source_name": "Broken"}, rss_fixture_entry()]}),
        encoding="utf-8",
    )
    hal_dump.write_text(json.dumps({"docs": []}), encoding="utf-8")

    result = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        db_path=db_path,
        log_path=log_path,
    )

    assert result["saved_count"] == 1
    assert "Invalid RSS entry skipped at index 0" in log_path.read_text(encoding="utf-8")
