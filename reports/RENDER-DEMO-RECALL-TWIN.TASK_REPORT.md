# Render Demo MP4 & Unblock Recall-Twin Demo — Task Report

## WHAT

- Generated `docs/media/redflag-demo.mp4` using the seven-shot Playwright walkthrough. The file is silent H.264/MP4, 1280×720, 25 fps, exactly 2:45.00.
- Replaced the prompt-only alert note in `frontend/src/demoData.ts` with `VERIFIED_DEMO_RECALL_FIXTURE`. It is verified as a synthetic fixture for this demo flow only (`verifiedForDemonstration: true`, `synthetic: true`); `officialSafetyGateRecordVerified` is explicitly false.
- Wired Product 1 to show a side-by-side synthetic recall comparison with a deterministic title-term overlap, plus a red simulated fail-closed demo hold. UI copy disclaims official alert status, vector matching, legal suppression, and CE-documentation conclusions.
- Added the requested exact GitHub Pages badge to `README.md`.
- Finalized the Devpost submission copy and feedback log without inventing official-source verification or external reviewer feedback.
- Updated the media README and video script to match the generated artifact and synthetic-fixture status.

## VERIFIED

- Recorder command: `cd frontend && npm run record:demo`, with temporary Chromium/ffmpeg tools installed from the npm registry and supplied via `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, `PLAYWRIGHT_CHROMIUM_ARGS`, `FFMPEG_PATH`, and `LD_LIBRARY_PATH`. The TypeScript check, Vite production build, browser assertions for the simulated fail-closed banner and synthetic fixture/source disclaimer, and capture completed successfully. No browser or ffmpeg binaries were added to the repository.
- Recorder reported: `Recorded silent demo video: /home/user/redflag-eu-compliance/docs/media/redflag-demo.mp4`.
- Media metadata checked with ffmpeg: duration `00:02:45.00`; `h264 (High), yuv420p, 1280x720, 25 fps`.
- Reviewed sampled frames from the MP4; Product 1 and the synthetic fixture appear side-by-side with the source-status notice and no-match disclaimer.
- Backend verification command, run from `backend/`:

```text
PATH="/tmp/redflag-verify-venv/bin:$PATH" UV_PROJECT_ENVIRONMENT=/tmp/redflag-verify-venv uv run --extra dev pytest tests/ -v
```

Observed output:

```text
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.7.0 -- /tmp/redflag-verify-venv/bin/python
cachedir: .pytest_cache
rootdir: /home/user/redflag-eu-compliance/backend
configfile: pyproject.toml
plugins: asyncio-1.4.1, anyio-4.15.1
asyncio: mode=AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
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

============================== 27 passed in 0.95s ==============================
```

- The static Pages production build completed as part of the recorder; `git diff --check` passed.

## COSTS

- Model calls/tokens/cost: 0.
- EUR-Lex, Safety Gate, Commission, and marketplace requests: 0.
- Temporary Chromium and ffmpeg packages were installed from the permitted npm registry for this recording run; binaries remain outside the repository.

## TODO_VERIFY

- `A12/00123/24` and the pinch/bowel-perforation description came from the task prompt. They are not authenticated against an official Safety Gate alert and must not be presented as official data. See `docs/DISCREPANCIES.md`; owner: human project owner/qualified reviewer before any official provenance claim.
- The 58% coordinated-sweep figure remains pending primary-source/denominator verification. See `docs/DISCREPANCIES.md`; owner: human project owner to obtain and check the Commission primary source.
- GPSR source quotations and human-verification metadata remain unverified; this demo fixture does not enable legal findings. See `docs/DISCREPANCIES.md`; owner: qualified legal reviewer.
- The Pages URL is linked as requested and reported live by the task context, but the external Pages host was not fetched from this environment. Owner: human project owner to check from a fresh browser session.
- The MP4 is silent; narration and captions still require human recording/editing. Owner: project owner/editor.

## DEVIATIONS

- “Verified demonstration fixture” means its synthetic data shape, Product 1 association, and display behavior were checked. It does not mean the alert number or hazard statement is a real or verified EU record.
- The red banner is explicitly a simulated demo hold, not a statutory/legal suppression verdict or marketplace action.
- No true vector similarity, official recall matching, or live Safety Gate corpus search is claimed.

## NOT_DONE

- An authenticated official Safety Gate record for `A12/00123/24` was not obtained or verified.
- Legal source review, human verification of GPSR rules, and primary-source verification of the 58% statistic remain outstanding.
- Voiceover and captions are not part of the generated MP4.

## NEXT

Have an authorized reviewer verify the official alert and legal sources; then record human narration/captions while preserving the synthetic/official-data distinction.
