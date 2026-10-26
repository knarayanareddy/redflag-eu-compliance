# A-T04-RECONCILE-T20 Task Report

## WHAT

- Updated `data/gpsr-rules.v0.json` with the four exact strings supplied in the ticket, but explicitly marked each `source_quote_status: USER_SUPPLIED_CANDIDATE_UNVERIFIED`. Left `human_verified=false`, `source_retrieved_at=null`, and `source_sha256=null`; the supplied digest was not presented as a fetched-source hash.
- Hardened `backend/app/gate/gate.py` so ticket-supplied candidate quotes remain unverified even if someone fills the human-verification and hash fields without first updating their source-review status. Added a regression test in `backend/tests/test_gate.py`; adjusted the existing synthetic-rule test to remove candidate status when replacing a candidate with a synthetic verified-test rule.
- Added `frontend/src/App.tsx` and changed `frontend/src/main.tsx` to render it. The UI provides raw-text and URL-reference modes, calls the existing listing-screen API, shows a verdict banner driven only by the API response, renders recall candidates and hazard correlations when present, explains corpus abstention, and copies extracted listing details as a clearly labeled draft for Amazon/bol.com. URL fetching remains disabled; the UI asks for pasted visible text.
- Updated `frontend/src/app.css` without changing `frontend/src/tokens.css` to style the marketplace-card dashboard.
- Updated `README.md` to document the current API/UI, local keyword-retrieval limitations, the 58% figure as pending primary-source verification, and recall-prior framing as a design hypothesis rather than a measured result.
- Recorded the legal-source, fixture-data, statistics, and verdict conflicts in `docs/DISCREPANCIES.md`.

## VERIFIED

Backend VERIFY command run from `backend/`:

```text
PATH="/tmp/a-t04-reconcile-venv/bin:$PATH" UV_PROJECT_ENVIRONMENT=/tmp/a-t04-reconcile-venv uv run --extra dev pytest tests/ -v
```

Exact output:

```text
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.7.0 -- /tmp/a-t04-reconcile-venv/bin/python
cachedir: .pytest_cache
rootdir: /home/user/redflag-eu-compliance/backend
configfile: pyproject.toml
plugins: asyncio-1.4.1, anyio-4.15.1
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 27 items

tests/test_api.py::test_health_and_capability_disclosure PASSED          [  3%]
tests/test_api.py::test_rules_endpoint_marks_gpsr_rules_unverified PASSED [  7%]
tests/test_api.py::test_assessment_abstains_on_unverified_gpsr_rule PASSED [ 11%]
tests/test_api.py::test_assessment_rejects_extra_request_fields PASSED   [ 14%]
tests/test_api.py::test_listing_screen_exposes_fail_closed_recall_twin PASSED [ 18%]
tests/test_extraction.py::test_deterministic_extraction_emits_exact_spans_and_contract_shape PASSED [ 22%]
tests/test_extraction.py::test_html_extraction_offsets_and_quote_point_into_original_html PASSED [ 25%]
tests/test_extraction.py::test_model_present_quote_is_reanchored_and_absence_cannot_override_source PASSED [ 29%]
tests/test_extraction.py::test_model_quote_not_found_is_demoted_to_unparseable PASSED [ 33%]
tests/test_extraction.py::test_model_transport_failure_falls_back_to_deterministic PASSED [ 37%]
tests/test_extraction.py::test_empty_or_oversize_input_fails_without_partial_output PASSED [ 40%]
tests/test_extraction.py::test_eurlex_parser_stages_exact_article_without_human_verification PASSED [ 44%]
tests/test_extraction.py::test_screen_response_contains_schema_valid_fields_verdict_and_citations PASSED [ 48%]
tests/test_extraction.py::test_missing_rp_only_becomes_blocking_with_verified_test_rules PASSED [ 51%]
tests/test_gate.py::test_ticket_supplied_gpsr_quotes_remain_unverified_candidates PASSED [ 55%]
tests/test_gate.py::test_statutory_rule_abstains_even_when_quote_matches PASSED [ 59%]
tests/test_gate.py::test_quote_mismatch_never_becomes_a_pass PASSED      [ 62%]
tests/test_gate.py::test_gtin_check_is_deterministic_and_validates_claimed_input PASSED [ 66%]
tests/test_gate.py::test_gtin_check_abstains_when_value_is_not_in_source PASSED [ 70%]
tests/test_gate.py::test_placeholder_check_uses_artifact_not_quote_semantics PASSED [ 74%]
tests/test_gate.py::test_rule_loader_has_unique_rule_ids_and_reports_unverified_gpsr_rules PASSED [ 77%]
tests/test_recall_twin.py::test_missing_local_corpus_abstains PASSED     [ 81%]
tests/test_recall_twin.py::test_recall_result_and_alert_citations_follow_contract PASSED [ 85%]
tests/test_recall_twin.py::test_exact_gtin_match_is_returned_and_cited PASSED [ 88%]
tests/test_recall_twin.py::test_nonmatching_terms_do_not_claim_no_recall_exists PASSED [ 92%]
tests/test_schemas.py::test_core_schema_is_valid_json_schema PASSED      [ 96%]
tests/test_schemas.py::test_citation_contract_accepts_valid_and_rejects_invalid PASSED [100%]

============================== 27 passed in 0.40s ==============================
```

