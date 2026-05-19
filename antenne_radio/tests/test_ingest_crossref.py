import json
import sys
from pathlib import Path

import httpx
import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ingest import ingest_crossref  # noqa: E402


def crossref_payload(items=None):
    return {
        "status": "ok",
        "message-type": "work-list",
        "message": {
            "total-results": len(items or []),
            "items": items or [],
        },
    }


def crossref_item():
    return {
        "DOI": "10.1080/19376529.2026.1234567",
        "URL": "https://doi.org/10.1080/19376529.2026.1234567",
        "title": ["Community radio and podcast publics"],
        "container-title": ["Journal of Radio & Audio Media"],
        "published-online": {"date-parts": [[2026, 5, 1]]},
        "author": [{"given": "Ada", "family": "Radio"}],
        "subject": ["Communication", "Radio studies"],
        "abstract": "<jats:p>Radio studies abstract.</jats:p>",
        "language": "en",
    }


def write_config(tmp_path, *, enabled=True, mailto="radio@example.org", status_rows=2):
    config_path = tmp_path / "sources.yaml"
    config = {
        "crossref": {
            "enabled": enabled,
            "name": "Crossref fixture",
            "base_url": "https://api.crossref.org",
            "mailto": mailto,
            "rows": status_rows,
            "polite_delay_seconds": 0,
            "journals": [
                {
                    "id": "journal_radio_audio_media",
                    "name": "Journal of Radio & Audio Media",
                    "enabled": True,
                    "issn": ["1937-6529", "1937-6537"],
                }
            ],
        }
    }
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return config_path


def test_parse_response_reads_crossref_items():
    parsed = ingest_crossref.parse_response(crossref_payload([crossref_item()]))

    assert parsed["total_results"] == 1
    assert parsed["items"][0]["DOI"] == "10.1080/19376529.2026.1234567"


def test_ingest_crossref_uses_polite_mailto_and_user_agent(tmp_path):
    config_path = write_config(tmp_path)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/journals/1937-6529/works"
        assert request.url.params["mailto"] == "radio@example.org"
        assert request.url.params["rows"] == "2"
        assert "radio-watch" in request.headers["User-Agent"]
        return httpx.Response(200, json=crossref_payload([crossref_item()]))

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_crossref.ingest_crossref(config_path=config_path, output_path=output_path, client=client)

    assert payload["result_count"] == 1
    assert payload["items"][0]["_crossref_source"]["issn"] == "1937-6529"
    assert payload["journals"][0]["total_results"] == 1
    assert output_path.exists()


def test_disabled_crossref_writes_raw_output_without_network(tmp_path):
    config_path = write_config(tmp_path, enabled=False)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"
    db_path = tmp_path / "data" / "normalized" / "db.json"

    payload = ingest_crossref.ingest_crossref(config_path=config_path, output_path=output_path)

    assert payload["errors"][0]["type"] == "disabled"
    assert output_path.exists()
    assert not db_path.exists()


def test_missing_mailto_is_logged_and_does_not_call_network(tmp_path):
    config_path = write_config(tmp_path, mailto=None)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("network should not be called without mailto")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_crossref.ingest_crossref(
        config_path=config_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == "missing_mailto"
    assert "requires a mailto" in log_path.read_text(encoding="utf-8")


def test_timeout_is_logged_and_raw_output_is_written(tmp_path):
    config_path = write_config(tmp_path)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"
    log_path = tmp_path / "data" / "logs" / "api.log"

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated timeout", request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_crossref.ingest_crossref(
        config_path=config_path,
        output_path=output_path,
        log_path=log_path,
        client=client,
    )

    assert payload["errors"][0]["type"] == "timeout"
    assert output_path.exists()
    assert "Crossref request timed out" in log_path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("status_code", "error_type"),
    [
        (403, "forbidden"),
        (429, "rate_limited"),
        (500, "server_error"),
    ],
)
def test_http_status_errors_are_classified(tmp_path, status_code, error_type):
    config_path = write_config(tmp_path)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json={"message": "nope"}, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_crossref.ingest_crossref(config_path=config_path, output_path=output_path, client=client)

    assert payload["errors"][0]["type"] == error_type
    assert payload["errors"][0]["status_code"] == status_code


def test_empty_response_is_recorded_without_failing(tmp_path):
    config_path = write_config(tmp_path)
    output_path = tmp_path / "data" / "raw" / "crossref_latest.json"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=crossref_payload([]))

    client = httpx.Client(transport=httpx.MockTransport(handler))
    payload = ingest_crossref.ingest_crossref(config_path=config_path, output_path=output_path, client=client)
    written = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["result_count"] == 0
    assert payload["errors"][0]["type"] == "empty_response"
    assert written["journals"][0]["errors"][0]["type"] == "empty_response"
