"""S2 tests use only clearly synthetic listing content."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import httpx
import pytest
import pytest_asyncio
from jsonschema import Draft202012Validator

from app import main
from app.stages import s2_extract_fields
from app.stages.s2_extract_fields import FIELD_KEYS, extract_fields

ROOT = Path(__file__).resolve().parents[2]

CORE_SCHEMA = json.loads((ROOT / "schemas" / "core-schemas.json").read_text(encoding="utf-8"))
SYNTHETIC_LISTING = """SYNTHETIC TEST LISTING — not a real product or seller.
Product name: Example magnetic building set
EAN: 4006381333931
Manufacturer: Example Tools B.V.
Manufacturer address: Example Street 12, 2611 AB Delft, Netherlands
Manufacturer email: manufacturer@example.test
EU Responsible Person: Example Compliance B.V.
EU Responsible Person address: Sample Road 4, 2611 AB Delft, Netherlands
EU Responsible Person email: rp@example.test
Safety warnings: Warning: keep away from small children.
"""


def _load_eurlex_fetcher():
    spec = importlib.util.spec_from_file_location("fetch_eurlex", ROOT / "scripts" / "fetch_eurlex.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validator(type_name: str) -> Draft202012Validator:
    target_ref = CORE_SCHEMA["types"][type_name]["$ref"]
    schema = {
        "$schema": CORE_SCHEMA["$schema"],
        "$defs": CORE_SCHEMA["$defs"],
        "$ref": target_ref,
    }
    return Draft202012Validator(schema)


def test_deterministic_extraction_emits_exact_spans_and_contract_shape() -> None:
    output = extract_fields(SYNTHETIC_LISTING, use_model=False)
    _validator("ListingFields").validate(output)

    assert output["schema_ok"] is True
    assert set(output["fields"]) == set(FIELD_KEYS)
    for result in output["fields"].values():
        span = result["evidence_span"]
        if result["status"] == "PRESENT":
            assert span is not None
            assert SYNTHETIC_LISTING[span["char_start"] : span["char_end"]] == span["quote"]

    assert output["fields"]["product_identifier"]["value"] == "4006381333931"
    assert output["fields"]["responsible_person_identity"]["value"] == "Example Compliance B.V."
    assert output["fields"]["warnings_or_safety_info"]["extra"]["languages_detected"] == ["en"]


def test_html_extraction_offsets_and_quote_point_into_original_html() -> None:
    synthetic_html = (
        "<html><body><p>EAN: 4006381333931</p>"
        "<p>EU Responsible Person: Example Compliance B.V.</p>"
        "<img src='product.png' alt='synthetic product'></body></html>"
    )
    output = extract_fields(synthetic_html, source_format="html", use_model=False)
    _validator("ListingFields").validate(output)
    for result in output["fields"].values():
        span = result["evidence_span"]
        if result["status"] == "PRESENT":
            assert synthetic_html[span["char_start"] : span["char_end"]] == span["quote"]
    image_span = output["fields"]["product_image_present"]["evidence_span"]
    assert image_span["source"] == "images"
    assert "<img" in image_span["quote"]


def test_model_present_quote_is_reanchored_and_absence_cannot_override_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_NANO", "synthetic-nano-model")
    source = "Manufacturer: Example Maker\nEU Responsible Person: Example RP B.V."
    response = {
        "fields": {
            "manufacturer_identity": {
                "status": "PRESENT",
                "value": "Example Maker",
                "evidence_span": {"source": "description", "quote": "Manufacturer: Example Maker"},
                "confidence": 0.95,
                "extra": {},
            },
            "responsible_person_identity": {
                "status": "ABSENT",
                "value": None,
                "evidence_span": None,
                "confidence": 0.9,
                "extra": {},
            },
        }
    }
    monkeypatch.setattr(s2_extract_fields, "_call_nano", lambda *_args: response)

    output = extract_fields(source)
    manufacturer = output["fields"]["manufacturer_identity"]
    assert manufacturer["status"] == "PRESENT"
    assert source[manufacturer["evidence_span"]["char_start"] : manufacturer["evidence_span"]["char_end"]] == manufacturer["evidence_span"]["quote"]
    assert output["fields"]["responsible_person_identity"]["status"] == "PRESENT"


def test_model_quote_not_found_is_demoted_to_unparseable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_NANO", "synthetic-nano-model")
    fake_response = {
        "fields": {
            "manufacturer_identity": {
                "status": "PRESENT",
                "value": "Invented Manufacturer",
                "evidence_span": {"source": "description", "quote": "not in input"},
                "confidence": 0.99,
                "extra": {},
            }
        }
    }
    monkeypatch.setattr(s2_extract_fields, "_call_nano", lambda *_args: fake_response)

    output = extract_fields("SYNTHETIC TEST listing with no manufacturer label.")
    result = output["fields"]["manufacturer_identity"]
    assert output["model"] == "synthetic-nano-model"
    assert result["status"] == "UNPARSEABLE"
    assert result["confidence"] == 0
    assert result["evidence_span"] is None


def test_model_transport_failure_falls_back_to_deterministic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_NANO", "synthetic-nano-model")

    def fail_call(*_args):
        raise OSError("synthetic network failure")

    monkeypatch.setattr(s2_extract_fields, "_call_nano", fail_call)
    output = extract_fields(SYNTHETIC_LISTING)
    assert output["model"] == "deterministic_fallback:synthetic-nano-model"
    assert output["schema_ok"] is True


def test_empty_or_oversize_input_fails_without_partial_output() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        extract_fields("  ", use_model=False)
    with pytest.raises(ValueError, match="exceeds"):
        extract_fields("x" * 100_001, use_model=False)


def test_eurlex_parser_stages_exact_article_without_human_verification() -> None:
    fetcher = _load_eurlex_fetcher()
    with pytest.raises(ValueError, match="Refusing non-EUR-Lex"):
        fetcher.fetch_document("https://example.invalid/document")
    synthetic_html = (
        "<p class='oj-ti-art'>Article 19</p>"
        "<p>SYNTHETIC TEST TEXT ONLY — not the law.</p>"
        "<p class='oj-ti-art'>Article 20</p><p>Next synthetic article.</p>"
    )
    articles = fetcher.extract_articles(synthetic_html)
    assert "SYNTHETIC TEST TEXT ONLY" in articles[19]
    assert 20 in articles

    url = "https://eur-lex.europa.eu/eli/reg/2023/988/oj/eng"
    source_bytes = synthetic_html.encode()
    rule_data = {
        "rules": [{
            "rule_id": "RF-TEST",
            "source_quote": "TODO_VERIFY(test only)",
            "source_url": url,
            "legal_basis": {"article_ref": "Art. 19(?)", "verify": "REQUIRED"},
            "human_verified": False,
            "human_verified_at": None,
        }]
    }
    updated, unresolved = fetcher.update_rule_sources(
        rule_data,
        {url: (source_bytes, hashlib.sha256(source_bytes).hexdigest(), "2026-10-26T00:00:00Z")},
    )
    rule = rule_data["rules"][0]
    assert updated == 1 and unresolved == []
    assert rule["source_quote"] == articles[19]
    assert rule["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert rule["human_verified"] is False


@pytest_asyncio.fixture
async def api_client():
    transport = httpx.ASGITransport(app=main.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_screen_response_contains_schema_valid_fields_verdict_and_citations(api_client) -> None:
    response = await api_client.post(
        "/v1/listings/screen",
        json={"listing_text": SYNTHETIC_LISTING, "source_format": "text"},
    )
    assert response.status_code == 200
    body = response.json()
    _validator("ListingFields").validate(body["listing_fields"])
    _validator("Verdict").validate(body["verdict"])
    citation_validator = _validator("Citation")
    for citation in body["citation_chips"]:
        citation_validator.validate(citation)

    # Current source rules are unverified, so the screen must abstain even when
    # the synthetic listing appears to contain all requested fields.
    assert body["verdict"]["verdict"] == "UNDETERMINED"
    assert body["verdict"]["gate"]["abstain"] is True
    assert body["citation_chips"]
    assert all(citation["kind"] == "user_input" for citation in body["citation_chips"])


async def test_missing_rp_only_becomes_blocking_with_verified_test_rules(
    api_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    # SYNTHETIC TEST RULES — these are not legal text and never modify data files.
    test_rules = copy.deepcopy(main.rules)
    for rule_id in ("RF-ART19-01", "RF-ART19-02", "RF-ART19-03", "RF-ART19-04", "RF-ART19-05"):
        rule = test_rules[rule_id]
        rule["source_quote"] = f"SYNTHETIC TEST ONLY: {rule_id}; not a statutory quote."
        rule["source_url"] = "https://example.invalid/synthetic-rule"
        rule["source_retrieved_at"] = "2026-10-26T00:00:00Z"
        rule["source_sha256"] = hashlib.sha256(rule["source_quote"].encode()).hexdigest()
        rule["human_verified"] = True
        rule["human_verified_at"] = "2026-10-26"
    monkeypatch.setattr(main, "rules", test_rules)

    response = await api_client.post(
        "/v1/listings/screen",
        json={"listing_text": "SYNTHETIC TEST listing with no responsible-person block."},
    )
    assert response.status_code == 200
    body = response.json()
    _validator("Verdict").validate(body["verdict"])
    citation_validator = _validator("Citation")
    for citation in body["citation_chips"]:
        citation_validator.validate(citation)
    citation_ids = {citation["id"] for citation in body["citation_chips"]}
    assert body["verdict"]["verdict"] == "WOULD_BE_SUPPRESSED"
    rp_finding = next(
        finding for finding in body["verdict"]["findings"] if finding["rule_id"] == "RF-ART19-02"
    )
    assert rp_finding["severity"] == "BLOCKING"
    assert rp_finding["citation_ids"]
    assert set(rp_finding["citation_ids"]).issubset(citation_ids)
