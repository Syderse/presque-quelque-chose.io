import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core import normalize  # noqa: E402
from scripts.core.models import RadioWatchItem, SourceType, WatchStatus  # noqa: E402
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


def crossref_fixture_item():
    return {
        "DOI": "10.1080/19376529.2026.1234567",
        "URL": "https://doi.org/10.1080/19376529.2026.1234567",
        "title": ["Community radio and podcast publics"],
        "container-title": ["Journal of Radio & Audio Media"],
        "published-online": {"date-parts": [[2026, 5, 1]]},
        "author": [{"given": "Ada", "family": "Radio"}],
        "subject": ["Communication", "Radio studies"],
        "abstract": "<jats:p>Radio studies abstract.</jats:p>",
        "language": "en",
        "_crossref_source": {
            "journal_id": "journal_radio_audio_media",
            "journal_name": "Journal of Radio & Audio Media",
            "issn": "1937-6529",
            "endpoint": "https://api.crossref.org/journals/1937-6529/works",
        },
    }


def taylor_rss_doi_entry():
    return {
        "title": "Community radio and podcast publics",
        "link": "https://www.tandfonline.com/doi/full/10.1080/19376529.2026.1234567?src=recsys",
        "published": "2026-05-01T00:00:00Z",
        "source_name": "Journal of Radio & Audio Media",
        "source_feed": "https://www.tandfonline.com/feed/rss/hjrs20",
    }


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


def test_normalize_crossref_entry_from_fixture():
    item = normalize.normalize_crossref_entry(crossref_fixture_item(), discovered_at=DISCOVERED_AT)

    assert item.title == "Community radio and podcast publics"
    assert item.doi == "10.1080/19376529.2026.1234567"
    assert item.url == "https://doi.org/10.1080/19376529.2026.1234567"
    assert item.source_name == "Journal of Radio & Audio Media"
    assert item.source_api == "crossref"
    assert item.authors == ["Ada Radio"]
    assert item.tags == ["Communication", "Radio studies"]


def test_merge_deduplicates_hal_and_crossref_with_same_doi():
    hal_item = normalize.normalize_hal_entry(
        {
            "title_s": ["Community radio and podcast publics"],
            "uri_s": "https://hal.science/hal-999999",
            "doiId_s": "DOI:10.1080/19376529.2026.1234567",
            "producedDate_tdate": "2026-05-01T00:00:00Z",
            "language_s": ["en"],
            "authorFullName_s": ["HAL Author"],
            "abstract_s": ["HAL abstract"],
            "keyword_s": ["radio"],
        },
        source_name="HAL radio studies search",
        source_api="hal",
        discovered_at=DISCOVERED_AT,
    )
    crossref_item = normalize.normalize_crossref_entry(crossref_fixture_item(), discovered_at=DISCOVERED_AT)

    merged = normalize.merge_items_without_duplicates([], [hal_item, crossref_item])

    assert len(merged) == 1
    assert merged[0].id == hal_item.id
    assert merged[0].source_api == "hal"
    assert merged[0].doi == "10.1080/19376529.2026.1234567"
    assert merged[0].authors == ["HAL Author", "Ada Radio"]


def test_merge_deduplicates_taylor_rss_url_and_crossref_doi():
    rss_item = normalize.normalize_rss_entry(taylor_rss_doi_entry(), discovered_at=DISCOVERED_AT)
    crossref_item = normalize.normalize_crossref_entry(crossref_fixture_item(), discovered_at=DISCOVERED_AT)

    merged = normalize.merge_items_without_duplicates([], [rss_item, crossref_item])

    assert len(merged) == 1
    assert merged[0].id == rss_item.id
    assert merged[0].source_name == "Journal of Radio & Audio Media"
    assert merged[0].source_api == "rss"
    assert merged[0].doi == "10.1080/19376529.2026.1234567"
    assert merged[0].abstract == "<jats:p>Radio studies abstract.</jats:p>"


@pytest.mark.parametrize("status", [WatchStatus.to_read, WatchStatus.ignored, WatchStatus.exported])
def test_merge_preserves_existing_human_status_and_legacy_id(status):
    existing_item = RadioWatchItem(
        id="url:legacy-taylor-item",
        title="Community radio and podcast publics",
        source_name="Journal of Radio & Audio Media",
        source_type=SourceType.journal_article,
        language="en",
        status=status,
        discovered_at=DISCOVERED_AT,
        published_at=DISCOVERED_AT,
        url="https://www.tandfonline.com/doi/full/10.1080/19376529.2026.1234567?src=recsys",
        raw={"source": "existing"},
    )
    crossref_item = normalize.normalize_crossref_entry(crossref_fixture_item(), discovered_at=DISCOVERED_AT)

    merged = normalize.merge_items_without_duplicates([existing_item], [crossref_item])

    assert len(merged) == 1
    assert merged[0].id == "url:legacy-taylor-item"
    assert merged[0].status is status
    assert merged[0].doi == "10.1080/19376529.2026.1234567"


def test_merge_deduplicates_title_and_date_when_doi_and_url_are_absent():
    first_item = RadioWatchItem(
        id="fallback:first",
        title="Radio Archives: everyday listening!",
        source_name="Fixture source",
        source_type=SourceType.blog,
        language="en",
        status=WatchStatus.new,
        discovered_at=DISCOVERED_AT,
        published_at=DISCOVERED_AT,
    )
    second_item = RadioWatchItem(
        id="fallback:second",
        title="radio archives everyday listening",
        source_name="Other fixture source",
        source_type=SourceType.blog,
        language="en",
        status=WatchStatus.new,
        discovered_at=DISCOVERED_AT,
        published_at=DISCOVERED_AT,
        abstract="Useful private metadata",
    )

    merged = normalize.merge_items_without_duplicates([], [first_item, second_item])

    assert len(merged) == 1
    assert merged[0].id == "fallback:first"
    assert merged[0].abstract == "Useful private metadata"


def test_identical_passes_do_not_create_duplicates(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    crossref_dump = tmp_path / "data" / "raw" / "crossref_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(json.dumps({"entries": [rss_fixture_entry()]}), encoding="utf-8")
    hal_dump.write_text(
        json.dumps({"source_name": "HAL fixture", "source_api": "hal", "docs": [hal_fixture_doc()]}),
        encoding="utf-8",
    )
    crossref_dump.write_text(json.dumps({"items": [crossref_fixture_item()]}), encoding="utf-8")

    first = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        db_path=db_path,
        log_path=log_path,
    )
    second = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        db_path=db_path,
        log_path=log_path,
    )
    saved = normalize.load_existing_db(db_path, log_path=log_path)

    assert first["added_count"] == 3
    assert second["added_count"] == 0
    assert len(saved) == 3


def test_invalid_entry_is_logged_and_valid_entries_continue(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    crossref_dump = tmp_path / "data" / "raw" / "crossref_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(
        json.dumps({"entries": [{"title": "", "link": "", "source_name": "Broken"}, rss_fixture_entry()]}),
        encoding="utf-8",
    )
    hal_dump.write_text(json.dumps({"docs": []}), encoding="utf-8")
    crossref_dump.write_text(json.dumps({"items": []}), encoding="utf-8")

    result = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        db_path=db_path,
        log_path=log_path,
    )

    assert result["saved_count"] == 1
    assert "Invalid RSS entry skipped at index 0" in log_path.read_text(encoding="utf-8")
