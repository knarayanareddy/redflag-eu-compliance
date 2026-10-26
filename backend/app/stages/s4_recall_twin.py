"""Deterministic keyword-based retrieval over a local Safety Gate sample corpus.

This module does not fetch alerts or claim semantic similarity. It returns
UNDETERMINED when no local corpus is present and labels matches as keyword-based.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]
SAMPLE_PATH = ROOT / "data" / "fixtures" / "safety_gate_samples.json"
MAX_CANDIDATES = 5

# These are query terms, not a claim that any particular alert has a given risk.
HAZARD_TERMS: dict[str, tuple[str, ...]] = {
    "Choking": ("choking", "small parts", "swallow", "ingestion", "ingest"),
    "Electric shock": ("electric shock", "electricity", "electrical", "charger", "mains"),
    "Fire": ("fire", "overheat", "overheating", "flammable"),
    "Burns": ("burn", "burns", "hot surface", "high temperature"),
    "Cuts": ("cut", "cuts", "sharp edge", "sharp point"),
    "Strangulation": ("strangulation", "cord", "loop", "entanglement"),
    "Suffocation": ("suffocation", "suffocate", "plastic bag", "asphyxiation"),
}


def _normalise_category(value: str) -> str:
    text = value.casefold().replace("_", " ").replace("-", " ")
    if "toy" in text:
        return "toy"
    if "child" in text or "baby" in text:
        return "childcare"
    if any(term in text for term in ("electrical", "electronic", "charger", "power supply")):
        return "electrical"
    if "battery" in text:
        return "battery"
    return re.sub(r"[^a-z0-9 ]", "", text).strip()


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.casefold()) if len(token) > 2}


def _query_hazards(text: str) -> set[str]:
    lowered = text.casefold()
    return {
        risk
        for risk, signals in HAZARD_TERMS.items()
        if any(signal in lowered for signal in signals)
    }


def _valid_alert(row: Any) -> bool:
    if not isinstance(row, dict):
        return False
    required = (
        "alert_number", "publication_date", "notifying_country", "category", "product",
        "risk_types", "danger", "alert_url", "retrieved_at", "source_endpoint",
    )
    if any(not row.get(key) for key in required):
        return False
    try:
        date.fromisoformat(str(row["publication_date"]))
        retrieved_at = datetime.fromisoformat(str(row["retrieved_at"]))
        if retrieved_at.tzinfo is None:
            return False
    except ValueError:
        return False
    parsed = urlparse(str(row["alert_url"]))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    return isinstance(row["risk_types"], list) and all(isinstance(risk, str) for risk in row["risk_types"])


def load_sample_records(path: Path = SAMPLE_PATH) -> tuple[list[dict[str, Any]], bool]:
    """Read the committed local fixture corpus; return unavailable if it is absent."""
    if not path.is_file():
        return [], False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], False
    rows = data.get("alerts") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return [], False
    valid_rows = [row for row in rows if _valid_alert(row)]
    return valid_rows, bool(valid_rows)


@dataclass(frozen=True)
class RecallTwinMatch:
    recall_twin: dict[str, Any]
    risk_correlation: list[dict[str, Any]]
    citation_chips: list[dict[str, Any]]
    corpus_available: bool


def match_recall_twins(
    *,
    listing_id: str,
    product_category: str = "",
    description: str = "",
    identifier: str | None = None,
    records: Iterable[dict[str, Any]] | None = None,
) -> RecallTwinMatch:
    """Rank local alert records by category/text overlap and report hazard overlap.

    `records=None` loads the committed sample file. Passing records is intended
    for tests and offline callers; it does not fetch or synthesize official data.
    """
    if records is None:
        rows, available = load_sample_records()
    else:
        rows = [row for row in records if _valid_alert(row)]
        available = bool(rows)

    if not available:
        return RecallTwinMatch(
            recall_twin={
                "listing_id": listing_id,
                "exact_barcode_hit": None,
                "candidates": [],
                "shared_failure_mode": {
                    "verdict": "UNDETERMINED",
                    "reasoning": "No local Safety Gate sample corpus is installed; no recall comparison was made.",
                    "cited_alert_numbers": [],
                },
                "model": None,
                "ledger_id": None,
            },
            risk_correlation=[],
            citation_chips=[],
            corpus_available=False,
        )

    query_text = f"{product_category} {description}".strip()
    query_tokens = _tokens(query_text)
    query_category = _normalise_category(product_category) if product_category else ""
    query_hazards = _query_hazards(query_text)
    ranked: list[tuple[float, dict[str, Any], set[str], str]] = []
    exact_barcode_hit: str | None = None

    for row in rows:
        barcode = str(row.get("barcode") or "").strip()
        exact_match = bool(identifier and barcode and identifier.strip() == barcode)
        if exact_match:
            alert_number = str(row["alert_number"])
            if exact_barcode_hit is None or alert_number < exact_barcode_hit:
                exact_barcode_hit = alert_number

        alert_category = _normalise_category(str(row.get("category_norm") or row["category"]))
        alert_text = " ".join(
            str(row.get(key) or "") for key in ("product", "product_specific", "brand", "danger", "description")
        )
        alert_tokens = _tokens(alert_text)
        token_score = len(query_tokens & alert_tokens) / max(len(query_tokens | alert_tokens), 1)
        category_score = 1.0 if query_category and query_category == alert_category else 0.0
        alert_risks = {risk.casefold() for risk in row["risk_types"]}
        matched_hazards = {
            risk for risk in query_hazards if any(risk.casefold() == alert_risk or risk.casefold() in alert_risk for alert_risk in alert_risks)
        }
        score = 1.0 if exact_match else min(1.0, 0.5 * token_score + 0.3 * category_score + 0.2 * bool(matched_hazards))
        if score <= 0:
            continue
        ranked.append((score, row, matched_hazards, "barcode_exact" if exact_match else "keyword"))

    ranked.sort(
        key=lambda item: (
            -item[0],
            0 if item[3] == "barcode_exact" else 1,
            str(item[1]["alert_number"]),
        )
    )
    ranked = ranked[:MAX_CANDIDATES]
    candidates: list[dict[str, Any]] = []
    correlations: list[dict[str, Any]] = []
    citation_chips: list[dict[str, Any]] = []
    for score, row, hazards, similarity_basis in ranked:
        candidates.append({
            "alert_number": str(row["alert_number"]),
            "publication_date": str(row["publication_date"]),
            "notifying_country": str(row["notifying_country"]),
            "country_of_origin": row.get("country_of_origin"),
            "category": str(row["category"]),
            "product": str(row["product"]),
            "brand": row.get("brand"),
            "barcode": row.get("barcode"),
            "risk_types": list(row["risk_types"]),
            "danger_verbatim": str(row["danger"]),
            "measures": row.get("measures"),
            "image_urls": list(row.get("image_urls") or []),
            "alert_url": str(row["alert_url"]),
            "similarity": round(score, 4),
            "similarity_basis": similarity_basis,
        })
        citation_id = hashlib.sha256(
            f"{row['alert_number']}|{row['retrieved_at']}|{row['danger']}".encode()
        ).hexdigest()[:24]
        citation_chips.append({
            "id": f"cit_{citation_id}",
            "kind": "official_dataset",
            "locator": str(row["alert_number"]),
            "quote": str(row["danger"]),
            "retrieved_at": str(row["retrieved_at"]),
            "sha256": row.get("sha256"),
            "ttl_seconds": 604800,
            "trust": "official_secondary",
        })
        if hazards:
            correlations.append({
                "alert_number": str(row["alert_number"]),
                "matched_hazards": sorted(hazards),
                "alert_risk_types": list(row["risk_types"]),
            })

    cited_numbers = [item["alert_number"] for item in correlations]
    if exact_barcode_hit:
        verdict = "SHARES"
        reasoning = "The submitted identifier exactly matches a sample Safety Gate barcode."
        cited_numbers = [exact_barcode_hit]
    elif correlations:
        verdict = "POSSIBLY_SHARES"
        reasoning = "Keyword signals overlap with the cited alert hazard types; this is a retrieval lead, not a safety determination."
    else:
        verdict = "UNDETERMINED"
        reasoning = (
            "No alert with a correlated hazard signal was found in the available sample corpus. "
            "This does not establish that the product is safe or has no recall twin."
        )

    return RecallTwinMatch(
        recall_twin={
            "listing_id": listing_id,
            "exact_barcode_hit": exact_barcode_hit,
            "candidates": candidates,
            "shared_failure_mode": {
                "verdict": verdict,
                "reasoning": reasoning,
                "cited_alert_numbers": cited_numbers,
            },
            "model": None,
            "ledger_id": None,
        },
        risk_correlation=correlations,
        citation_chips=citation_chips,
        corpus_available=True,
    )
