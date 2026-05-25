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
    openalex_dump = tmp_path / "data" / "raw" / "openalex_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)
    openalex_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(json.dumps({"entries": [rss_fixture_entry()]}), encoding="utf-8")
    hal_dump.write_text(
        json.dumps({"source_name": "HAL fixture", "source_api": "hal", "docs": [hal_fixture_doc()]}),
        encoding="utf-8",
    )
    crossref_dump.write_text(json.dumps({"items": [crossref_fixture_item()]}), encoding="utf-8")
    openalex_dump.write_text(json.dumps({"items": []}), encoding="utf-8")

    first = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        openalex_raw_path=openalex_dump,
        db_path=db_path,
        log_path=log_path,
    )
    second = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        openalex_raw_path=openalex_dump,
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
    openalex_dump = tmp_path / "data" / "raw" / "openalex_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)
    openalex_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(
        json.dumps({"entries": [{"title": "", "link": "", "source_name": "Broken"}, rss_fixture_entry()]}),
        encoding="utf-8",
    )
    hal_dump.write_text(json.dumps({"docs": []}), encoding="utf-8")
    crossref_dump.write_text(json.dumps({"items": []}), encoding="utf-8")
    openalex_dump.write_text(json.dumps({"items": []}), encoding="utf-8")

    result = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        openalex_raw_path=openalex_dump,
        db_path=db_path,
        log_path=log_path,
    )

    assert result["saved_count"] == 1
    assert "Invalid RSS entry skipped at index 0" in log_path.read_text(encoding="utf-8")


def openalex_fixture_entry(**overrides):
    entry = {
        "id": "https://openalex.org/W1234567890",
        "doi": "https://doi.org/10.1080/19376529.2026.9999999",
        "display_name": "Community Radio and Sound Art Practices",
        "title": "Community Radio and Sound Art Practices",
        "publication_date": "2026-03-15",
        "publication_year": 2026,
        "type": "article",
        "language": "en",
        "primary_location": {
            "source": {
                "display_name": "Journal of Radio & Audio Media",
            },
            "landing_page_url": "https://www.tandfonline.com/doi/full/10.1080/19376529.2026.9999999",
        },
        "keywords": [
            {"display_name": "Radio studies", "keyword": "Radio studies"},
            {"display_name": "Community radio", "keyword": "Community radio"},
        ],
        "primary_topic": {
            "display_name": "Broadcasting and Media Studies",
        },
        "relevance_score": 42.5,
        "_openalex_source": {
            "profile_id": "radio_studies",
            "profile_label": "Radio studies",
            "endpoint": "https://api.openalex.org/works",
        },
    }
    entry.update(overrides)
    return entry


def test_normalize_openalex_entry_basic():
    item = normalize.normalize_openalex_entry(openalex_fixture_entry(), discovered_at=DISCOVERED_AT)

    assert item.title == "Community Radio and Sound Art Practices"
    assert item.doi == "10.1080/19376529.2026.9999999"
    assert item.url == "https://doi.org/10.1080/19376529.2026.9999999"
    assert item.source_name == "Journal of Radio & Audio Media"
    assert item.source_api == "openalex"
    assert item.language == "en"
    assert "Radio studies" in item.tags
    assert "Community radio" in item.tags
    assert "Broadcasting and Media Studies" in item.tags
    assert item.published_at is not None
    assert item.published_at.year == 2026
    assert item.abstract is None  # Never reconstructed


def test_normalize_openalex_doi_as_url_form():
    item = normalize.normalize_openalex_entry(
        openalex_fixture_entry(doi="https://doi.org/10.1080/19376529.2026.9999999"),
        discovered_at=DISCOVERED_AT,
    )
    assert item.doi == "10.1080/19376529.2026.9999999"

    item2 = normalize.normalize_openalex_entry(
        openalex_fixture_entry(doi="http://dx.doi.org/10.1080/19376529.2026.9999999"),
        discovered_at=DISCOVERED_AT,
    )
    assert item2.doi == "10.1080/19376529.2026.9999999"

    item3 = normalize.normalize_openalex_entry(
        openalex_fixture_entry(doi="doi:10.1080/19376529.2026.9999999"),
        discovered_at=DISCOVERED_AT,
    )
    assert item3.doi == "10.1080/19376529.2026.9999999"

    # All should produce the same stable ID
    assert item.id == item2.id == item3.id


def test_normalize_openalex_doi_from_ids_field():
    entry = openalex_fixture_entry(doi=None)
    entry["ids"] = {"doi": "https://doi.org/10.1080/19376529.2026.9999999", "openalex": "https://openalex.org/W1234567890"}
    item = normalize.normalize_openalex_entry(entry, discovered_at=DISCOVERED_AT)

    assert item.doi == "10.1080/19376529.2026.9999999"
    assert item.url == "https://doi.org/10.1080/19376529.2026.9999999"


def test_normalize_openalex_no_doi_with_landing_page():
    entry = openalex_fixture_entry(doi=None)
    entry["primary_location"]["landing_page_url"] = "https://example.org/article/radio-community"
    item = normalize.normalize_openalex_entry(entry, discovered_at=DISCOVERED_AT)

    assert item.doi is None
    assert item.url == "https://example.org/article/radio-community"


def test_normalize_openalex_no_doi_no_landing_page_fallback_openalex_id():
    entry = openalex_fixture_entry(doi=None)
    entry["primary_location"] = None
    item = normalize.normalize_openalex_entry(entry, discovered_at=DISCOVERED_AT)

    assert item.doi is None
    assert item.url == "https://openalex.org/W1234567890"


