import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core import scoring  # noqa: E402
from scripts.core.models import SourceType, WatchStatus  # noqa: E402


KEYWORDS = scoring.load_yaml(ROOT / "config" / "keywords.yaml")
SCORING = scoring.load_yaml(ROOT / "config" / "scoring.yaml")
DISCOVERED_AT = datetime(2026, 5, 18, 12, 0, tzinfo=timezone.utc).isoformat()


def item_payload(**overrides):
    payload = {
        "id": "manual:test",
        "title": "Untitled radio watch item",
        "source_name": "Fixture source",
        "source_type": SourceType.journal_article.value,
        "language": "fr",
        "status": WatchStatus.new.value,
        "discovered_at": DISCOVERED_AT,
        "abstract": None,
        "tags": [],
        "raw": {},
    }
    payload.update(overrides)
    return payload


def score_payload(payload):
    item = scoring.RadioWatchItem(**payload)
    return scoring.score_item(item, KEYWORDS, SCORING)


def test_very_relevant_item_becomes_to_read():
    scored = score_payload(
        item_payload(
            title="Radio libre et archives sonores",
            abstract="Une enquête sur Guattari, l'écoute et la psychothérapie institutionnelle.",
            tags=["community radio"],
        )
    )

    assert scored.status is WatchStatus.to_read
    assert scored.relevance_score >= 6
    assert "radio libre" in scored.keywords_matched
    assert scored.negative_keywords_matched == []


def test_social_science_radio_item_stays_to_read():
    scored = score_payload(
        item_payload(
            title="Community radio and rural participation",
            abstract="A social science article about broadcasting, identity, and local media participation.",
        )
    )

    assert scored.status is WatchStatus.to_read
    assert scored.relevance_score >= 6
    assert "community radio" in scored.keywords_matched
    assert scored.negative_keywords_matched == []


def test_podcast_and_radio_libre_item_is_favored():
    scored = score_payload(
        item_payload(
            title="Radio libre podcast archives",
            abstract="A podcasting project about pirate radio and community radio memory.",
        )
    )

    assert scored.status is WatchStatus.to_read
    assert scored.relevance_score >= 6
    assert "radio libre" in scored.keywords_matched
    assert "podcast" in scored.keywords_matched
    assert scored.negative_keywords_matched == []


def test_radiology_noise_is_ignored():
    scored = score_payload(
        item_payload(
            title="Radiology and radiofrequency imaging systems",
            abstract="Medical imaging methods for RF engineering and antenna design.",
            tags=["radiologie"],
        )
    )

    assert scored.status is WatchStatus.ignored
    assert scored.relevance_score < 2
    assert "radiology" in scored.negative_keywords_matched
    assert "radiofrequency" in scored.negative_keywords_matched
    assert "radio" not in scored.keywords_matched


def test_telecom_radio_noise_is_ignored():
    scored = score_payload(
        item_payload(
            title="Cognitive radio networks for 6G spectrum sensing",
            abstract="Dynamic spectrum access in wireless networks for LoRaWAN and V2X systems.",
            tags=["cognitive radio", "telecommunications"],
        )
    )

    assert scored.status is WatchStatus.ignored
    assert scored.relevance_score < 2
    assert "radio" in scored.keywords_matched
    assert "cognitive radio" in scored.negative_keywords_matched
    assert "spectrum sensing" in scored.negative_keywords_matched


def test_ambiguous_radio_technical_item_stays_candidate():
    scored = score_payload(
        item_payload(
            title="Review of Radio Counter-Counter Unmanned Aerial Systems",
            abstract="A report on radio practices in contemporary conflict.",
        )
    )

    assert scored.status is WatchStatus.candidate
    assert 2 <= scored.relevance_score < 6
    assert "radio" in scored.keywords_matched
    assert "unmanned aerial systems" in scored.negative_keywords_matched


def test_light_positive_match_becomes_candidate():
    # Titre peu chargé en mots-clés → un seul match → score dans [2, 6)
    scored = score_payload(
        item_payload(
            title="Court podcast hebdomadaire",
            abstract=None,
        )
    )

    assert scored.status is WatchStatus.candidate
    assert 2 <= scored.relevance_score < 6
    assert "podcast" in scored.keywords_matched


def test_score_explanation_is_not_empty():
    scored = score_payload(item_payload(title="Note sans mot-clé direct"))

    assert scored.score_explanation
    assert "score final" in scored.score_explanation


def test_score_db_writes_only_new_items(tmp_path):
    db_path = tmp_path / "db.json"
    exported = item_payload(
        id="manual:exported",
        title="Radio libre déjà exportée",
        status=WatchStatus.exported.value,
        relevance_score=None,
        score_explanation=None,
    )
    new_item = item_payload(id="manual:new", title="Community radio archive")
    db_path.write_text(json.dumps([exported, new_item]), encoding="utf-8")

    result = scoring.score_db(db_path=db_path, keywords_path=ROOT / "config" / "keywords.yaml", scoring_path=ROOT / "config" / "scoring.yaml")
    saved = json.loads(db_path.read_text(encoding="utf-8"))

    assert result["scored_count"] == 1
    assert saved[0] == exported
    assert saved[1]["status"] == WatchStatus.to_read.value
    assert saved[1]["score_explanation"]


