import json
import sys
from datetime import date
from pathlib import Path

import httpx
import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ingest import ingest_openalex  # noqa: E402


def openalex_payload(title="Radio studies and listening publics"):
    return {
        "meta": {
            "count": 1,
            "page": 1,
            "per_page": 2,
            "cost_usd": 0.001,
        },
        "results": [
            {
                "id": "https://openalex.org/W123",
                "doi": "https://doi.org/10.1234/radio.1",
                "title": title,
                "display_name": title,
                "publication_date": "2026-05-01",
                "type": "article",
                "language": "en",
                "relevance_score": 12.5,
            }
        ],
    }


def write_config(
    tmp_path,
    *,
    enabled=True,
    mailto="radio@example.org",
    api_key=None,
    per_page=2,
    max_pages_per_profile=1,
    profiles=None,
):
    config_path = tmp_path / "sources.yaml"
    profile_values = profiles or [
        {
            "id": "radio_studies",
            "label": "Radio studies",
            "search": '("radio studies" OR radiophonic)',
        },
        {
            "id": "sound_studies",
            "label": "Sound studies",
            "search": '("sound studies" OR "auditory culture")',
        },
    ]
    openalex_config = {
        "enabled": enabled,
        "name": "OpenAlex fixture",
        "base_url": "https://api.openalex.org",
        "endpoint": "/works",
        "mailto_env": "OPENALEX_MAILTO",
        "api_key_env": "OPENALEX_API_KEY",
        "user_agent": "radio-watch/0.1 (test)",
        "timeout_seconds": 20,
        "polite_delay_seconds": 0,
        "window_months": 18,
        "per_page": per_page,
        "max_pages_per_profile": max_pages_per_profile,
        "sort": "relevance_score:desc",
        "filters": {
            "type": "article|book|book-chapter|dissertation|review",
            "language": ["fr", "en"],
            "is_retracted": False,
            "is_paratext": False,
        },
        "select": [
            "id",
            "doi",
            "title",
            "display_name",
            "publication_date",
            "type",
            "language",
            "topics",
            "primary_topic",
            "keywords",
            "relevance_score",
            "abstract_inverted_index",
        ],
        "forbidden_select": ["abstract_inverted_index", "authorships"],
        "noise_exclusions": [
            "radio frequency",
            "radiotherapy",
            "radio telescope",
            "cognitive radio",
            "5G",
            "6G",
            "MIMO",
            "beamforming",
        ],
        "profiles": profile_values,
    }
    if mailto is not None:
        openalex_config["mailto"] = mailto
    if api_key is not None:
        openalex_config["api_key"] = api_key

    config_path.write_text(yaml.safe_dump({"openalex": openalex_config}, sort_keys=False), encoding="utf-8")
    return config_path


def test_parse_response_reads_openalex_results():
    parsed = ingest_openalex.parse_response(openalex_payload())

    assert parsed["meta"]["count"] == 1
    assert parsed["items"][0]["doi"] == "https://doi.org/10.1234/radio.1"


def test_disabled_openalex_writes_raw_output_without_network(tmp_path):
    config_path = write_config(tmp_path, enabled=False)
    output_path = tmp_path / "data" / "raw" / "openalex_latest.json"

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("network should not be called when OpenAlex is disabled")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_openalex.ingest_openalex(config_path=config_path, output_path=output_path, client=client)

    assert payload["errors"][0]["type"] == "disabled"
    assert payload["result_count"] == 0
    assert output_path.exists()


def test_missing_mailto_is_logged_and_does_not_call_network(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENALEX_MAILTO", raising=False)
    config_path = write_config(tmp_path, mailto=None)
    output_path = tmp_path / "data" / "raw" / "openalex_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("network should not be called without mailto")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_openalex.ingest_openalex(
        config_path=config_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == "missing_mailto"
    assert payload["per_page"] == 2
    assert "requires a mailto" in log_path.read_text(encoding="utf-8")


def test_build_params_applies_window_select_and_noise_exclusions(tmp_path):
    config = yaml.safe_load(write_config(tmp_path).read_text(encoding="utf-8"))["openalex"]
    params = ingest_openalex.build_params(
        config,
        config["profiles"][0],
        mailto="radio@example.org",
        page=1,
        today=date(2026, 5, 21),
    )

    assert params["per_page"] == 2
    assert "from_publication_date:2024-11-21" in params["filter"]
    assert "type:article|book|book-chapter|dissertation|review" in params["filter"]
    assert "language:fr|en" in params["filter"]
    assert "is_retracted:false" in params["filter"]
    assert "is_paratext:false" in params["filter"]
    assert '"radio studies"' in params["search"]
    assert 'NOT ("radio frequency" OR radiotherapy' in params["search"]
    assert "abstract_inverted_index" not in params["select"]
    assert "authorships" not in params["select"]
    assert params["sort"] == "relevance_score:desc"


def test_ingest_openalex_uses_profiles_and_respects_volume_limits(tmp_path):
    config_path = write_config(tmp_path)
    output_path = tmp_path / "data" / "raw" / "openalex_latest.json"
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert request.url.path == "/works"
        assert request.url.params["mailto"] == "radio@example.org"
        assert request.url.params["per_page"] == "2"
        assert request.url.params["page"] == "1"
        assert request.url.params["sort"] == "relevance_score:desc"
        assert "radio-watch" in request.headers["User-Agent"]
        assert "abstract_inverted_index" not in request.url.params["select"]
        assert "authorships" not in request.url.params["select"]
        return httpx.Response(200, json=openalex_payload())

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_openalex.ingest_openalex(config_path=config_path, output_path=output_path, client=client)

    searches = [request.url.params["search"] for request in requests]
    assert len(requests) == 2
    assert payload["request_count"] == 2
    assert payload["result_count"] == 2
    assert payload["items"][0]["_openalex_source"]["profile_id"] == "radio_studies"
    assert payload["items"][1]["_openalex_source"]["profile_id"] == "sound_studies"
    assert any('"radio studies"' in search for search in searches)
    assert any('"sound studies"' in search for search in searches)
    assert json.loads(output_path.read_text(encoding="utf-8"))["connector"] == "openalex"


def test_timeout_is_logged_and_raw_output_is_written(tmp_path):
    config_path = write_config(tmp_path, profiles=[{"id": "radio_studies", "search": '"radio studies"'}])
    output_path = tmp_path / "data" / "raw" / "openalex_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated timeout", request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_openalex.ingest_openalex(
        config_path=config_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == "timeout"
    assert output_path.exists()
    assert "OpenAlex request timed out" in log_path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("status_code", "error_type"),
    [
        (403, "forbidden"),
        (429, "rate_limited"),
        (500, "server_error"),
    ],
)
def test_http_status_errors_are_classified_and_redacted(tmp_path, status_code, error_type):
    config_path = write_config(
        tmp_path,
        api_key="secret-openalex-key",
        profiles=[{"id": "radio_studies", "search": '"radio studies"'}],
    )
    output_path = tmp_path / "data" / "raw" / "openalex_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json={"message": "nope"}, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_openalex.ingest_openalex(
        config_path=config_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == error_type
    assert payload["errors"][0]["status_code"] == status_code
    assert "radio%40example.org" not in payload["errors"][0]["message"]
    assert "secret-openalex-key" not in payload["errors"][0]["message"]
    assert "mailto=<redacted>" in payload["errors"][0]["message"]
    assert "api_key=<redacted>" in payload["errors"][0]["message"]