Additional checks:

- `cd frontend && npm ci && npm run build`: passed; TypeScript type-check and Vite production build succeeded.
- From `backend/`, `uv run --extra dev ruff check app tests`: `All checks passed!`
- From `backend/`, `uv run --extra dev mypy app`: `Success: no issues found in 7 source files`.

The first backend test attempt failed because `uv` was not on PATH; `uv` was installed in a temporary environment outside the repository and the verification above succeeded. An earlier test run caught that the existing synthetic legal-rule test inherited the new candidate marker; it was corrected to remove that marker for its explicitly synthetic test data, then the full suite passed.

## COSTS

- Model calls: 0; tokens/cost: 0.
- EUR-Lex, Commission, Safety Gate, and marketplace data requests: 0.
- `npm ci` fetched locked packages from npm; no source-data fetch was made.

## TODO_VERIFY

- The four quotations are copied from the ticket, not checked against the official EUR-Lex text. Confirm their exact wording, Article 19 subparagraphs, applicability, and mapping against Regulation (EU) 2023/988. The supplied SHA-256 digest was not independently validated against source bytes.
- No ten-record official/sample RAPEX corpus was available. The path `data/fixtures/safety_gate_samples.json` remains absent; real/sample alerts, provenance, retrieval dates, and matching quality remain unverified.
- `SPEC.md` states the 58% sweep figure itself must be verified against a primary Commission source. That source and an exact denominator/quotation are not in the repository. Do not quote the figure as established fact until sourced.
- “Zero-wrapper recall prior” is not defined as a reproducible statistic or supported result in the checked-in materials; README describes it only as a hypothesis.
- URL fetching is not implemented; URL mode records a reference and requires pasted listing text.

## DEVIATIONS

- Did not set `human_verified=true`, a retrieval timestamp, or the supplied digest in rule metadata, because no EUR-Lex fetch or human legal review occurred. The ticket strings are retained only as unverified candidates, and the gate explicitly rejects them.
- Did not invent ten Safety Gate alerts. S4 continues to abstain with no valid local corpus.
- Did not hard-code the requested “WOULD BE SUPPRESSED — Missing EU Responsible Person (GPSR Art. 19(b))” banner or enable active statutory PASS/FAIL outcomes. The UI reflects the API verdict; unverified legal rules remain `UNDETERMINED`.
- README includes the 58% figure only as a pending verification item, not as an asserted fact.

## NOT_DONE

- Human-verified statutory rule metadata and independently validated source hash: not satisfied.
- Ten real/sample Safety Gate alert fixtures: not satisfied; none were fabricated.
- Active legal PASS/FAIL verdicts and a static Art. 19(b) suppression conclusion: intentionally not satisfied; these conflict with the fail-closed evidence state.
- The UI card layout, dynamic API verdict banner, local recall comparison, and draft copy button are implemented. URL fetching is not.
- The 58% and zero-wrapper statements are not presented as verified statistics.

## NEXT

Have an authorized reviewer confirm the EUR-Lex text and digest, and have the data owner supply provenance-backed Safety Gate alerts; then validate the UI against those reviewed sources before enabling any statutory finding.
