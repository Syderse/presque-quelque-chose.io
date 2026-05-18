from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"


def load_yaml(name: str):
    with (CONFIG / name).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_config_files_are_valid_yaml():
    for filename in ("sources.yaml", "keywords.yaml", "scoring.yaml"):
        assert isinstance(load_yaml(filename), dict)


def test_sources_keep_enabled_flags():
    sources = load_yaml("sources.yaml")

    assert "rss_atom" in sources
    assert all("enabled" in source for source in sources["rss_atom"])
    assert sources["hal"]["enabled"] is True
    assert sources["hal"]["limit"] == 20


def test_scoring_references_keyword_categories():
    keywords = load_yaml("keywords.yaml")
    scoring = load_yaml("scoring.yaml")

    keyword_categories = set(keywords) - {"version"}
    weighted_categories = set(scoring["weights"])

    assert keyword_categories == weighted_categories
    assert scoring["thresholds"]["to_read"]["gte"] == 6
    assert scoring["thresholds"]["candidate"]["gte"] == 2
    assert scoring["thresholds"]["ignored"]["lt"] == 2
    assert set(scoring["fields"]) == {"title", "abstract", "tags"}
