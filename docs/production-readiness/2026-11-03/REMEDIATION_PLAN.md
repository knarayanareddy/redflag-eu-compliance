# RedFlag remediation plan

Pinned revision `ae6c6ccc6c5d41da2fa9f97b544ae016235ea6cc`; see [REVIEW.md](REVIEW.md). All steps are **future work**. The documented abstaining state is not a configuration-independent guard; implement and verify one before changing legal rule metadata. No phase establishes certification.

## Dependencies and phases

| Phase | Tasks | Entry → exit |
|---|---|---|
| 0: baseline | T1 | Owner authorizes isolated work → reproduction record and exposure decisions |
| 1: correctness and data | T2, T3 | T1 → negative controls and clear processing boundaries |
| 2: legal feasibility | T4 | T1, T2 → enforce and test abstention before metadata changes, then source review |
| 3: automation and operations | T5 | T1-T4 → reproducible checks and deployment decision |
| 4: independent acceptance | T6 | T2-T5 → separate observed acceptance or documented rejection |

### T1 — Establish reproducible baseline (RF-04, RF-05)

**Paths:** observed `backend/pyproject.toml`, `frontend/package.json`, `.github/workflows/ci.yml`, `jobs/Dockerfile`; inspect complete `backend/app/main.py` and `frontend/src/App.tsx`, currently only partially sampled. **Prerequisite:** owner approval for isolated test environment and no real listing data.

1. Inventory call sites, configurations, lockfiles, CI logs and deployment topology at a pinned checkout; record differences from the review SHA.
2. In isolation, run existing CI-defined backend checks and frontend build; record commands and results without lowering thresholds.
3. With approval, build and start the container, observe exit, asset paths and `/health`, and establish whether Pages or a server is intended.

**Deliverable:** baseline, failure reproduction and threat model. **Verify:** another engineer checks revision and logs and reproduces claimed failures.

- [ ] Actual execution environment, results and unrun checks recorded.
- [ ] Hosting, identity, permitted data and account ownership decided; no invented container failure reported.

### T2 — Correct HTML evidence boundaries (RF-03)

**Paths:** observed `backend/app/stages/s2_extract_fields.py` and `backend/tests/test_extraction.py`. **Prerequisite:** T1 baseline.

1. Add independent fixtures with labeled data exclusively inside script/style, adjacent visible labels, mixed HTML, entities and original-source offsets.
2. Change parsing to exclude non-visible script/style content while keeping valid exact raw spans for visible content; document remaining CSS/visibility limitations rather than claiming browser-equivalent rendering.
3. Exercise extraction and the actual screening entry point with benign and adversarial cases; document baseline behavior without treating existing abstention as metadata-independent enforcement, which T4 establishes.

**Deliverable:** source and regression tests. **Verify:** demonstrate that restoring old parser behavior makes the hidden-label test fail, then rerun the applicable existing checks.

- [ ] Hidden-only labels are not emitted as visible evidence; valid visible spans still match raw text.
- [ ] Existing documented unverified-rule behavior is not regressed; malformed input is reviewed.

### T3 — Make model processing explicit and safe (RF-02, RF-05)

**Paths:** observed `backend/app/stages/s2_extract_fields.py`, `backend/app/main.py`, `frontend/src/App.tsx`, `README.md`; any configuration policy file is **proposed**. **Prerequisite:** T1 establishes the actual endpoint call chain and approved provider policy.

1. Trace every caller and distinguish deterministic-only from model-enabled requests; make outbound processing disabled by default and require an explicit authorized configuration or consent appropriate to the owner-approved deployment.
2. Bind bearer credentials to approved HTTPS provider origins, reject untrusted destinations and redirects, avoid logging credentials or raw listings, and define retention and incident ownership. Do not introduce real credentials into fixtures.
3. Align API capability disclosure, UI, README and copy/export text with actual processing; make provider failures visibly distinguishable from a completed model analysis.

**Deliverable:** enforced processing policy, clear notices and boundary tests. **Verify:** use a controlled fake transport to prove default mode has zero outbound calls, approved opt-in sends only agreed fields, and an unapproved destination receives neither text nor token; deliberately remove each guard to prove tests fail.

- [ ] Consent/configuration and credential binding reviewed.
- [ ] Local-processing claim is accurate for every exposed mode; no live vendor call implied.

### T4 — Enforce abstention, then validate feasibility (RF-01, RF-06)

**Paths:** observed `backend/app/main.py`, `backend/app/gate/gate.py`, `backend/tests/test_api.py`, `data/gpsr-rules.v0.json`, `data/safety-gate-schema.md`, `README.md`; a reviewed source register and evaluation set are **proposed**, not present in inspected evidence. **Prerequisite:** T1 and T2; qualified domain reviewer and permission to use source records. No rule metadata changes before step 1 and its verification pass.

