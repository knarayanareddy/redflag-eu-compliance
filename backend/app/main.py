"""HTTP API for RedFlag's fail-closed listing-screening prototype."""

import hashlib
import json
import time
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from app.gate.gate import DeterministicGate, load_rules, rule_is_verified
from app.stages.s2_extract_fields import extract_fields

rules = load_rules()
gate = DeterministicGate(rules)
app = FastAPI(
    title="RedFlag Listing Evidence Gate",
    description=(
        "Extract listing fields and screen evidence. Unverified legal rules abstain; "
        "this prototype does not provide legal advice or product certification."
    ),
    version="0.3.0",
)


class AssessmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, max_length=80)
    raw_source: str = Field(min_length=1, max_length=100_000)
    evidence_quote: str | None = Field(default=None, max_length=20_000)
    assertion: dict[str, Any] = Field(default_factory=dict)


class ListingScreenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    listing_text: str = Field(min_length=1, max_length=100_000)
    source_format: Literal["text", "html"] = "text"


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "mode": "local-prototype"}


@app.get("/v1/info")
def get_info() -> dict[str, Any]:
    return {
        "project": "RedFlag EU Compliance Prototype",
        "mode": "local-deterministic-checks-with-optional-nano-extraction",
        "legal_compliance_verdicts_enabled": False,
        "notice": "Unverified legal rules abstain; this is not legal advice or certification.",
    }


@app.get("/v1/rules")
def get_rules() -> dict[str, Any]:
    return {
        "rules": [
            {
                "rule_id": rule_id,
                "title": rule.get("title", rule_id),
                "severity": rule.get("severity_if_missing"),
                "verified": rule_is_verified(rule),
                "legal": (rule.get("legal_basis") or {}).get("verify") == "REQUIRED",
                "evaluator_available": rule_id in {"RF-ID-CHK", "RF-PLACEHOLDER"},
            }
            for rule_id, rule in sorted(rules.items())
        ],
        "legal_compliance_verdicts_enabled": False,
    }


@app.post("/v1/assessments")
def assess(request: AssessmentRequest) -> dict[str, Any]:
    """Check evidence integrity and supported local invariants, failing closed."""
    result = gate.evaluate(
        rule_id=request.rule_id,
        assertion=request.assertion,
        evidence_quote=request.evidence_quote,
        raw_source=request.raw_source,
    )
    return {
        "assessment_id": "local-evidence-check",
        **result,
        "legal_compliance_verdict": "NOT_PROVIDED",
    }


def _citation_for_rule(rule: dict[str, Any]) -> dict[str, Any]:
    source_quote = rule["source_quote"]
    source_url = rule["source_url"]
    digest = hashlib.sha256(f"{source_url}\n{source_quote}".encode()).hexdigest()[:16]
    return {
        "id": f"cit_{digest}",
        "kind": "regulation",
        "locator": f"{source_url} — {rule['rule_id']}",
        "quote": source_quote,
        "retrieved_at": rule["source_retrieved_at"],
        "sha256": rule["source_sha256"],
        "ttl_seconds": 2_592_000,
        "trust": "primary",
    }


