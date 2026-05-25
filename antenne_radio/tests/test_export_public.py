import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import SourceType, WatchStatus  # noqa: E402
from scripts.export import export_public  # noqa: E402


GENERATED_AT = datetime(2026, 5, 19, 12, 0, tzinfo=timezone.utc)

EDITORIAL_ITEM_KEYS = {
    "id",
    "title",
    "url",
    "doi",
    "published_at",
    "source_name",
    "source_type",
    "language",
    "source_family",
    "attribution_id",
}
BIBLIOGRAPHIC_ITEM_KEYS = EDITORIAL_ITEM_KEYS | {"authors", "container_title", "item_type"}
# Alias pour les tests qui vérifient la whitelist complète (13 clés)
PUBLIC_ITEM_KEYS = BIBLIOGRAPHIC_ITEM_KEYS

FORBIDDEN_KEYS = {
    "raw",
    "abstract",
    "logs",
    "notes",
    "status",
    "relevance_score",
    "score_explanation",
    "keywords_matched",
    "negative_keywords_matched",
    "discovered_at",
    "source_feed",
    "source_api",
    "title_original",
    "errors",
    "raw_responses",
    "tags",
}


def item_payload(**overrides):
    payload = {
        "id": "manual:test",
        "title": "Radio libre et archives",
        "source_name": "Radio Survivor",
        "source_type": SourceType.blog.value,
        "language": "fr",
        "status": WatchStatus.to_read.value,
        "discovered_at": GENERATED_AT.isoformat(),
        "authors": ["A. Fixture"],
        "published_at": GENERATED_AT.isoformat(),
        "url": "https://example.org/radio",
        "doi": "10.1234/radio.2026",
        "abstract": "<p>Un résumé privé.</p>",
        "tags": ["radio"],
        "keywords_matched": ["radio libre"],
        "negative_keywords_matched": [],
        "relevance_score": 8,
        "score_explanation": "+6 radio libre dans title; score final 8",
        "source_feed": "https://example.org/feed.xml",
        "source_api": "rss",
        "title_original": "Radio libre et archives",
        "raw": {"entry": "private"},
    }
    payload.update(overrides)
    return payload


def write_db(path, items):
    path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def forbidden_keys(value):
    found = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_KEYS:
                found.add(key)
            found.update(forbidden_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(forbidden_keys(nested))
    return found


def test_public_export_creates_whitelisted_json(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload()])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )

    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["items_exported"] == 1
    assert exported["schema_version"] == "antenne-radio-public-v0"
    assert exported["generated_at"] == "2026-05-19T12:00:00Z"
    assert exported["item_count"] == 1
    # Radio Survivor = source éditoriale (RSS) → 10 clés, pas d'auteurs/revue/type biblio
    assert set(exported["items"][0]) == EDITORIAL_ITEM_KEYS
    assert exported["items"][0] == {
        "attribution_id": "radio_survivor",
        "doi": "10.1234/radio.2026",
        "id": "manual:test",
        "language": "fr",
        "published_at": "2026-05-19T12:00:00Z",
        "source_family": "rss",
        "source_name": "Radio Survivor",
        "source_type": "blog",
        "title": "Radio libre et archives",
        "url": "https://example.org/radio",
    }


def test_public_export_excludes_private_fields_recursively(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload()])

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert forbidden_keys(exported) == set()
    content = output_path.read_text(encoding="utf-8")
    assert "Un résumé privé" not in content
    assert "private" not in content
    assert "score final" not in content
    assert "https://example.org/feed.xml" not in content