1. Before changing rule metadata, implement an explicit screening boundary that forces `UNDETERMINED` and `gate.abstain=true` independently of rule verification metadata; ensure no legal findings or non-abstaining legal outputs escape through the endpoint while disabled. The `/v1/info` boolean alone is not a guard.
2. Through the actual `/v1/listings/screen` HTTP route, test synthetic rules whose metadata satisfies `rule_is_verified`, with every required rule verified-looking and synthetic PRESENT and sufficiently confident ABSENT inputs. Cover BLOCKING and MAJOR absent rules; assert abstention and no legal findings, and check the disclosed disabled state agrees with the response. Deliberately bypass the new boundary and show the absent-rule test fails because the old path produces a non-abstaining outcome; restore the boundary and rerun. Do not claim the PRESENT-only case necessarily fails under the old code.
3. Only after step 2 passes, record official texts, versions, retrieval dates, quotes and hashes; obtain qualified human review of each proposed mapping, applicability and exceptions. Record metadata changes without enabling legal decisions.
4. Establish a licensed, dated alert dataset and independently labeled cases, including missing, stale and no-match examples; measure held-out extraction and retrieval, false negatives and uncertainty. Verify the 58% statistic against its primary source before using it.

**Deliverable:** enforced abstention boundary, endpoint regression and mutation evidence, provenance register, expert sign-off and evaluation report. **Verify:** independently review HTTP responses and the failing boundary-bypass control; a second reviewer traces sample outputs to sources and challenges incorrect mappings. Any later enablement is a separate owner-approved, legally reviewed change, not a consequence of metadata updates.

- [ ] Source currency, data rights and reviewer identity recorded.
- [ ] Before metadata changes, verified-looking PRESENT and ABSENT cases abstain end-to-end; bypassing the boundary fails the ABSENT regression and the restored boundary passes.
- [ ] Decision to retain prototype-only claims or propose a separately approved legal feature recorded.

### T5 — Automate and choose operations (RF-04, RF-05; preventive)

**Paths:** observed `.github/workflows/ci.yml`, `jobs/Dockerfile`, `frontend/package.json`; deployment and recovery artifacts are **proposed**. **Prerequisites:** T1-T4.

1. Add regression checks for T2-T4 to existing CI after their respective changes; define a frontend accessibility/interaction test script before referencing it, and pin CI actions and base images to reviewed immutable versions.
2. If hosting is approved, package the actual required assets, select a real server entry point, define auth/authorization and network limits, minimize logs, and smoke-test the built artifact through its user-facing route. If local-only, document and test that boundary instead.
3. Establish release, health monitoring, rollback and retention policies; if persistent records are introduced, define backup credentials, encrypted storage and a real restore drill. Do not assert a restore requirement or successful drill for nonexistent storage.

**Deliverable:** CI evidence and operations decision. **Verify:** use a clean checkout, break a guard to show CI fails, and capture hosted artifact identity and health.

- [ ] CI executes meaningful negative tests, without suppressing failures.
- [ ] Exposure, secrets, dependency provenance and recovery requirements have named owners.

### T6 — Independent acceptance (all findings)

**Paths:** observed tests and workflows above; acceptance report is **proposed**. **Prerequisites:** T2-T5 complete or explicitly waived by the owner.

1. Have a reviewer not responsible for the changes replay source-to-UI flows using synthetic listings, an empty corpus and adversarial HTML; verify actual deployed code identity when applicable.
2. Re-run deliberate mutations of hidden-content, outbound-call and abstention guards; ensure independent assertions fail on broken behavior rather than mirroring implementation logic.
3. Test keyboard, focus, status announcements and narrow-screen behavior in both demo and API modes; record gaps and conduct an actual restore observation only if persistence exists.

**Deliverable:** signed acceptance record with revision, environment, observations, unresolved risks and claim limits. **Verify:** evidence links and negative-control failures are independently inspected; test counts alone are insufficient.

- [ ] Each RF finding is resolved, explicitly deferred, or accepted by a named owner.
- [ ] No legal compliance or certification claim is made from the engineering tests.

## Release and approval gate

- [ ] Owner approves hosting, provider processing, credentials, data retention and any legal claim change before implementation or release.
- [ ] Enforced abstention and endpoint negative controls precede rule metadata changes; any legal enablement requires separate owner approval and qualified legal review. Missing corpus and uncertainty remain visible.
- [ ] Release only a reviewed immutable revision with recorded CI and artifact identity. Roll back to the last approved artifact and configuration if screening, privacy or abstention controls regress; verify the rollback in the actual target environment.
- [ ] If persistent data is added, approve recovery objectives and demonstrate restore from a protected backup before relying on it. Otherwise record recovery as not applicable.
- [ ] Independent acceptance records remaining limitations; publishing, deployment, production access and enabling external integrations require separate owner authorization.
