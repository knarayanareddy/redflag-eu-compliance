from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from app.stages import s4_recall_twin
from app.stages.s4_recall_twin import load_sample_records, match_recall_twins

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "schemas" / "core-schemas.json").read_text(encoding="utf-8"))


def _synthetic_alert() -> dict[str, object]:
    """A non-authoritative contract fixture; never a real Safety Gate alert."""
    return {
        "alert_number": "SYNTHETIC-TEST-NOT-REAL",
        "publication_date": "2026-01-02",
        "notifying_country": "XX",
        "country_of_origin": None,
        "category": "Toys",
        "category_norm": "toy",
        "product": "Synthetic toy with small parts",
        "brand": "Example Test Brand",
        "barcode": "0000000000000",
        "risk_types": ["Choking"],
        "danger": "SYNTHETIC TEST TEXT ONLY: small parts may cause choking.",
        "measures": "Synthetic test measure",
        "image_urls": [],
        "alert_url": "https://example.invalid/synthetic-test-alert",
        "retrieved_at": "2026-10-26T12:00:00Z",
        "source_endpoint": "synthetic-test-only",
    }


def test_missing_local_corpus_abstains(tmp_path: Path, monkeypatch) -> None:
    absent_path = tmp_path / "absent.json"
    monkeypatch.setattr(s4_recall_twin, "SAMPLE_PATH", absent_path)
    records, available = load_sample_records(absent_path)
    assert records == []
    assert available is False

    result = match_recall_twins(listing_id="listing-test", records=None)
    assert result.corpus_available is False
    assert result.recall_twin["shared_failure_mode"]["verdict"] == "UNDETERMINED"
    assert result.risk_correlation == []
    assert result.citation_chips == []


def test_recall_result_and_alert_citations_follow_contract() -> None:
    result = match_recall_twins(
        listing_id="listing-test",
        product_category="Toys",
        description="Toy with small parts; choking hazard",
        records=[_synthetic_alert()],
    )
    assert result.corpus_available is True
    assert result.recall_twin["shared_failure_mode"]["verdict"] == "POSSIBLY_SHARES"
    assert result.recall_twin["shared_failure_mode"]["cited_alert_numbers"] == ["SYNTHETIC-TEST-NOT-REAL"]
    assert result.risk_correlation[0]["matched_hazards"] == ["Choking"]

    recall_schema = {"$schema": SCHEMA["$schema"], "$defs": SCHEMA["$defs"], "$ref": "#/$defs/RecallTwin"}
    Draft202012Validator(recall_schema).validate(result.recall_twin)
    citation_schema = {"$schema": SCHEMA["$schema"], "$defs": SCHEMA["$defs"], "$ref": "#/$defs/Citation"}
    citation_validator = Draft202012Validator(citation_schema)
    for citation in result.citation_chips:
        citation_validator.validate(citation)
        assert citation["quote"] == _synthetic_alert()["danger"]


def test_exact_gtin_match_is_returned_and_cited() -> None:
    result = match_recall_twins(
        listing_id="listing-test",
        identifier="0000000000000",
        records=[_synthetic_alert()],
    )
    assert result.recall_twin["exact_barcode_hit"] == "SYNTHETIC-TEST-NOT-REAL"
    candidate = result.recall_twin["candidates"][0]
    assert candidate["similarity_basis"] == "barcode_exact"
    assert candidate["similarity"] == 1.0
    assert result.recall_twin["shared_failure_mode"]["cited_alert_numbers"] == [candidate["alert_number"]]
    assert result.citation_chips[0]["locator"] == candidate["alert_number"]


def test_nonmatching_terms_do_not_claim_no_recall_exists() -> None:
    result = match_recall_twins(
        listing_id="listing-test",
        product_category="Toys",
        description="wooden adult chess set",
        records=[_synthetic_alert()],
    )
    assert result.recall_twin["shared_failure_mode"]["verdict"] == "UNDETERMINED"
    assert "does not establish" in result.recall_twin["shared_failure_mode"]["reasoning"]
