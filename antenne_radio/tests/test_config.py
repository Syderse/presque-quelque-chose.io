from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
AUDITED_2026_05_20_RSS_ENABLED = {
    "radiomorphoses",
    "radio_fanch",
    "les_radios_libres",
    "la_radio_du_futur",
    "la_lettre_pro",
    "meccsa_radio_audio_studies",
    "nieman_storyboard",
}
AUDITED_2026_05_20_RSS_DECLARED = {
    *AUDITED_2026_05_20_RSS_ENABLED,
    "transom",
}


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
    assert sources["crossref"]["enabled"] is False
    assert sources["crossref"]["mailto_env"] == "CROSSREF_MAILTO"
    assert sources["crossref"]["journals"][0]["issn"] == ["1937-6529", "1937-6537"]


def test_legal_audit_2026_05_20_rss_sources_are_configured():
    sources = load_yaml("sources.yaml")
    rss_sources = {source["id"]: source for source in sources["rss_atom"]}

    assert AUDITED_2026_05_20_RSS_DECLARED <= set(rss_sources)
    for source_id in AUDITED_2026_05_20_RSS_ENABLED:
        source = rss_sources[source_id]
        assert source["enabled"] is True
        assert source["audit_date"] == "2026-05-20"
        assert source["legal_status"].startswith("VALIDÉ")
        assert source["tags"]
        assert source["categories"]

    transom = rss_sources["transom"]
    assert transom["enabled"] is False
    assert transom["audit_date"] == "2026-05-20"
    assert transom["legal_status"].startswith("VALIDÉ")


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