def _screen_verdict(listing_id: str, listing_fields: dict[str, Any], elapsed_ms: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    finding_rows: list[dict[str, Any]] = []
    citation_rows: dict[str, dict[str, Any]] = {}
    for field in listing_fields["fields"].values():
        span = field.get("evidence_span")
        if field.get("status") != "PRESENT" or not isinstance(span, dict):
            continue
        quote = span["quote"]
        citation_key = f"{listing_id}:{span.get('char_start')}:{span.get('char_end')}:{quote}"
        citation_id = f"cit_{hashlib.sha256(citation_key.encode()).hexdigest()[:16]}"
        citation_rows[citation_id] = {
            "id": citation_id,
            "kind": "user_input",
            "locator": f"{listing_id} characters {span.get('char_start')}-{span.get('char_end')}",
            "quote": quote,
            "retrieved_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "sha256": hashlib.sha256(quote.encode()).hexdigest(),
            "ttl_seconds": None,
            "trust": "primary",
        }
    rejected: list[dict[str, str]] = []
    checks_run = 0
    checks_passed = 0
    checks_failed = 0
    unknown_rule = False
    core_rule_ids = (
        "RF-ART19-01",
        "RF-ART19-02",
        "RF-ART19-03",
        "RF-ART19-04",
        "RF-ART19-05",
    )
    extracted = listing_fields["fields"]

    for rule_id in core_rule_ids:
        rule = rules.get(rule_id)
        if rule is None:
            unknown_rule = True
            rejected.append({"claim": rule_id, "reason": "rule_unverified", "stage": "s6_gate"})
            continue
        checks_run += 1
        if not rule_is_verified(rule):
            unknown_rule = True
            rejected.append({
                "claim": rule.get("title", rule_id),
                "reason": "rule_unverified",
                "stage": "s6_gate",
            })
            continue

        field = extracted.get(rule.get("field_key"), {})
        status = field.get("status")
        if status == "PRESENT":
            checks_passed += 1
            continue
        if status != "ABSENT" or float(field.get("confidence", 0.0)) < 0.60:
            rejected.append({
                "claim": rule.get("title", rule_id),
                "reason": "confidence_below_floor",
                "stage": "s2_extract_fields",
            })
            continue

        severity = rule.get("severity_if_missing")
        if severity not in {"BLOCKING", "MAJOR", "MINOR", "INFO"}:
            rejected.append({"claim": rule_id, "reason": "rule_unverified", "stage": "s6_gate"})
            unknown_rule = True
            continue
        citation = _citation_for_rule(rule)
        citation_rows[citation["id"]] = citation
        finding_rows.append({
            "id": f"f_{len(finding_rows) + 1:02d}",
            "severity": severity,
            "rule_id": rule_id,
            "statement": rule.get("title", rule_id),
            "citation_ids": [citation["id"]],
            "gate_checks_passed": ["rule_verified", "source_hash_present", "field_status_absent"],
            "evidence": {"quote": None, "source": "submitted listing"},
            "fix": rule.get("fix_template"),
        })
        checks_failed += 1

    blocking = any(item["severity"] == "BLOCKING" for item in finding_rows)
    major = any(item["severity"] == "MAJOR" for item in finding_rows)
    if blocking and not unknown_rule:
        verdict = "WOULD_BE_SUPPRESSED"
        abstain = False
        abstain_reason = None
    elif major and not unknown_rule:
        verdict = "AT_RISK"
        abstain = False
        abstain_reason = None
    else:
        verdict = "UNDETERMINED"
        abstain = True
        abstain_reason = (
            "one_or_more_required_rules_unverified"
            if unknown_rule
            else "insufficient_evidence_or_rule_coverage"
        )

    if finding_rows:
        headline = f"{len(finding_rows)} verified listing requirement(s) need attention"
        action = next((item["fix"] for item in finding_rows if item["severity"] == "BLOCKING"), finding_rows[0]["fix"])
    elif unknown_rule:
        headline = "Legal rule sources are not verified"
        action = "Do not rely on this run for a compliance decision; have the listing reviewed by a qualified person."
    else:
        headline = "Evidence is insufficient for a compliance determination"
        action = "Review the extracted fields and confirm applicable requirements with a qualified person."

    gate_material = json.dumps(
        {"verdict": verdict, "findings": finding_rows, "rejected": rejected},
        sort_keys=True,
        separators=(",", ":"),
    )
    verdict_obj = {
        "run_id": f"run_{uuid4().hex}",
        "listing_id": listing_id,
        "verdict": verdict,
        "headline": headline[:90],
        "action_first": {"primary": action or "Review the listing manually.", "copy_targets": []},
        "findings": finding_rows,
        "gate": {
            "checks_run": checks_run,
            "checks_passed": checks_passed,
            "checks_failed": checks_failed,
            "rejected_claims": rejected,
            "abstain": abstain,
            "abstain_reason": abstain_reason,
            "determinism_hash": hashlib.sha256(gate_material.encode("utf-8")).hexdigest(),
        },
        "cost": {"total_usd": 0.0, "by_model": {}},
        "timings_ms": {"s2_extract_fields": elapsed_ms, "gate": 0, "total": elapsed_ms},
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "disclaimer": (
            "Prototype only. Not legal advice, certification, or a determination that a product may be sold."
        ),
    }
    return verdict_obj, list(citation_rows.values())


@app.post("/v1/listings/screen")
def screen_listing(request: ListingScreenRequest) -> dict[str, Any]:
    """Extract listing fields and return a schema-shaped tri-state gate response."""
    started = time.perf_counter()
    listing_fields = extract_fields(request.listing_text, source_format=request.source_format)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    verdict, citation_chips = _screen_verdict(
        listing_fields["listing_id"], listing_fields, elapsed_ms
    )
    return {
        "listing_fields": listing_fields,
        "citation_chips": citation_chips,
        "verdict": verdict,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