def test_normalize_openalex_keywords_as_strings():
    entry = openalex_fixture_entry(keywords=["radio studies", "sound art", "broadcasting"])
    item = normalize.normalize_openalex_entry(entry, discovered_at=DISCOVERED_AT)

    assert "radio studies" in item.tags
    assert "sound art" in item.tags
    assert "broadcasting" in item.tags


def test_normalize_openalex_keywords_mixed_and_invalid():
    entry = openalex_fixture_entry(keywords=[
        {"display_name": "Radio studies"},
        "sound art",
        42,  # should be silently ignored
        None,  # should be silently ignored
        {"keyword": "broadcasting"},
    ])
    item = normalize.normalize_openalex_entry(entry, discovered_at=DISCOVERED_AT)

    assert "Radio studies" in item.tags
    assert "sound art" in item.tags
    assert "broadcasting" in item.tags


def test_merge_deduplicates_openalex_and_crossref_with_same_doi():
    openalex_item = normalize.normalize_openalex_entry(
        openalex_fixture_entry(doi="https://doi.org/10.1080/19376529.2026.1234567"),
        discovered_at=DISCOVERED_AT,
    )
    crossref_item = normalize.normalize_crossref_entry(crossref_fixture_item(), discovered_at=DISCOVERED_AT)

    # Crossref arrives first → OpenAlex must not overwrite it
    merged = normalize.merge_items_without_duplicates([crossref_item], [openalex_item])

    assert len(merged) == 1
    assert merged[0].id == crossref_item.id
    assert merged[0].source_api == "crossref"
    assert merged[0].source_name == "Journal of Radio & Audio Media"
    assert merged[0].doi == "10.1080/19376529.2026.1234567"
    assert merged[0].url == crossref_item.url  # Crossref URL preserved
    assert merged[0].status == crossref_item.status


def test_merge_openalex_does_not_overwrite_existing_stronger_source():
    existing_item = RadioWatchItem(
        id="doi:existing-hal-item",
        title="Community Radio and Sound Art Practices",
        source_name="HAL radio studies search",
        source_type=SourceType.journal_article,
        language="en",
        status=WatchStatus.to_read,
        discovered_at=DISCOVERED_AT,
        published_at=DISCOVERED_AT,
        url="https://hal.science/hal-999999",
        doi="10.1080/19376529.2026.9999999",
        source_api="hal",
        raw={"source": "hal"},
    )
    openalex_item = normalize.normalize_openalex_entry(
        openalex_fixture_entry(),
        discovered_at=DISCOVERED_AT,
    )

    merged = normalize.merge_items_without_duplicates([existing_item], [openalex_item])

    assert len(merged) == 1
    assert merged[0].id == "doi:existing-hal-item"
    assert merged[0].source_name == "HAL radio studies search"
    assert merged[0].source_api == "hal"
    assert merged[0].status is WatchStatus.to_read
    assert merged[0].url == "https://hal.science/hal-999999"


def test_normalize_latest_dumps_includes_openalex(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    crossref_dump = tmp_path / "data" / "raw" / "crossref_latest.json"
    openalex_dump = tmp_path / "data" / "raw" / "openalex_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)
    openalex_dump.parent.mkdir(parents=True, exist_ok=True)

    rss_dump.write_text(json.dumps({"entries": []}), encoding="utf-8")
    hal_dump.write_text(json.dumps({"docs": []}), encoding="utf-8")
    crossref_dump.write_text(json.dumps({"items": []}), encoding="utf-8")
    openalex_dump.write_text(json.dumps({"items": [openalex_fixture_entry()]}), encoding="utf-8")

    result = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        openalex_raw_path=openalex_dump,
        db_path=db_path,
        log_path=log_path,
    )

    assert result["normalized_count"] == 1
    assert result["saved_count"] == 1
    saved = normalize.load_existing_db(db_path, log_path=log_path)
    assert len(saved) == 1
    assert saved[0].source_api == "openalex"
    assert saved[0].doi == "10.1080/19376529.2026.9999999"


def test_normalize_latest_dumps_deduplicates_openalex_crossref(tmp_path):
    rss_dump = tmp_path / "data" / "raw" / "rss_latest.json"
    hal_dump = tmp_path / "data" / "raw" / "hal_latest.json"
    crossref_dump = tmp_path / "data" / "raw" / "crossref_latest.json"
    openalex_dump = tmp_path / "data" / "raw" / "openalex_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    rss_dump.parent.mkdir(parents=True, exist_ok=True)
    hal_dump.parent.mkdir(parents=True, exist_ok=True)
    crossref_dump.parent.mkdir(parents=True, exist_ok=True)
    openalex_dump.parent.mkdir(parents=True, exist_ok=True)

    # Same DOI in both sources
    rss_dump.write_text(json.dumps({"entries": []}), encoding="utf-8")
    hal_dump.write_text(json.dumps({"docs": []}), encoding="utf-8")
    crossref_dump.write_text(json.dumps({"items": [crossref_fixture_item()]}), encoding="utf-8")
    openalex_dump.write_text(
        json.dumps({"items": [openalex_fixture_entry(doi="https://doi.org/10.1080/19376529.2026.1234567")]}),
        encoding="utf-8",
    )

    result = normalize.normalize_latest_dumps(
        rss_raw_path=rss_dump,
        hal_raw_path=hal_dump,
        crossref_raw_path=crossref_dump,
        openalex_raw_path=openalex_dump,
        db_path=db_path,
        log_path=log_path,
    )

    assert result["normalized_count"] == 2  # 1 crossref + 1 openalex
    assert result["saved_count"] == 1  # Deduplicated to 1
    saved = normalize.load_existing_db(db_path, log_path=log_path)
    assert len(saved) == 1
    # Crossref was normalized first, so it's the existing one
    assert saved[0].source_api == "crossref"
    assert saved[0].doi == "10.1080/19376529.2026.1234567"