def test_public_export_schema_stays_whitelisted_for_merged_private_metadata(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:merged",
                authors=["Ada Radio"],
                tags=["Crossref"],
                abstract="Private Crossref abstract",
                raw={
                    "entry": "private",
                    "_merged_sources": [
                        {
                            "source_name": "Crossref",
                            "source_api": "crossref",
                            "doi": "10.1234/radio.2026",
                        }
                    ],
                },
            )
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]
    content = output_path.read_text(encoding="utf-8")

    # Radio Survivor = éditoriale → 10 clés, pas d'auteurs
    assert set(public_item) == EDITORIAL_ITEM_KEYS
    assert forbidden_keys(exported) == set()
    assert "Private Crossref abstract" not in content
    assert "Ada Radio" not in content
    assert "_merged_sources" not in content


def test_public_export_keeps_only_public_statuses_and_audited_sources(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(id="manual:to-read", status=WatchStatus.to_read.value),
            item_payload(id="manual:candidate", status=WatchStatus.candidate.value),
            item_payload(id="manual:exported", status=WatchStatus.exported.value),
            item_payload(id="manual:ignored", status=WatchStatus.ignored.value),
            item_payload(id="manual:new", status=WatchStatus.new.value),
            item_payload(id="manual:crossref", source_name="Crossref radio journals", source_api="crossref"),
        ],
    )

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["items_exported"] == 3
    assert {item["id"] for item in exported["items"]} == {
        "manual:to-read",
        "manual:candidate",
        "manual:exported",
    }


def test_public_export_adds_source_attributions(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(id="manual:rss", source_name="Sounding Out!"),
            item_payload(
                id="manual:hal",
                source_name="HAL radio studies search",
                source_type=SourceType.journal_article.value,
                source_api="hal",
            ),
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert {source["attribution_id"] for source in exported["sources"]} == {"hal", "sounding_out"}
    assert {item["attribution_id"] for item in exported["items"]} == {"hal", "sounding_out"}
    assert {item["source_name"] for item in exported["items"]} == {"HAL open archive", "Sounding Out!"}
    assert all(source["attribution_text"].startswith("Source: ") for source in exported["sources"])


@pytest.mark.parametrize(
    ("source_name", "attribution_id", "public_name"),
    [
        ("Radiomorphoses", "radiomorphoses", "Radiomorphoses / OpenEdition Journals"),
        ("Radio Fañch", "radio_fanch", "Radio Fañch"),
        ("Les Radios Libres", "les_radios_libres", "Les Radios Libres"),
        ("La Radio du Futur", "la_radio_du_futur", "La Radio du Futur"),
        ("La Lettre Pro de la Radio", "la_lettre_pro", "La Lettre Pro de la Radio & du Podcast"),
        ("MeCCSA Radio & Audio Studies", "meccsa_radio_audio_studies", "MeCCSA Radio and Audio Studies"),
        ("Nieman Storyboard", "nieman_storyboard", "Nieman Storyboard"),
        ("Transom", "transom", "Transom"),
    ],
)
def test_public_export_maps_legal_audit_2026_05_20_sources(
    tmp_path,
    source_name,
    attribution_id,
    public_name,
):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(source_name=source_name)])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["items_exported"] == 1
    assert exported["items"][0]["attribution_id"] == attribution_id
    assert exported["items"][0]["source_name"] == public_name
    assert exported["sources"][0]["attribution_id"] == attribution_id


