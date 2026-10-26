# RedFlag — EU product-safety evidence-gate prototype

> **Status: early prototype, not an EU product-compliance assessment.** The repository currently provides a local API and small UI for checking exact-quote presence, GTIN check digits, and common template placeholders. Statutory rules are unverified; the system deliberately abstains on them. It does not decide whether a product may be sold, provide legal advice, certify compliance, or call an LLM.

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

No API keys are required. The current implementation performs no external model or web calls.

## What is implemented

- `GET /health` — process health.
- `GET /v1/info` — explicitly reports that legal compliance verdicts are disabled.
- `GET /v1/rules` — rule metadata and verification status.
- `POST /v1/assessments` — exact quote integrity check plus the implemented internal GTIN-check-digit and placeholder checks. Unverified or unsupported rules return `UNDETERMINED`.
- A minimal React UI for submitting source text and viewing these results.

A quote match means only that the quote exists in the submitted text; it is **not** semantic support for a claim.

## Known blockers before any legal use

1. The GPSR rules are seed data. Many statutory quotes are `TODO_VERIFY(...)`, and the rules have not been independently verified against EUR-Lex.
2. The repository does not yet implement listing ingestion, field extraction, obligation applicability, Safety Gate recall matching, live-source currency checks, model routing, artifact generation, or sandbox verification.
3. The prototype has no product-level compliance verdict. Never use its internal `PASS`/`FAIL` checks as evidence of GPSR compliance.
4. Human specialist review and authoritative legal sources remain necessary. See [LIMITATIONS.md](LIMITATIONS.md).

`SPEC.md` describes a proposed future system; it is not evidence that those components exist. The actual current behavior is defined by the code and tests.
