from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
AUDITED_2026_05_20_RSS_ENABLED = {
    "radiomorphoses",
    "radio_fanch",
    "les_radios_libres",
    "la_radio_du_futur",
    "meccsa_radio_audio_studies",
}
AUDITED_2026_05_20_RSS_DECLARED = {
    *AUDITED_2026_05_20_RSS_ENABLED,
    "nieman_storyboard",
    "la_lettre_pro",
    "transom",
}
PRIORITY_CROSSREF_CANDIDATES = {
    "radio_journal": ["1476-4504", "2040-1388"],
    "sound_studies_journal": ["2055-1940", "2055-1959"],
    "resonance_journal": ["2688-867X"],
}
PRIORITY_OPENALEX_CANDIDATES = {
    "journal_sonic_studies_venue": "2212-6252",
}
V2_SOURCE_IDS = {
    "journal_radio_audio_media",
    "sounding_out_blog",
    "meccsa_radio_audio_studies",
}
# Nouvelles revues ajoutées au Prompt 1 (2026-05-25)
NEW_CROSSREF_JOURNALS_2026_05_25 = {
    "organised_sound": ["1355-7718", "1469-8153"],
    "sound_effects_journal": ["1904-4566", "1904-4577"],
}
NEW_OPENALEX_VENUE_PROFILES_2026_05_25 = {
    "popular_communication_filtered": "1540-5710",
    "convergence_filtered": "1748-7382",
    "media_culture_society_filtered": "1460-3675",
    "feminist_media_studies_filtered": "1471-5902",
    "participations_filtered": "1749-8716",
    "critical_studies_tv_filtered": "2040-0616",
    "view_journal_filtered": "2213-0969",
    "reseaux_filtered": "1777-5809",
    "questions_communication_filtered": "1633-5961",
    "etudes_communication_filtered": "1968-0473",
    "volume_filtered": "1950-568X",
    "transposition_filtered": "2110-6134",
    "societes_representations_filtered": "1262-2966",
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
    assert sources["crossref"]["enabled"] is True
    assert sources["crossref"]["mailto_env"] == "CROSSREF_MAILTO"
    assert sources["crossref"]["rows"] <= 20
    assert sources["crossref"]["polite_delay_seconds"] >= 1
    assert sources["crossref"]["journals"][0]["issn"] == ["1937-6529", "1937-6537"]
    assert sources["openalex"]["enabled"] is True
    assert sources["openalex"]["mailto_env"] == "OPENALEX_MAILTO"
    assert sources["openalex"]["per_page"] <= 20
    assert sources["openalex"]["max_pages_per_profile"] == 1
    assert "abstract_inverted_index" in sources["openalex"]["forbidden_select"]
    assert "radio frequency" in sources["openalex"]["noise_exclusions"]


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

    la_lettre_pro = rss_sources["la_lettre_pro"]
    assert la_lettre_pro["enabled"] is False
    assert la_lettre_pro["audit_date"] == "2026-05-20"
    assert la_lettre_pro["legal_status"].startswith("VALIDÉ")

    transom = rss_sources["transom"]
    assert transom["enabled"] is False
    assert transom["audit_date"] == "2026-05-20"
    assert transom["legal_status"].startswith("VALIDÉ")

    nieman_storyboard = rss_sources["nieman_storyboard"]
    assert nieman_storyboard["enabled"] is False
    assert nieman_storyboard["audit_date"] == "2026-05-20"
    assert nieman_storyboard["legal_status"].startswith("VALIDÉ")


def test_priority_venues_are_configured_as_enabled_candidates_without_v2_duplicates():
    sources = load_yaml("sources.yaml")
    rss_source_ids = [source["id"] for source in sources["rss_atom"]]
    crossref_journals = {journal["id"]: journal for journal in sources["crossref"]["journals"]}
    openalex_profiles = {profile["id"]: profile for profile in sources["openalex"]["profiles"]}

    for source_id in V2_SOURCE_IDS:
        assert rss_source_ids.count(source_id) == 1

    for journal_id, issns in PRIORITY_CROSSREF_CANDIDATES.items():
        journal = crossref_journals[journal_id]
        assert journal["enabled"] is True
        assert journal["issn"] == issns
        assert journal["audit_date"] == "2026-05-21"
        assert journal["legal_status"].startswith("CANDIDAT")
        assert "academic_watch" in journal["tags"]

    for profile_id, issn in PRIORITY_OPENALEX_CANDIDATES.items():
        profile = openalex_profiles[profile_id]
        assert profile["enabled"] is True
        assert profile["filters"]["primary_location.source.issn"] == issn
        assert profile["sort"] == "publication_date:desc"
        assert "academic_watch" in profile["tags"]


def test_scoring_references_keyword_categories():
    keywords = load_yaml("keywords.yaml")
    scoring = load_yaml("scoring.yaml")

    keyword_categories = set(keywords) - {"version"}
    weighted_categories = set(scoring["weights"])

    assert keyword_categories == weighted_categories
    assert scoring["thresholds"]["to_read"]["gte"] == 6
    assert scoring["thresholds"]["candidate"]["gte"] == 2
    assert scoring["thresholds"]["ignored"]["lt"] == 2
    assert set(scoring["fields"]) == {"title", "abstract", "tags", "source_name"}


def test_academic_source_floor_is_configured():
    scoring = load_yaml("scoring.yaml")
    floor = scoring.get("academic_source_floor")
    assert isinstance(floor, dict), "academic_source_floor doit être un dict dans scoring.yaml"
    assert set(floor["source_apis"]) == {"crossref", "openalex", "hal"}
    assert floor["min_score"] >= 0


def test_new_crossref_journals_2026_05_25_are_configured():
    sources = load_yaml("sources.yaml")
    crossref_journals = {journal["id"]: journal for journal in sources["crossref"]["journals"]}

    for journal_id, issns in NEW_CROSSREF_JOURNALS_2026_05_25.items():
        journal = crossref_journals[journal_id]
        assert journal["enabled"] is True
        assert journal["issn"] == issns
        assert journal["audit_date"] == "2026-05-25"
        assert journal["legal_status"].startswith("CANDIDAT")
        assert "academic_watch" in journal["tags"]


def test_new_openalex_venue_profiles_2026_05_25_are_configured():
    sources = load_yaml("sources.yaml")
    openalex_profiles = {profile["id"]: profile for profile in sources["openalex"]["profiles"]}

    for profile_id, issn in NEW_OPENALEX_VENUE_PROFILES_2026_05_25.items():
        profile = openalex_profiles[profile_id]
        assert profile.get("enabled") is not False, f"{profile_id} ne doit pas être disabled"
        assert profile["filters"]["primary_location.source.issn"] == issn
        assert profile.get("search"), f"{profile_id} doit avoir un filtre mots-clés (search)"
        assert profile["sort"] == "publication_date:desc"
        assert "academic_watch" in profile["tags"]


def test_la_lettre_pro_is_definitively_disabled():
    sources = load_yaml("sources.yaml")
    rss_sources = {source["id"]: source for source in sources["rss_atom"]}
    assert rss_sources["la_lettre_pro"]["enabled"] is False