@pytest.mark.parametrize(
    ("source_name", "attribution_id", "public_name", "source_family"),
    [
        (
            "Radio Journal: International Studies in Broadcast & Audio Media",
            "radio_journal",
            "Radio Journal: International Studies in Broadcast & Audio Media",
            "crossref",
        ),
        (
            "Radio Journal:International Studies in Broadcast & Audio Media",
            "radio_journal",
            "Radio Journal: International Studies in Broadcast & Audio Media",
            "crossref",
        ),
        (
            "Sound Studies",
            "sound_studies_journal",
            "Sound Studies: An Interdisciplinary Journal",
            "crossref",
        ),
        (
            "Journal of Sonic Studies",
            "journal_sonic_studies",
            "Journal of Sonic Studies",
            "openalex",
        ),
        (
            "Resonance The Journal of Sound and Culture",
            "resonance_journal",
            "Resonance: The Journal of Sound and Culture",
            "crossref",
        ),
    ],
)
def test_public_export_maps_priority_venue_candidates(
    tmp_path,
    source_name,
    attribution_id,
    public_name,
    source_family,
):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(source_name=source_name, source_type=SourceType.journal_article.value)])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]

    assert result["items_exported"] == 1
    # Toutes les venues prioritaires sont bibliographiques (crossref ou openalex)
    assert set(public_item) == BIBLIOGRAPHIC_ITEM_KEYS
    assert public_item["attribution_id"] == attribution_id
    assert public_item["source_name"] == public_name
    assert public_item["source_family"] == source_family
    assert "authors" in public_item
    assert "container_title" in public_item
    assert "item_type" in public_item
    assert exported["sources"][0]["attribution_id"] == attribution_id
    assert forbidden_keys(exported) == set()


def test_public_export_uses_doi_url_fallback(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(url=None, doi="10.1234/radio.2026")])

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert exported["items"][0]["url"] == "https://doi.org/10.1234/radio.2026"


def test_public_export_skips_items_without_public_link(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(url=None, doi=None)])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert result["items_exported"] == 0
    assert exported["items"] == []
    assert exported["sources"] == []


def test_public_export_does_not_modify_db(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    items = [item_payload()]
    write_db(db_path, items)

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )

    assert json.loads(db_path.read_text(encoding="utf-8")) == items


def test_openalex_item_export_public_without_score_or_abstract(tmp_path):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:openalex",
                source_name="OpenAlex",
                source_api="openalex",
                source_type=SourceType.journal_article.value,
                abstract="Private OpenAlex abstract that must not leak",
                relevance_score=15.5,
                score_explanation="+8 radio dans title; score final 15.5",
                keywords_matched=["radio", "community radio"],
                negative_keywords_matched=[],
                tags=["radio studies", "broadcasting"],
                authors=["Private Author"],
                raw={
                    "id": "https://openalex.org/W999",
                    "abstract_inverted_index": {"This": [0], "is": [1], "private": [2]},
                    "authorships": [{"author": {"display_name": "Private Author"}}],
                    "relevance_score": 42.5,
                },
            )
        ],
    )

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    content = output_path.read_text(encoding="utf-8")

    assert result["items_exported"] == 1
    # OpenAlex = source bibliographique → 13 clés avec auteurs, container_title, item_type
    assert set(exported["items"][0]) == BIBLIOGRAPHIC_ITEM_KEYS
    assert exported["items"][0]["attribution_id"] == "openalex"
    assert exported["items"][0]["source_name"] == "OpenAlex"
    assert exported["items"][0]["source_family"] == "openalex"
    assert "authors" in exported["items"][0]
    assert "container_title" in exported["items"][0]
    assert "item_type" in exported["items"][0]
    assert forbidden_keys(exported) == set()
    # Champs privés stricts : jamais dans l'index public
    assert "Private OpenAlex abstract" not in content
    assert "abstract_inverted_index" not in content
    assert "authorships" not in content
    assert "relevance_score" not in content
    assert "score_explanation" not in content
    assert "keywords_matched" not in content
    assert "score final" not in content


def test_openalex_attribution_mapping():
    assert "OpenAlex" in export_public.ATTRIBUTION_BY_SOURCE_NAME
    assert export_public.ATTRIBUTION_BY_SOURCE_NAME["OpenAlex"] == "openalex"
    assert "openalex" in export_public.AUDITED_ATTRIBUTIONS
    assert export_public.AUDITED_ATTRIBUTIONS["openalex"]["source_family"] == "openalex"
    assert export_public.AUDITED_ATTRIBUTIONS["openalex"]["url"] == "https://openalex.org/"


