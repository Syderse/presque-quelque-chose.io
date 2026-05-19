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
    scored = score_payload(
        item_payload(
            title="Carnet sonore hebdomadaire",
            abstract="Un podcast documentaire sur les pratiques d'écoute ordinaires.",
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
