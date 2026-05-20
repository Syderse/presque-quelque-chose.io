from datetime import datetime, timezone
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import (  # noqa: E402
    RadioWatchItem,
    SourceType,
    WatchStatus,
    generate_stable_id,
)


def minimal_item_payload():
    return {
        "id": "manual:test",
        "title": "Radio archives and everyday listening",
        "source_name": "Example source",
        "source_type": SourceType.journal_article,
        "language": "en",
        "status": WatchStatus.new,
        "discovered_at": datetime(2026, 5, 18, tzinfo=timezone.utc),
    }


def test_minimal_item_is_valid():
    item = RadioWatchItem(**minimal_item_payload())

    assert item.title == "Radio archives and everyday listening"
    assert item.source_type is SourceType.journal_article
    assert item.status is WatchStatus.new
    assert item.authors == []


def test_stable_id_prefers_doi():
    from_doi = generate_stable_id(
        doi="https://doi.org/10.1234/RADIO.2026",
        url="https://example.org/ignored",
    )
    from_normalized_doi = generate_stable_id(doi="doi:10.1234/radio.2026")

    assert from_doi == from_normalized_doi
    assert from_doi.startswith("doi:")


def test_stable_id_uses_url_when_doi_is_missing():
    first = generate_stable_id(
        url="HTTP://Example.org/watch/item/?utm_source=newsletter&b=2&a=1#section"
    )
    second = generate_stable_id(url="http://example.org/watch/item?a=1&b=2")

    assert first == second
    assert first.startswith("url:")


def test_item_without_title_is_rejected():
    payload = minimal_item_payload()
    payload.pop("title")

    with pytest.raises(ValidationError):
        RadioWatchItem(**payload)
