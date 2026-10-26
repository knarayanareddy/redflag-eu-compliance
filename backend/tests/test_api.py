import httpx
import pytest_asyncio

from app.main import app


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


async def test_health_and_capability_disclosure(client: httpx.AsyncClient) -> None:
    assert (await client.get("/health")).json()["status"] == "ok"
    info = (await client.get("/v1/info")).json()
    assert info["legal_compliance_verdicts_enabled"] is False


async def test_rules_endpoint_marks_gpsr_rules_unverified(client: httpx.AsyncClient) -> None:
    response = await client.get("/v1/rules")
    assert response.status_code == 200
    rules = {rule["rule_id"]: rule for rule in response.json()["rules"]}
    assert rules["RF-ART19-02"]["verified"] is False
    assert response.json()["legal_compliance_verdicts_enabled"] is False


async def test_assessment_abstains_on_unverified_gpsr_rule(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/v1/assessments",
        json={
            "rule_id": "RF-ART19-02",
            "raw_source": "Product identifier: ABC-123",
            "evidence_quote": "Product identifier: ABC-123",
            "assertion": {"claim": "This listing is compliant"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "UNDETERMINED"
    assert body["legal_compliance_verdict"] == "NOT_PROVIDED"


async def test_assessment_rejects_extra_request_fields(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/v1/assessments",
        json={"rule_id": "RF-ID-CHK", "raw_source": "EAN: x", "made_up": True},
    )
    assert response.status_code == 422


async def test_listing_screen_exposes_fail_closed_recall_twin(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/v1/listings/screen",
        json={"listing_text": "Product: Wooden chess set", "product_category": "Toys"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["recall_twin"]["shared_failure_mode"]["verdict"] == "UNDETERMINED"
    assert body["risk_correlations"] == []
    assert body["warnings"] == []
    assert body["recall_corpus_available"] is False
