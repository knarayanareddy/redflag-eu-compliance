# RedFlag — EU product-safety evidence-gate prototype

> **Status: early prototype, not an EU product-compliance assessment.** RedFlag extracts seller-supplied listing text, runs a fail-closed statutory screening path, and can compare it with a local Safety Gate corpus when one is installed. The current GPSR rules remain unverified, and this checkout has no official Safety Gate sample corpus. Legal compliance verdicts are not enabled.

## Run locally

Requirements: Python 3.11+, [uv](https://docs.astral.sh/uv/), and Node.js/npm.

```bash
# Terminal 1: API
make serve

# Terminal 2: UI
cd frontend
npm ci
npm run dev -- --host 0.0.0.0
```

Open the Vite URL shown in the terminal. The UI calls the API through Vite's `/v1` proxy. API documentation is available at `/docs` on port 8000.

Run backend tests/lint and build the frontend with:

```bash
make check
cd frontend && npm ci && npm run build
```

No API keys are required. The current implementation performs no external model, marketplace, EUR-Lex, or Safety Gate calls. Listing URLs are accepted as references only; the user must paste visible listing text for screening.

## What is implemented

- `GET /health` — process health.
- `GET /v1/info` — capability disclosure; legal compliance verdicts are disabled.
- `GET /v1/rules` — rule metadata and verification status.
- `POST /v1/assessments` — exact-quote integrity check plus narrow internal GTIN-check-digit and placeholder checks. These internal PASS/FAIL results are not GPSR compliance outcomes.
- `POST /v1/listings/screen` — deterministic S2 text extraction plus S4 local recall-twin keyword retrieval. It returns extracted fields, an abstaining screening verdict, local recall candidates, risk correlations, warnings, and citation chips.
- `frontend/src/App.tsx` — mock marketplace-card interface with a local screening form, dynamic verdict banner, recall-lead panel, extracted-field summary, and draft-copy action.

A quote match means only that the quote exists in the submitted text; it is **not** semantic support for a claim. Recall keyword overlaps are manual-review leads, not findings that two products are identical or share the same defect. If the local alert corpus is absent or empty, the recall stage reports `UNDETERMINED`; no-match results do not establish product safety or absence of a recall.

## Working insight and external claims

**Recall-prior thesis (a design hypothesis, not a measured result):** product-risk retrieval may be more useful as a review prior than as an exact-product blacklist alone. The current implementation is only deterministic keyword retrieval; there is no committed official alert corpus or validation study in this checkout. Do not describe this as proven recall reasoning or as a "zero-wrapper" result.

**58% coordinated-sweep figure — pending source verification.** `SPEC.md` attributes a figure that 58% of approximately 1,700 offers across 35 marketplaces showed manufacturer, EU responsible-person, and product-ID information together to a European Commission release dated 7 September 2026. The primary release and a retrieval record are not included here, and this figure has not been independently verified in this environment. Confirm the official release, exact denominator, wording, and date and add a citation before presenting the statistic as fact in product copy, a demo, or external materials.

## Known blockers before any legal use

1. `data/gpsr-rules.v0.json` remains seed data. Statutory quotes and rule mappings have not been independently verified against EUR-Lex; they must not be marked human-verified until an authorized review is recorded.
2. `data/fixtures/safety_gate_samples.json` is not present. No official alert records have been added, so live recall matches, alert citations, and retrieval quality are unverified.
3. The prototype does not produce active legal PASS/FAIL results. Unverified legal rules remain fail-closed and return `UNDETERMINED`.
4. URL fetching, live marketplace ingestion, alert ingestion, live-source currency checks, model routing, artifact generation, and sandbox verification are not implemented.
5. Human specialist review and authoritative legal sources remain necessary. See [LIMITATIONS.md](LIMITATIONS.md).

`SPEC.md` describes proposed or research-stage system behavior; it is not evidence that those components, source records, or statistics have been verified. Actual behavior is defined by the code and tests.