@pytest.mark.parametrize(
    ("source_name", "attribution_id", "source_family"),
    [
        ("Organised Sound", "organised_sound", "crossref"),
        ("SoundEffects", "sound_effects_journal", "crossref"),
        ("SoundEffects: An Interdisciplinary Journal of Sound and Sound Experience", "sound_effects_journal", "crossref"),
        ("Popular Communication", "popular_communication", "openalex"),
        ("Convergence", "convergence_journal", "openalex"),
        ("Convergence: The International Journal of Research into New Media Technologies", "convergence_journal", "openalex"),
        ("Media, Culture & Society", "media_culture_society", "openalex"),
        ("Feminist Media Studies", "feminist_media_studies", "openalex"),
        ("Participations", "participations_journal", "openalex"),
        ("Participations: Journal of Audience & Reception Studies", "participations_journal", "openalex"),
        ("Critical Studies in Television", "critical_studies_tv", "openalex"),
        ("VIEW Journal of European Television History and Culture", "view_journal", "openalex"),
        ("Réseaux", "reseaux", "openalex"),
        ("Réseaux (Paris)", "reseaux", "openalex"),
        ("Questions de communication", "questions_communication", "openalex"),
        ("Études de communication", "etudes_communication", "openalex"),
        ("Volume!", "volume_journal", "openalex"),
        ("Transposition", "transposition_journal", "openalex"),
        ("Sociétés & Représentations", "societes_representations", "openalex"),
    ],
)
def test_public_export_maps_new_2026_05_25_sources(
    tmp_path,
    source_name,
    attribution_id,
    source_family,
):
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(db_path, [item_payload(source_name=source_name, source_type=SourceType.journal_article.value)])

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]

    assert result["items_exported"] == 1
    # Toutes ces nouvelles sources sont bibliographiques (crossref ou openalex)
    assert set(public_item) == BIBLIOGRAPHIC_ITEM_KEYS
    assert public_item["attribution_id"] == attribution_id
    assert public_item["source_family"] == source_family
    assert "authors" in public_item
    assert "container_title" in public_item
    assert "item_type" in public_item
    assert exported["sources"][0]["attribution_id"] == attribution_id
    assert forbidden_keys(exported) == set()


def test_new_crossref_attribution_integrity():
    for attribution_id in ("organised_sound", "sound_effects_journal"):
        assert attribution_id in export_public.AUDITED_ATTRIBUTIONS
        assert export_public.AUDITED_ATTRIBUTIONS[attribution_id]["source_family"] == "crossref"

def test_new_openalex_attribution_integrity():
    new_openalex_ids = (
        "popular_communication", "convergence_journal", "media_culture_society",
        "feminist_media_studies", "participations_journal", "critical_studies_tv",
        "view_journal", "reseaux", "questions_communication", "etudes_communication",
        "volume_journal", "transposition_journal", "societes_representations",
    )
    for attribution_id in new_openalex_ids:
        assert attribution_id in export_public.AUDITED_ATTRIBUTIONS, f"Attribution manquante : {attribution_id}"
        assert export_public.AUDITED_ATTRIBUTIONS[attribution_id]["source_family"] == "openalex"


def test_public_export_anti_leak_reinforced(tmp_path):
    """Reinforced anti-leak: abstract_inverted_index, authorships, and all forbidden keys must never appear."""
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:leak-check",
                raw={
                    "abstract_inverted_index": {"hidden": [0, 1]},
                    "authorships": [{"author": {"display_name": "Leak Author"}}],
                    "_merged_sources": [{"source_api": "openalex"}],
                },
                abstract="Leak abstract content",
                authors=["Leak Author"],
                tags=["leak-tag"],
                relevance_score=9.0,
                score_explanation="private explanation",
                keywords_matched=["radio"],
                negative_keywords_matched=["wireless"],
            )
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    content = output_path.read_text(encoding="utf-8")

    assert forbidden_keys(exported) == set()
    assert "abstract_inverted_index" not in content
    assert "authorships" not in content
    # Source éditoriale (Radio Survivor) → auteurs absents du public même s'ils sont en base
    assert "Leak Author" not in content
    assert "Leak abstract content" not in content
    assert "leak-tag" not in content
    assert "private explanation" not in content
    assert "_merged_sources" not in content


