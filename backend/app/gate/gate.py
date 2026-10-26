"""Fail-closed, deterministic checks used by the prototype API.

Evidence matching proves only that a quote occurs in supplied text. It does not
prove that the quote supports a legal claim. Legal rules without verified source
text and an implemented deterministic evaluator always abstain.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

RULES_PATH = Path(__file__).resolve().parents[3] / "data" / "gpsr-rules.v0.json"
_PLACEHOLDER_RE = re.compile(
    r"(?i)(?:\b(?:TODO|TBD|lorem|ipsum|XXXX+|placeholder)\b|"
    r"example\.com|your[- ]name|\{\{)"
)


def load_rules(path: Path = RULES_PATH) -> dict[str, dict[str, Any]]:
    """Load the rule table, rejecting malformed or duplicate rule identifiers."""
    with path.open(encoding="utf-8") as source:
        document = json.load(source)
    if not isinstance(document, dict):
        raise TypeError("Rule data must be a JSON object")
    rows = document.get("rules")
    if not isinstance(rows, list):
        raise TypeError("Rule data must contain a rules array")

    rules: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("rule_id"), str):
            raise TypeError("Every rule must be an object with a string rule_id")
        rule_id = row["rule_id"]
        if rule_id in rules:
            raise ValueError(f"Duplicate rule_id: {rule_id}")
        rules[rule_id] = row
    return rules


def rule_is_verified(rule: Mapping[str, Any]) -> bool:
    """Require explicit verification and real source metadata for legal rules."""
    quote = rule.get("source_quote")
    if not isinstance(quote, str) or not quote.strip():
        return False
    if quote.lstrip().startswith("TODO_VERIFY"):
        return False
    if rule.get("source_quote_status") == "USER_SUPPLIED_CANDIDATE_UNVERIFIED":
        return False
    if rule.get("human_verified") is not True:
        return False

    legal_basis = rule.get("legal_basis") or {}
    if legal_basis.get("verify") == "REQUIRED":
        return bool(
            rule.get("source_retrieved_at")
            and rule.get("source_sha256")
            and rule.get("human_verified_at")
        )
    return True


def _gtin_checksum_valid(value: Any) -> bool:
    if not isinstance(value, str) or not value.isdigit() or len(value) not in {8, 12, 13, 14}:
        return False
    digits = [int(digit) for digit in value]
    check_digit = digits.pop()
    weighted_sum = sum(
        digit * (3 if (len(digits) - index) % 2 else 1)
        for index, digit in enumerate(digits)
    )
    return (10 - weighted_sum % 10) % 10 == check_digit


class DeterministicGate:
    """Evaluate implemented local invariants; abstain on legal obligations."""

    def __init__(self, rules: Mapping[str, Mapping[str, Any]] | None = None) -> None:
        self.rules = dict(rules) if rules is not None else load_rules()

    def evaluate(
        self,
        rule_id: str,
        assertion: Mapping[str, Any],
        evidence_quote: str | None,
        raw_source: str,
    ) -> dict[str, Any]:
        rule = self.rules.get(rule_id)
        result: dict[str, Any] = {
            "rule_id": rule_id,
            "verdict": "UNDETERMINED",
            "evidence_verified": False,
            "rule_verified": bool(rule and rule_is_verified(rule)),
            "reason": "",
        }
        if rule is None:
            result["reason"] = "Unknown rule; no determination was made"
            return result
        if not isinstance(raw_source, str) or not raw_source.strip():
            result["reason"] = "Raw source text is required"
            return result
        if not isinstance(evidence_quote, str) or not evidence_quote.strip():
            result["reason"] = "No evidence quote supplied; no determination was made"
            return result
        if evidence_quote not in raw_source:
            result["reason"] = "Evidence quote is not an exact substring of the supplied source"
            return result

        result["evidence_verified"] = True
        if not result["rule_verified"]:
            result["reason"] = "Rule source is unverified; legal compliance was not assessed"
            return result
        if not isinstance(assertion, Mapping):
            result["reason"] = "Assertion must be a structured object"
            return result

        # These are deliberately narrow, non-legal quality checks. A quote match
        # is not treated as proof for either result.
        if rule_id == "RF-ID-CHK":
            identifier = assertion.get("value")
            if not isinstance(identifier, str) or identifier not in raw_source:
                result["reason"] = "Checked identifier does not appear verbatim in the supplied source"
                return result
            valid = _gtin_checksum_valid(identifier)
            result.update(
                verdict="PASS" if valid else "FAIL",
                reason=(
                    "Identifier passes the GTIN check-digit calculation"
                    if valid
                    else "Identifier is not a supported-length numeric GTIN with a valid check digit"
                ),
                checked_value=identifier,
            )
            return result

        if rule_id == "RF-PLACEHOLDER":
            artifact_text = assertion.get("artifact_text")
            if not isinstance(artifact_text, str):
                result["reason"] = "artifact_text is required for the placeholder check"
                return result
            match = _PLACEHOLDER_RE.search(artifact_text)
            result.update(
                verdict="FAIL" if match else "PASS",
                reason=(
                    f"Placeholder-like text found at character {match.start()}"
                    if match
                    else "No known placeholder pattern was found"
                ),
            )
            return result

        result["reason"] = "No deterministic evaluator is implemented for this rule"
        result["verdict"] = "UNDETERMINED"
        return result
