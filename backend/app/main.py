"""HTTP API for RedFlag's local, fail-closed evidence-gate prototype."""

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from app.gate.gate import DeterministicGate, load_rules, rule_is_verified

rules = load_rules()
gate = DeterministicGate(rules)
app = FastAPI(
    title="RedFlag Evidence Gate Prototype",
    description=(
        "A local evidence-integrity and deterministic-check prototype. It does not "
        "provide legal advice, product certification, or a GPSR compliance verdict."
    ),
    version="0.2.0",
)


class AssessmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, max_length=80)
    raw_source: str = Field(min_length=1, max_length=100_000)
    evidence_quote: str | None = Field(default=None, max_length=20_000)
    assertion: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "mode": "local-prototype"}


@app.get("/v1/info")
def get_info() -> dict[str, Any]:
    return {
        "project": "RedFlag EU Compliance Prototype",
        "mode": "local-deterministic-checks",
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