def test_bibliographic_item_has_enriched_keys(tmp_path):
    """Items bibliographiques (crossref/openalex/hal) : 13 clés avec auteurs, revue et type."""
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:biblio",
                source_name="Sound Studies",
                source_type=SourceType.journal_article.value,
                authors=["Alice Chercheure", "Bob Étude"],
            )
        ],
    )

    result = export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]

    assert result["items_exported"] == 1
    assert set(public_item) == BIBLIOGRAPHIC_ITEM_KEYS
    assert public_item["authors"] == ["Alice Chercheure", "Bob Étude"]
    assert public_item["item_type"] == "journal_article"
    assert "container_title" in public_item
    assert forbidden_keys(exported) == set()


def test_editorial_item_has_no_bibliographic_keys(tmp_path):
    """Items éditoriaux (RSS) : 10 clés exactement, sans auteurs, revue ni type biblio."""
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:editorial",
                source_name="Radio Survivor",
                authors=["Ghost Author"],
            )
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]
    content = output_path.read_text(encoding="utf-8")

    assert set(public_item) == EDITORIAL_ITEM_KEYS
    assert "authors" not in public_item
    assert "container_title" not in public_item
    assert "item_type" not in public_item
    assert "Ghost Author" not in content


def test_authors_email_cleaning(tmp_path):
    """Les adresses e-mail accidentellement capturées dans les noms d'auteurs sont retirées."""
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:email-clean",
                source_name="Sound Studies",
                source_type=SourceType.journal_article.value,
                authors=[
                    "Alice Chercheure alice.chercheure@univ.fr",
                    "Bob Étude <bob@research.org>",
                    "Carol Sans Email",
                ],
            )
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    content = output_path.read_text(encoding="utf-8")
    public_authors = exported["items"][0]["authors"]

    assert "@" not in content
    assert "alice.chercheure@univ.fr" not in content
    assert "bob@research.org" not in content
    assert "Carol Sans Email" in content
    # Les noms nettoyés sont bien présents (sans le mail)
    assert any("Alice Chercheure" in a for a in public_authors)
    assert any("Bob Étude" in a for a in public_authors)
    assert "Carol Sans Email" in public_authors


def test_hal_item_has_bibliographic_keys(tmp_path):
    """Items HAL : source bibliographique → 13 clés."""
    db_path = tmp_path / "db.json"
    output_path = tmp_path / "public" / "index.json"
    write_db(
        db_path,
        [
            item_payload(
                id="manual:hal-biblio",
                source_name="HAL radio studies search",
                source_type=SourceType.journal_article.value,
                authors=["Dupont Aline"],
            )
        ],
    )

    export_public.export_public_json(
        db_path=db_path,
        output_path=output_path,
        generated_at=GENERATED_AT,
    )
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    public_item = exported["items"][0]

    assert set(public_item) == BIBLIOGRAPHIC_ITEM_KEYS
    assert public_item["source_family"] == "hal"
    assert public_item["authors"] == ["Dupont Aline"]
    assert "container_title" in public_item
    assert "item_type" in public_item
    assert forbidden_keys(exported) == set()


def test_public_export_whitelist_has_exactly_13_keys():
    """La whitelist complète (sources bibliographiques) comporte exactement 13 clés."""
    assert len(export_public.PUBLIC_ITEM_KEYS) == 13
    assert len(export_public.EDITORIAL_ITEM_KEYS) == 10
    assert len(export_public.BIBLIOGRAPHIC_ITEM_KEYS) == 13
    assert export_public.BIBLIOGRAPHIC_SOURCE_FAMILIES == {"crossref", "openalex", "hal"}
