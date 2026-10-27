# GitHub Pages Live Demo & Demo Video Automation — Task Report

## WHAT

- Set `base: '/redflag-eu-compliance/'` in `frontend/vite.config.ts` for the repository Pages path.
- Added a `VITE_STATIC_DEMO=true` branch in the React entry path, with three synthetic title-only sample cards in `frontend/src/demoData.ts` and `frontend/src/StaticDemoDashboard.tsx`. Screening is local-only and displays lexical title terms, a demo-only evidence hold, and an explicit no-legal-determination state.
- The task-supplied `A12/00123/24` string and magnetic pinch/bowel-perforation description are rendered only as an **unverified prompt-supplied reference**, not as an official alert or confirmed match. No vector result is claimed.
- Added GitHub Pages workflow `.github/workflows/deploy-pages.yml` for pushes to `main`, and `make build-pages` to build `frontend/dist` with static mode enabled.
- Replaced `video/script.md` with seven timed shots totaling exactly 165 seconds and caveats for the unverified statistic, alert reference, synthetic listings, legal rules, and offline simulation.
- Added `scripts/record-demo.ts`, which builds the static app, starts a local preview, records the seven-shot Playwright walkthrough, trims the silent capture to 165 seconds, and converts it to `docs/media/redflag-demo.mp4` using ffmpeg/libx264.
- Added `docs/DEVPOST_SUBMISSION.md`, `docs/DEVPOST_FEEDBACK.md`, and `docs/media/README.md`; no external reviewer feedback is invented.

## VERIFIED

- `make build-pages` — TypeScript check and static Vite build passed. The generated `index.html` references `/redflag-eu-compliance/assets/...`; local Pages preview returned HTTP 200 at `/redflag-eu-compliance/`.
- `cd frontend && npm run build` and `VITE_STATIC_DEMO=true npm run build` both passed.
- Inspected the static bundle: it contains all three demo product data and the prompt-supplied alert reference, and does not contain the `/v1/listings/screen` API route string.
- From `backend/`, command run:

```text
PATH="/tmp/a-t04-pages-venv/bin:$PATH" UV_PROJECT_ENVIRONMENT=/tmp/a-t04-pages-venv uv run --extra dev pytest tests/ -v
```

Exact output:

```text
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.6.0 -- /tmp/a-t04-pages-venv/bin/python
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

============================== 27 passed in 0.90s ==============================
```

- `npm run record:demo` was attempted. It built the static Pages app and started the preview, but exited before recording because Playwright's Chromium headless-shell executable is absent. The environment also has no `ffmpeg` executable, so MP4 conversion could not run. **`docs/media/redflag-demo.mp4` was not generated.**

## COSTS

- Model calls/tokens/cost: 0.
- EUR-Lex, Commission, Safety Gate, and marketplace requests: 0.
- Playwright and TSX packages were installed from the npm registry for the requested automation; browser and video binaries were not downloaded.

## TODO_VERIFY

- Verify the 13 December 2024 applicability date and the SPEC's 58% coordinated-sweep figure against primary Commission/EUR-Lex sources before using them as facts. The demo labels both as project-note claims pending source review.
- Independently verify the prompt-supplied alert number `A12/00123/24`, its origin, and the magnetic pinch/bowel-perforation description against the official Safety Gate record. No official record is included or fetched.
- The three product inputs are title-only synthetic examples, not live third-party marketplace listings.
- GitHub Pages deployment has not run from `main`; repository Pages settings and the public URL remain to be confirmed after merge.
- The video recorder requires a Playwright Chromium installation and ffmpeg with libx264. No MP4 is present until those prerequisites are supplied and recording succeeds.

## DEVIATIONS

- Did not label the prompt-supplied alert reference as official, report a vector similarity, or state that the product shares a recalled failure mode. The available S4 implementation is keyword-based and has no valid official corpus.
- The static banner is a demo-only evidence hold, not a legal suppression decision. It does not claim CE documentation is a general GPSR Article 19 requirement.
- The 58% figure is disclosed only as an unverified project-note claim; no non-compliance rate is asserted.
- The offline shot demonstrates a client-side simulation after page load, not a sandbox network-isolation test.
- The automation script and video script are implemented, but the requested MP4 artifact could not be generated in this environment.

## NOT_DONE

- GitHub Pages is configured for future deployment, but not yet confirmed live at the requested URL.
- `docs/media/redflag-demo.mp4` is not generated because the browser binary and ffmpeg are unavailable.
- Official alert verification, a true RAPEX match, vector matching, and live EUR-Lex/Safety Gate synchronization are not implemented.
- The mission's requested independent public-source claims remain unverified and are not presented as facts.

## NEXT

Install the matching Playwright Chromium browser and ffmpeg/libx264, run `cd frontend && npm run record:demo`, then merge the Pages workflow and confirm the live deployment URL from the Actions environment output.
