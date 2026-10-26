# A-T04-UNBLOCK-T19 Blocked: legal source data, real alert corpus, and frontend ownership

## Precise questions

1. Can an authorized human retrieve/review the official EUR-Lex text and provide the correct Article 19 rule-ID mapping, exact supporting quotes, a digest of the actual source document, retrieval metadata, and signed human-verification decisions?
2. Can the data owner provide committed, provenance-documented Safety Gate sample records at `data/fixtures/safety_gate_samples.json`?
3. Can the frontend owner implement the requested warning and recall-twin display, consuming the backend response fields without treating them as legal-compliance conclusions?

## What I checked / tried

- Followed `docs/AGENT-DELEGATION-PROTOCOL.md`; its lane table assigns `data/` to `data-agent` and `frontend/` to `frontend-agent`, so those paths were not edited.
- Confirmed `data/fixtures/` and `data/fixtures/safety_gate_samples.json` are absent. No official alert data was fabricated.
- Inspected `data/gpsr-rules.v0.json`. Its current mapping is RF-ART19-02 = responsible-person identity; RF-ART19-03/-04 = responsible-person postal/electronic contact; RF-ART19-05 = manufacturer identity; RF-ART19-09 = warnings/safety information. This conflicts with the ticket mapping.
- Confirmed the requested digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is the digest of empty bytes. No EUR-Lex content was fetched or reviewed, and no `human_verified` field was changed.
- Implemented backend-local deterministic retrieval and API exposure, with abstention for a missing/empty/invalid corpus. Tests use a clearly labeled synthetic-only record and do not represent it as an official alert.
- Ran the requested pytest suite successfully (26 passed); Ruff and production-app mypy passed. See `reports/A-T04-UNBLOCK-T19.TASK_REPORT.md` for exact output.

## Output / current safe state

- Backend API returns a separate recall-twin result, risk correlations, warning objects, corpus availability, and citations for retrieved local records.
- Since the actual corpus is absent, runtime recall output is `UNDETERMINED`, with no warnings or risk correlations. This is not evidence of product safety or absence of recalls.
- Existing statutory GPSR rules remain unverified and continue to fail closed.

## Two options

1. **Complete the blocked acceptance safely:** have the data/legal owner resolve the rule mapping, fetch and review the official EUR-Lex source, record a true document hash and reviewer metadata, and provide provenance-backed Safety Gate sample records; then have the frontend owner implement the warning/recall UI.
2. **Keep this backend-only partial implementation:** preserve abstention and clearly report the unmet legal-data, real-corpus, and UI acceptance criteria until those owners supply their artifacts.

Do not substitute the empty-content digest, guessed legal mappings, or invented alerts for the missing evidence.
