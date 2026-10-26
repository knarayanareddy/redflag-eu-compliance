from app.gate.gate import DeterministicGate, load_rules


def test_statutory_rule_abstains_even_when_quote_matches() -> None:
    gate = DeterministicGate()
    result = gate.evaluate(
        "RF-ART19-02",
        {"claim": "This listing is compliant"},
        "Product identifier: ABC-123",
        "Product identifier: ABC-123",
    )

    assert result["verdict"] == "UNDETERMINED"
    assert result["evidence_verified"] is True
    assert result["rule_verified"] is False
    assert "unverified" in result["reason"]


def test_quote_mismatch_never_becomes_a_pass() -> None:
    result = DeterministicGate().evaluate(
        "RF-ID-CHK",
        {"value": "4006381333931"},
        "EAN 4006381333931",
        "EAN 4006381333932",
    )

    assert result["verdict"] == "UNDETERMINED"
    assert result["evidence_verified"] is False


def test_gtin_check_is_deterministic_and_validates_claimed_input() -> None:
    gate = DeterministicGate()
    source = "EAN: 4006381333931"
    valid = gate.evaluate("RF-ID-CHK", {"value": "4006381333931"}, source, source)
    invalid_source = "EAN: 4006381333932"
    invalid = gate.evaluate(
        "RF-ID-CHK",
        {"value": "4006381333932"},
        invalid_source,
        invalid_source,
    )

    assert valid["verdict"] == "PASS"
    assert invalid["verdict"] == "FAIL"


def test_gtin_check_abstains_when_value_is_not_in_source() -> None:
    result = DeterministicGate().evaluate(
        "RF-ID-CHK",
        {"value": "4006381333931"},
        "EAN: unknown",
        "EAN: unknown",
    )
    assert result["verdict"] == "UNDETERMINED"


def test_placeholder_check_uses_artifact_not_quote_semantics() -> None:
    gate = DeterministicGate()
    source = "The product label is shown."
    result = gate.evaluate(
        "RF-PLACEHOLDER",
        {"artifact_text": "{{responsible_person_name}}"},
        source,
        source,
    )

    assert result["verdict"] == "FAIL"
    assert "Placeholder-like" in result["reason"]


def test_rule_loader_has_unique_rule_ids_and_reports_unverified_gpsr_rules() -> None:
    rules = load_rules()
    assert len(rules) == 15
    assert not rules["RF-ART19-02"].get("human_verified", False)