def test_radio_audio_studies_item_scores_high():
    scored = score_payload(
        item_payload(
            title="Radio studies in the digital age",
            abstract="An analysis of broadcasting history and radio journalism practices.",
            tags=["radio studies", "broadcasting"],
        )
    )

    assert scored.status is WatchStatus.to_read
    assert scored.relevance_score >= 6
    assert "radio studies" in scored.keywords_matched
    assert scored.negative_keywords_matched == []


def test_sound_studies_item_scores_positive():
    scored = score_payload(
        item_payload(
            title="Sonic geography and auditory culture",
            abstract="Exploring soundscapes and acoustic ecology in urban settings.",
            tags=["sound studies"],
        )
    )

    assert scored.status in {WatchStatus.to_read, WatchStatus.candidate}
    assert scored.relevance_score >= 2
    assert any(kw in scored.keywords_matched for kw in ["sound studies", "sonic", "auditory culture", "soundscape", "acoustic ecology", "sonic geography"])
    assert scored.negative_keywords_matched == []


def test_telecom_radio_noise_with_openalex_keywords():
    scored = score_payload(
        item_payload(
            title="Beamforming and signal processing for radio propagation",
            abstract="Antenna array optimization in wireless networks using MIMO-NOMA systems.",
            tags=["signal processing", "beamforming", "radio propagation"],
        )
    )

    assert scored.status is WatchStatus.ignored
    assert scored.relevance_score < 2
    assert len(scored.negative_keywords_matched) > 0


def test_source_name_does_not_dominate_scoring():
    scored = score_payload(
        item_payload(
            title="Spectrum sensing optimization for cognitive radio networks",
            abstract="Dynamic spectrum access in 5G mobile networks.",
            tags=["cognitive radio", "5G"],
            source_name="International Journal of Radio Frequency Engineering",
        )
    )

    # source_name contains "radio" giving a small positive boost,
    # but the heavy negative keywords should still push it to ignored
    assert scored.status is WatchStatus.ignored
    assert scored.relevance_score < 2
    assert "cognitive radio" in scored.negative_keywords_matched


def test_academic_floor_applies_for_crossref_source():
    # Titre laconique sans mot-clé connu, source Crossref → plancher candidate
    scored = score_payload(
        item_payload(
            title="Compositional practices in contemporary electroacoustic music",
            abstract=None,
            source_api="crossref",
        )
    )
    # "electroacoustic" and "electroacoustic music" match sound_studies (weight 2 × title 2 = +4)
    # but "Compositional practices" alone with no source_api would be ignored.
    # Test: a truly laconic title with zero keyword match on crossref → floor to candidate.
    scored_laconic = score_payload(
        item_payload(
            title="Recent developments in notational practice",
            abstract=None,
            source_api="crossref",
        )
    )
    assert scored_laconic.relevance_score == 0.0
    assert scored_laconic.status is WatchStatus.candidate
    assert "plancher académique" in scored_laconic.score_explanation


def test_academic_floor_does_not_apply_for_rss_source():
    # Même titre laconique, source RSS → pas de plancher → ignored
    scored = score_payload(
        item_payload(
            title="Recent developments in notational practice",
            abstract=None,
            source_api="rss",
        )
    )
    assert scored.relevance_score == 0.0
    assert scored.status is WatchStatus.ignored


def test_academic_floor_does_not_apply_without_source_api():
    # Pas de source_api (None) → pas de plancher
    scored = score_payload(
        item_payload(
            title="Recent developments in notational practice",
            abstract=None,
        )
    )
    assert scored.status is WatchStatus.ignored


def test_academic_floor_does_not_apply_for_heavy_technical_noise():
    # Article Crossref avec fort bruit technique → score très négatif → reste ignored
    scored = score_payload(
        item_payload(
            title="Cognitive radio spectrum sensing for 5G wireless networks",
            abstract="Dynamic spectrum access and beamforming in mobile networks.",
            source_api="crossref",
        )
    )
    assert scored.relevance_score < 0
    assert scored.status is WatchStatus.ignored
    assert "plancher académique" not in scored.score_explanation


def test_academic_floor_applies_for_openalex_source():
    scored = score_payload(
        item_payload(
            title="Recent developments in notational practice",
            abstract=None,
            source_api="openalex",
        )
    )
    assert scored.status is WatchStatus.candidate
    assert "plancher académique" in scored.score_explanation


def test_academic_floor_applies_for_hal_source():
    scored = score_payload(
        item_payload(
            title="Recent developments in notational practice",
            abstract=None,
            source_api="hal",
        )
    )
    assert scored.status is WatchStatus.candidate
    assert "plancher académique" in scored.score_explanation


def test_academic_floor_does_not_override_existing_to_read():
    # Si déjà to_read, le plancher ne change rien
    scored = score_payload(
        item_payload(
            title="Radio libre et archives sonores",
            abstract="Une enquête sur l'écoute radiophonique.",
            source_api="crossref",
        )
    )
    assert scored.status is WatchStatus.to_read
    assert "plancher académique" not in scored.score_explanation

