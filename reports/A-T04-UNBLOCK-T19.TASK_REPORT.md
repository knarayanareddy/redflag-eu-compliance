# A-T04-UNBLOCK-T19 Task Report

## WHAT

- Added `backend/app/stages/s4_recall_twin.py`: deterministic local-corpus keyword retrieval, top-five candidate serialization, GTIN exact-match priority, risk-type overlap summaries, verbatim alert citation chips, and explicit `UNDETERMINED` abstention when no valid local corpus is available. It makes no network calls and does not claim that absent matches establish safety.
- Wired the stage into `POST /v1/listings/screen` in `backend/app/main.py`. The API now returns `recall_twin`, `risk_correlations`, `recall_corpus_available`, and manual-review `warnings`, with alert citations merged into `citation_chips`. Only identifiers extracted as EAN/GTIN are used for exact barcode matching. Recall output is separate from the statutory screening verdict.
- Added backend tests in `backend/tests/test_recall_twin.py` and `backend/tests/test_api.py`, including missing-corpus failure behavior, synthetic-only record matching and citations, schema checks, GTIN exact matching, and a negative-query abstention case. The alert fixture is explicitly synthetic and is not a Safety Gate record.

## VERIFIED

The first direct invocation failed because `uv` was not on PATH. I installed `uv` in a temporary environment outside the repository and ran the requested test command from `backend/` with that executable and environment selected:

```text
PATH="/tmp/a-t04-venv/bin:$PATH" UV_PROJECT_ENVIRONMENT=/tmp/a-t04-venv uv run --extra dev pytest tests/ -v
```

Exact output:

```text
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.7.0 -- /tmp/a-t04-venv/bin/python
cachedir: .pytest_cache
rootdir: /home/user/redflag-eu-compliance/backend
configfile: pyproject.toml
plugins: asyncio-1.4.1, anyio-4.15.1
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 26 items

tests/test_api.py::test_health_and_capability_disclosure PASSED          [  3%]
tests/test_api.py::test_rules_endpoint_marks_gpsr_rules_unverified PASSED [  7%]
tests/test_api.py::test_assessment_abstains_on_unverified_gpsr_rule PASSED [ 11%]
tests/test_api.py::test_assessment_rejects_extra_request_fields PASSED   [ 15%]
tests/test_api.py::test_listing_screen_exposes_fail_closed_recall_twin PASSED [ 19%]
tests/test_extraction.py::test_deterministic_extraction_emits_exact_spans_and_contract_shape PASSED [ 23%]
tests/test_extraction.py::test_html_extraction_offsets_and_quote_point_into_original_html PASSED [ 26%]
tests/test_extraction.py::test_model_present_quote_is_reanchored_and_absence_cannot_override_source PASSED [ 30%]
tests/test_extraction.py::test_model_quote_not_found_is_demoted_to_unparseable PASSED [ 34%]
tests/test_extraction.py::test_model_transport_failure_falls_back_to_deterministic PASSED [ 38%]
tests/test_extraction.py::test_empty_or_oversize_input_fails_without_partial_output PASSED [ 42%]
tests/test_extraction.py::test_eurlex_parser_stages_exact_article_without_human_verification PASSED [ 46%]
tests/test_extraction.py::test_screen_response_contains_schema_valid_fields_verdict_and_citations PASSED [ 50%]
tests/test_extraction.py::test_missing_rp_only_becomes_blocking_with_verified_test_rules PASSED [ 53%]
tests/test_gate.py::test_statutory_rule_abstains_even_when_quote_matches PASSED [ 57%]
tests/test_gate.py::test_quote_mismatch_never_becomes_a_pass PASSED      [ 61%]
tests/test_gate.py::test_gtin_check_is_deterministic_and_validates_claimed_input PASSED [ 65%]
tests/test_gate.py::test_gtin_check_abstains_when_value_is_not_in_source PASSED [ 69%]
tests/test_gate.py::test_placeholder_check_uses_artifact_not_quote_semantics PASSED [ 73%]
tests/test_gate.py::test_rule_loader_has_unique_rule_ids_and_reports_unverified_gpsr_rules PASSED [ 76%]
tests/test_recall_twin.py::test_missing_local_corpus_abstains PASSED     [ 80%]
tests/test_recall_twin.py::test_recall_result_and_alert_citations_follow_contract PASSED [ 84%]
tests/test_recall_twin.py::test_exact_gtin_match_is_returned_and_cited PASSED [ 88%]
tests/test_recall_twin.py::test_nonmatching_terms_do_not_claim_no_recall_exists PASSED [ 92%]
tests/test_schemas.py::test_core_schema_is_valid_json_schema PASSED      [ 96%]
tests/test_schemas.py::test_citation_contract_accepts_valid_and_rejects_invalid PASSED [100%]

============================== 26 passed in 0.55s ==============================
```

Additional observed checks:

- `uv run --extra dev ruff check app tests`: `All checks passed!`
- `uv run --extra dev mypy app`: `Success: no issues found in 7 source files`
- `mypy app tests` reports missing third-party `jsonschema` type stubs in three test modules; production `app` type-check is clean. No dependency was added to address this unrelated test-stub gap.

## COSTS

- Model calls: 0; tokens/cost: 0.
- Safety Gate or EUR-Lex network requests: 0.

## TODO_VERIFY

- No real Safety Gate sample corpus was present at `data/fixtures/safety_gate_samples.json`; therefore real-alert retrieval, real-data citations, and any empirical recall-twin quality remain unverified. The runtime abstains when the corpus is absent or contains no valid records.
- The local corpus record shape was implemented against `data/safety-gate-schema.md`, but no actual official source record was available to validate ingestion or source metadata.
- `data/gpsr-rules.v0.json` remains unchanged and unverified. The ticket-supplied `source_sha256` is the SHA-256 of empty bytes (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`), not a fetched EUR-Lex document hash. No legal review occurred.
- The ticket's rule-ID mapping conflicts with `data/gpsr-rules.v0.json`: RF-ART19-02 maps to responsible-person identity, RF-ART19-03/-04 to responsible-person postal/electronic contact, RF-ART19-05 to manufacturer identity, and RF-ART19-09 to warnings/safety information. Confirm the intended mapping before changing those records.
- Ticket acceptance calls for frontend recall/warning UI. The delegation protocol assigns `frontend/` to `frontend-agent`; no frontend file was edited. A frontend owner needs to consume the new API response fields.

## DEVIATIONS

- Did not inject or mark legal quotes verified, because source retrieval and human legal verification were not available and the supplied digest is not a source-document digest.
- Implemented deterministic keyword matching only, not semantic/embedding matching or a learned verdict. Similarity is explicitly labeled `keyword`; risk overlap is a human-review lead.
- Did not add or fabricate real Safety Gate fixtures. The synthetic test record is conspicuously marked as non-authoritative and lives only in the test module.
- Did not edit `data/` or `frontend/`, following the protocol's ownership lanes despite ticket acceptance requesting both.

## NOT_DONE

- Verified Article 19 quotes, source metadata, and `human_verified=true`: not satisfied.
- Real Safety Gate-backed matching and real-alert citation acceptance: not satisfied; corpus absent.
- Frontend warning/recall-twin UI: not satisfied; delegated lane restriction.
- The backend API integration and fail-closed local matching acceptance are implemented and covered by tests; that does not satisfy the full ticket acceptance above.

## NEXT

Ask the data/legal owner to provide and verify official source materials plus the real committed Safety Gate fixture corpus; ask the frontend owner to render the returned recall-twin and warning fields without presenting them as legal-compliance verdicts.
