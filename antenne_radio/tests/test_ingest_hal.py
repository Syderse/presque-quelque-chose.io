import json
import sys
from pathlib import Path

import httpx
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ingest import ingest_hal  # noqa: E402


FIXTURE = ROOT / "tests" / "fixtures" / "hal_response.json"


def test_build_query_uses_selected_positive_keywords():
    keywords = {
        "radio_core": ["radio", "radiophonie"],
        "radio_free": ["radio libre", "community radio"],
        "podcast": ["podcast"],
        "negative_noise": ["radiology"],
    }

    query = ingest_hal.build_query(keywords, keyword_limit=4)

    assert query == '(radio OR "radio libre" OR podcast OR radiophonie)'
    assert "radiology" not in query


def test_parse_response_reads_hal_fixture():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    parsed = ingest_hal.parse_response(payload)

    assert parsed["num_found"] == 2
    assert len(parsed["docs"]) == 2
    assert parsed["docs"][0]["title_s"] == ["Radio libre et archives sonores"]


def test_fetch_hal_uses_json_params_without_network():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["wt"] == "json"
        assert request.url.params["rows"] == "2"
        return httpx.Response(200, json=payload)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    response = ingest_hal.fetch_hal(
        "https://api.archives-ouvertes.fr/search/",
        {"q": "(radio)", "rows": 2, "wt": "json"},
        client=client,
    )

    assert ingest_hal.parse_response(response)["num_found"] == 2


def test_timeout_is_logged_and_raw_output_is_written(tmp_path):
    config_path = tmp_path / "sources.yaml"
    keywords_path = tmp_path / "keywords.yaml"
    output_path = tmp_path / "data" / "raw" / "hal_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"
    db_path = tmp_path / "data" / "normalized" / "db.json"
    config = {
        "hal": {
            "enabled": True,
            "name": "HAL fixture",
            "base_url": "https://api.archives-ouvertes.fr/search/",
            "limit": 2,
        }
    }
    keywords = {"radio_core": ["radio"], "radio_free": ["radio libre"], "podcast": ["podcast"]}
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    keywords_path.write_text(yaml.safe_dump(keywords), encoding="utf-8")

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated timeout", request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_hal.ingest_hal(
        config_path=config_path,
        keywords_path=keywords_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == "timeout"
    assert output_path.exists()
    assert not db_path.exists()
    assert "HAL request timed out" in log_path.read_text(encoding="utf-8")
