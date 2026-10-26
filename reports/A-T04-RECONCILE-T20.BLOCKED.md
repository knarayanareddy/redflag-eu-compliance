# A-T04-RECONCILE-T20 Blocked: legal verification and official alert sources

## Precise questions

1. Can an authorized human reviewer confirm the four ticket-supplied candidate quotes against EUR-Lex, verify the exact Article 19 references and applicability, and validate the claimed SHA-256 against the exact downloaded source bytes?
2. Can the data owner provide ten provenance-backed Safety Gate/RAPEX alert records (including retrieval timestamps and source URLs) for the requested magnetic-toy, charger, and cosmetics examples?
3. Can the product owner provide the primary Commission release supporting the 58% statistic and define/source what “zero-wrapper recall prior” is meant to assert?

## What I checked / tried

- Followed `docs/AGENT-DELEGATION-PROTOCOL.md` and the ticket's no-fabrication requirements. The checkout has no `data/fixtures/` directory or Safety Gate samples.
- Confirmed the approved outbound-host policy does not permit fetching EUR-Lex, the Commission release, or Safety Gate in this environment. No such request was made.
- Saved the four exact strings supplied in the ticket as `USER_SUPPLIED_CANDIDATE_UNVERIFIED` values in `data/gpsr-rules.v0.json`. Left `human_verified=false`, `source_retrieved_at=null`, and `source_sha256=null`; the gate explicitly continues to reject these candidates.
- Implemented the marketplace-card UI and connected it to the existing `/v1/listings/screen` response. It uses API verdicts only, explains URL fetching is disabled, and reports when no local recall corpus exists.
- Updated README to document current behavior and label unsupported claims as hypotheses/pending verification. Logged the divergences in `docs/DISCREPANCIES.md`.
- Ran backend tests: 27 passed. Ran Ruff, production-app mypy, and the frontend TypeScript/Vite build successfully; exact backend output is in `reports/A-T04-RECONCILE-T20.TASK_REPORT.md`.

## Output observed / safe state

- GPSR legal rules remain unverified. The API continues returning `UNDETERMINED` for statutory rules; it does not return active legal PASS/FAIL verdicts.
- With no valid Safety Gate corpus, the recalled-twin feature abstains. No recall comparison is made, and no safety conclusion is implied.
- The new UI renders a dynamic banner and evidence/recall cards; it does not force a red suppression claim for an unverified rule.
- README does not present the 58% statistic as established fact and treats recall-prior wording as an unvalidated product hypothesis.

## Two options

1. **Finish the blocked acceptance with source evidence:** have a legal reviewer verify the quotes and source digest, have the data owner deliver official/provenance-backed alerts, and provide the primary Commission citation and a precise definition for the statistic/prior. Then run the acceptance checks against those artifacts.
2. **Keep the current evidence-safe implementation:** retain candidate quotes as unverified, preserve `UNDETERMINED` behavior, and keep recall matching unavailable until the genuine alert corpus is supplied.

Do not flip human verification, invent alert records, or show legal suppression outcomes as a workaround for missing evidence.
