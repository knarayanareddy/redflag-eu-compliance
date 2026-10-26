# Limitations and safe use

> **This prototype is not a legal authority, certification body, or product-compliance assessment. Do not use its output to decide whether a product may be sold.**

## Current scope

The running code checks whether a supplied quote is an exact substring of supplied text and provides two narrow internal checks: GTIN check digits and common placeholder patterns. A quote match does not establish that the quote supports a claim. The checks do not determine GPSR obligations, product safety, or marketplace suppression risk.

GPSR rules in `data/gpsr-rules.v0.json` are seed data and have not been verified against authoritative text. The API therefore abstains on legal rules. No model, web search, Safety Gate dataset, marketplace fetch, or sandbox is currently connected.

## Failure modes

| Failure mode | Current mitigation / limitation |
|---|---|
| Missing or mismatched quote | The evidence check returns `UNDETERMINED`; a text mismatch is not presented as a legal violation. |
| Unverified statutory rule | The gate returns `UNDETERMINED`; no legal compliance verdict is produced. |
| Unsupported rule evaluator | The gate returns `UNDETERMINED`. |
| Invalid GTIN check digit | The internal checksum test returns `FAIL`; this says nothing about the legality or safety of the product. |
| Placeholder-like artifact text | The internal placeholder check returns `FAIL`; it checks a limited pattern set and can miss other placeholders. |
| False or irrelevant quote | Exact substring matching cannot establish semantic relevance. Human review is required. |

## Safe use

Treat every output as a software prototype demonstration only. Do not rely on it for legal, regulatory, marketplace, or product-safety decisions. Verify applicable law using authoritative sources and consult a qualified professional.
