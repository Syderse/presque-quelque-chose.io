import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ingest import ingest_rss  # noqa: E402


FIXTURE = ROOT / "tests" / "fixtures" / "sample_rss.xml"


def test_selects_only_enabled_rss_sources():
    config = {
        "sources": [
            {"name": "Enabled RSS", "enabled": True, "type": "rss", "url": "https://example.org/rss"},
            {"name": "Disabled RSS", "enabled": False, "type": "rss", "url": "https://example.org/off"},
            {"name": "Enabled HAL", "enabled": True, "type": "hal", "url": "https://example.org/hal"},
        ]
    }

    sources = ingest_rss.select_rss_sources(config)

    assert [source["name"] for source in sources] == ["Enabled RSS"]


def test_local_fixture_parses_without_network(tmp_path):
    source = {
        "id": "fixture",
        "name": "Fixture Radio",
        "enabled": True,
        "type": "rss",
        "url": str(FIXTURE),
    }

    payload = ingest_rss.ingest_sources([source], log_path=tmp_path / "api.log")

    assert payload["entry_count"] == 1
    entry = payload["entries"][0]
    assert entry["title"] == "Community radio archives open again"
    assert entry["link"] == "https://example.org/radio/archive-open"
    assert entry["source_name"] == "Fixture Radio"


def test_cli_ingest_writes_raw_output_only(tmp_path):
    config_path = tmp_path / "sources.yaml"
    output_path = tmp_path / "data" / "raw" / "rss_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    config = {
        "version": 0.1,
        "sources": [
            {
                "id": "fixture",
                "name": "Fixture Radio",
                "enabled": True,
                "type": "rss",
                "url": str(FIXTURE),
            }
        ],
    }
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    payload = ingest_rss.ingest_rss(
        config_path=config_path,
        output_path=output_path,
        log_path=tmp_path / "data" / "logs" / "api.log",
    )

    assert payload["entry_count"] == 1
    assert output_path.exists()
    assert not db_path.exists()


def test_source_error_is_logged_and_other_sources_continue(monkeypatch, tmp_path):
    real_parse = ingest_rss.feedparser.parse

    def fake_parse(value):
        if value == "https://example.org/broken.xml":
            raise RuntimeError("fixture failure")
        return real_parse(value)

    monkeypatch.setattr(ingest_rss.feedparser, "parse", fake_parse)
    sources = [
        {
            "id": "broken",
            "name": "Broken Feed",
            "enabled": True,
            "type": "rss",
            "url": "https://example.org/broken.xml",
        },
        {
            "id": "fixture",
            "name": "Fixture Radio",
            "enabled": True,
            "type": "rss",
            "url": str(FIXTURE),
        },
    ]
    log_path = tmp_path / "api.log"

    payload = ingest_rss.ingest_sources(sources, log_path=log_path)

    assert payload["entry_count"] == 1
    assert payload["errors"] == [
        {
            "source_name": "Broken Feed",
            "source_feed": "https://example.org/broken.xml",
            "error": "fixture failure",
        }
    ]
    assert "RSS source Broken Feed failed: fixture failure" in log_path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "config",
    [
        {"rss_atom": [{"name": "Kind RSS", "enabled": True, "kind": "rss", "url": "https://example.org/rss"}]},
        {"rss_atom": [{"name": "Kind Atom", "enabled": True, "kind": "atom", "url": "https://example.org/atom"}]},
    ],
)
def test_existing_rss_atom_config_shape_is_supported(config):
    sources = ingest_rss.select_rss_sources(config)

    assert len(sources) == 1
