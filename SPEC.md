# SPEC — "RedFlag": pre-flight gate for selling a product into the EU

**Idea A · Track: Best Apps and Agents · Also eligible: Best Use of Tavily ($3,000)**
**Version:** 1.0 · 26 Oct 2026 · **Build window:** Sun 26 Oct → Thu 30 Oct 2026, 19:00 CEST

> **Status: proposed future-state specification, not a description of the current build.** The implemented repository is a local evidence-gate prototype; GPSR rules are unverified and legal compliance verdicts are disabled. See `README.md` and `ARCHITECTURE.md` for implemented behavior. Do not present planned model routing, recall matching, sandbox verification, or empirical studies as completed features.

> Read `_shared/agent-delegation-protocol.md` before dispatching any ticket in this file.
> Read `_shared/judging-rubric.md` before writing any user-facing copy.

---

## 1. Executive brief

### One-sentence pain (in the persona's own words)
> *"I listed 40 products for EU customers last month. Amazon suppressed eleven of them on a Tuesday and I found
> out from an email, not from a dashboard. I still don't know which of the other twenty-nine are next."*
> — paraphrase of a marketplace seller; **replace with a real quote from ticket A-T36**

### Persona
**Sofie**, 34, runs a 3-person homeware brand in Rotterdam. Sells ~600 SKUs across bol.com, Amazon NL/DE and
her own Shopify. Not a lawyer, cannot afford one. Reads compliance emails with dread. Her actual job is choosing
products and shipping them.

Secondary persona: a **marketplace compliance analyst** screening thousands of third-party offers — they need
batch throughput, not a chat.

### The 30-second hook (memorise this; nothing may be built that doesn't serve it)
> Paste a live product listing URL.
> In ~8 seconds, top of screen, large: **"WOULD BE SUPPRESSED — 2 of 5 required fields missing."**
> Under it: **"A near-identical magnetic building toy was recalled in DE on 11 Mar 2025 for magnet ingestion
> (Safety Gate SR/xxxxx/25). Your product shares that failure mode."** — with the actual recall photo beside yours.
> Under that: **"Here is the exact information block to paste into Amazon's compliance portal."** [Copy]
> *Only then* an expandable "Why" with article-level citations.

### One takeaway
**You can find out in eight seconds whether the EU will let you sell this product — before the marketplace or
the regulator tells you.**

### The named insider insight (Quality of the Idea — say this in the video)
> **Compliance is not a checklist problem, it's a recall-prior problem.**
> The EU publishes ~4,700 product-safety alerts a year with structured risk types, failure descriptions and
> photos — a 20-year labelled dataset of exactly how products like yours actually hurt people. Every existing
> compliance tool uses it as a *blacklist* ("is my exact product recalled?"). Used as a *reasoning prior*
> ("what is the dominant failure mode for products shaped like mine, and does my listing's evidence address
> it?"), it tells you about the risk you haven't had yet. That is the part a checklist can never do.

### Track fit & prize path
- **Best Apps and Agents** — "Build any app or agent someone would actually use… Power it with Nemotron models on
  Nebius through Token Factory. Reach for Nemotron 3 Ultra when you need serious reasoning, and let Nano or Super
  handle the fast, everyday calls… We encourage you to deploy with Nebius Serverless Endpoints, or use Nebius
  Serverless Jobs for background processing." **This project does all four things, literally.**
- Prize path: Grand Prize **OR** (Track Jetson **+** Best Use of Tavily $3,000). Stacking rule forbids both.

### Why this wins against this specific field
- **Zero of 833 competitor repos** do EU product-safety compliance for sellers. (`data/competitor-subset.csv`
  lists the 124 adjacent ones — e-commerce, marketplace, listing, recall, civic — so you can see the gap yourself.)
- Your **EU location** converts directly into the thing the rubric demands: you can read EUR-Lex natively, scrape
  a Dutch marketplace, and interview three real sellers in Eindhoven/Rotterdam in an afternoon.
- The **deterministic gate is the honest core of the product**, not a hackathon conceit — Article 19 is literally
  a list of required fields.
- It uses **Sandbox network-off verification + Sandbox branching + batch + cached tokens + four model tiers with
  published costs** — the features 90% of the field ignores.

---

## 2. The problem, evidenced

**Verify every figure against the primary source before it appears in your video or README** (ticket A-T04c).
Record the retrieved URL and date in the citation registry. Several of these come from compliance-vendor blogs
and must be traced back to the Commission's own release.

| Fact | Figure | Primary source to confirm |
|---|---|---|
| GPSR fully applicable since | **13 December 2024** | EUR-Lex, Regulation (EU) 2023/988 |
| 2026 coordinated product-safety sweep: offers screened | **~1,700** offers of childcare products & articles for physical activity | European Commission release, published **7 Sept 2026** |
| …across how many marketplaces | **35** online marketplaces | same |
| …removal/compliance orders sent to marketplaces | **560** | same |
| …offers showing manufacturer + EU responsible person + product ID **together** | **only 58%** | same |
| …marketplaces registered on the Safety Gate Portal with a contact point | **91%** (vs 53% a year earlier) | same |
| Safety Gate alerts in 2025 | **4,671** — a record, **+13%** YoY | Commission Safety Gate results, published **Mar 2026** |
| Follow-up enforcement actions (withdrawals, recalls, border seizures, marketplace delistings) | **+35%** | same |
| Marketplace removal deadline after an authority order | **2 working days** | GPSR **Art. 22(4)** |
| Real fine, Czech online retailer, 4 Mar 2026 | **CZK 380,000** — responsible-person details were on the *packaging* but not on the *listing* | Czech Trade Inspection Authority decision |
| German ceilings (ProdSG §28(2), as amended 19 Feb 2026) | up to **€10,000** ordinary offences; up to **€100,000** for failing to take corrective action on a dangerous product | German Product Safety Act |
| Netherlands | **~€1,050** for a routine administrative breach | Dutch implementation act |
| Italy | €100,000, **+50% (€150,000)** where there is a serious risk | Italian implementation |
| Ireland | up to **€500,000** | Irish implementation |
| France | up to **€600,000** (individuals) / **€3,000,000** (companies) / up to **10% of turnover** for Art. 19 failures | French implementation |
| Poland | up to **1,000,000 PLN** (manufacturers, importers, platform providers); 500,000 PLN ceiling for distributors | Polish implementation |
| Platform enforcement | Amazon automated suppression of non-compliant ASINs from Q1 2026 with 48-hour windows; DE BAuA + FR DGCCRF jointly flagged **2,000+ ASINs** for missing EU Responsible Person data (June 2026) | Confirm from Amazon Seller Central policy pages / national authority releases |
| Adjacent regulatory pressure | Commission fined **Temu €200M under the DSA on 27 May 2026** — first DSA penalty for failing to assess risks of illegal/dangerous products; a rival marketplace fined **€550M** in July 2026 | Commission press releases |

> ⚠️ **Do not use the widely-repeated claim that GPSR fines reach "4% of worldwide turnover."** It circulates in
> compliance blogs, has **no source in the Regulation**, and GPSR Art. 44 sets no figure at all — it delegates
> penalties to member states. Saying this correctly, and saying that you checked, *is itself the insider insight*.

### The legal spine (Phase 0 must read these from EUR-Lex verbatim)

| Provision | What it does | Where it enters the product |
|---|---|---|
| **Regulation (EU) 2023/988 (GPSR)** | General product safety; applies from 13 Dec 2024; replaces Directive 2001/16/EC… *(verify)* | The whole product |
| **Art. 4** + **Art. 4 of Reg. (EU) 2019/1020** | Who the **responsible economic operator established in the Union** is (manufacturer if in EU, else importer, else authorised representative, else fulfilment provider, else another mandated person) | The single most-missed field |
| **Art. 9** | Manufacturer duties: type/batch/serial identifier on the product, name + trademark + postal address + electronic contact, instructions & safety information in the member-state language, internal incident register | Feeds the identifier + warnings checks |
| **Art. 19** | **Information to be provided in the case of distance sales** — what an online offer must display, clearly, *prior to* conclusion of the contract | **The core rule table** |
| **Art. 22** | Obligations of **providers of online marketplaces**: register on the Safety Gate Portal, single point of contact, act on orders within **2 working days**, best-efforts assessment, ensure listings carry the Art. 19 traceability information | Explains *why* the marketplace suppresses your listing before any authority acts |
| **Art. 44** | Penalties — set by member states, must be "effective, proportionate and dissuasive" | The consequence line, per destination country |

**Integrity rule:** the rule table's `source_quote` field must be **copied verbatim from the EUR-Lex text** by an
agent that fetched it, with the fetch URL and timestamp recorded. **Never write these quotes from memory.** A
human spot-checks 5 of them. A misquoted statute in a legal-compliance tool is an instant credibility loss.

---

## 3. Success criteria, mapped to the four judging criteria

| Criterion | How RedFlag earns it | Measurable target |
|---|---|---|
| **Technological Implementation (25%)** | 4 Nemotron tiers with published per-stage cost; **Sandbox with guest networking disabled** verifying the generated compliance pack; **Sandbox branching** for a gate-on/gate-off A/B; **Cached Tokens** on the repeated legal preamble with measured savings; **Serverless Job** for the 200-listing batch; **Serverless Endpoint** for the deployed backend; structured JSON output on every model call; a complete cost/latency/token ledger | Ledger covers ≥95% of model calls; A/B chart published; all-Ultra counterfactual cost published |
| **Design (25%)** | Verdict + action above the fold, evidence collapsed; custom safety-signage design system; every async action has progress **and** stop; onboarding samples; concurrent-safe public demo; full keyboard nav | Stranger reaches aha in **≤60 s** (test on 3 people outside the team, timed) |
| **Potential Impact (25%)** | Commission's own 58% / 560-orders / 4,671-alerts numbers on screen; **3 real seller interviews**; **batch study over 150–250 real live listings producing original aggregate statistics** | ≥1 real quote with permission; batch n≥150 with per-field non-compliance rates |
| **Quality of the Idea (25%)** | The recall-prior insight; a gate that demonstrably rejects uncited claims; **abstention** (UNDETERMINED) implemented and shown on camera; zero direct competitors | Gate rejection shown live in the video; abstention shown on a benign/thin-evidence input |

---

## 4. Architecture

```
                        ┌────────────────────────────────────────────────────────────┐
   user pastes URL      │                        FRONTEND (React)                    │
   or picks a sample ──►│  /check   verdict card (above fold) → [Copy for Amazon]     │
                        │           evidence drawer (collapsed) · citation pills      │
                        │           progress + STOP · run history · batch report      │
                        └───────────────▲───────────────────────┬────────────────────┘
                                        │ SSE run events         │ POST /api/check
                        ┌───────────────┴───────────────────────▼────────────────────┐
                        │              BACKEND (FastAPI, Nebius Serverless Endpoint)  │
                        │                                                            │
   S1 fetch_listing ───►│  Playwright/httpx → ListingSnapshot (text+images+metadata) │
                        │        │                                                   │
   S2 extract_fields ──►│  Nemotron NANO + JSON schema → ListingFields               │
                        │        │        (presence/absence + evidence span per field)│
                        │        │                                                   │
   S3 applicability ───►│  Nemotron ULTRA → ObligationSet                            │
                        │        │   (only when S2 confidence < 0.75 or category is  │
                        │        │    regulated) — OTHERWISE SKIP, log the saving     │
                        │        │                                                   │
   S4 recall_twin ─────►│  embeddings → DuckDB vector search over Safety Gate corpus │
                        │            → top-k alerts                                  │
                        │            → Nemotron SUPER: does my product share the     │
                        │              failure mode? (must cite alert IDs)           │
                        │        │                                                   │
   S5 live_currency ───►│  TAVILY: is the cited harmonised standard current?         │
                        │            national penalty rules? new guidance?           │
                        │            (runtime, load-bearing, logged)                 │
                        │        │                                                   │
   S6 gate ────────────►│  DETERMINISTIC (pure Python, no LLM):                      │
                        │            • every finding has ≥1 resolvable citation      │
                        │            • citation TTL not expired                      │
                        │            • responsible-person country ∈ EU-27 (+EEA)     │
                        │            • EAN-13/GTIN checksum                          │
                        │            • warning language codes ⊇ destination countries│
                        │            • no placeholder/lorem text survived            │
                        │            • confidence ≥ threshold                        │
                        │        → Verdict ∈ {WOULD_BE_SUPPRESSED, AT_RISK,          │
                        │                     COMPLIANT, UNDETERMINED}               │
                        │        │                                                   │
   S7 artifact ────────►│  TOKEN FACTORY SANDBOX                                     │
                        │     image: rules table + validator + template pack         │
                        │     run:   generate compliance pack (marketplace blocks,   │
                        │            multilingual warnings, printable label sheet)   │
                        │     run:   VALIDATOR with guest network DISABLED           │
                        │     out:   bytes + SHA-256, downloaded and re-hashed       │
                        │                                                            │
   CROSS-CUTTING ──────►│  CITATION REGISTRY (ids → locator, quote, retrieved_at,    │
                        │                    sha256, ttl, trust)                     │
                        │  LEDGER (runs/ledger.jsonl — every model/tool/sandbox call:│
                        │          tokens, cached tokens, cost, latency, status)     │
                        └────────────────────────────────────────────────────────────┘

   BATCH LANE (Nebius Serverless Job, overnight):
     jobs/batch_run.py → S1→S6 over N listings → runs/reports/batch-YYYYMMDD.json + charts
     published as: "of 214 live listings in <category>, X% were missing the EU responsible person…"

   A/B LANE (Token Factory Sandboxes branching):
     save image(rules+testset) ──┬── branch gate_on  → run 120 cases → false-accept rate
                                └── branch gate_off → run 120 cases → false-accept rate
     published as a bar chart in README + video
```

### Component inventory (and why each earns its place — Jackie's test)

| Component | Justified by the 30-second hook? | If not, cut |
|---|---|---|
| `fetch_listing` | Yes — "paste a URL" is the hook | — |
| `extract_fields` | Yes — "2 of 5 required fields missing" | — |
| `applicability` | Yes — needed so Nano isn't asked to be a lawyer | — |
| `recall_twin` | **Yes — this is the wow** | Never cut |
| `live_currency` (Tavily) | Yes — and it's the $3,000 bonus prize | — |
| `gate` | Yes — it's the trust mechanism | — |
| `artifact` + Sandbox | Yes — "here is the text to paste" is the action | — |
| Batch job | Yes — converts demo into study | Shrink to n=50 if late |
| A/B branch | Yes — proves the gate works | Nice-to-have; keep if time |
| User accounts / login | **No** | **CUT** — also breaks the "free and unrestricted" rule |
| Vector DB server | **No** — DuckDB + a Parquet file is enough | **CUT** |
| Multi-language UI | **No** — multilingual *output* yes, multilingual *UI* no | **CUT** |
| Slack/Email notifications | **No** | **CUT** (list in Next Steps) |
| Browser extension | **No** — Telltale's judges asked for one; put it in Next Steps | **CUT** (say it in the video) |

---

## 5. Data model

Frozen in Phase 1 at `schemas/core-schemas.json`. **Changing a schema after Phase 1 requires its own ticket that
updates every consumer in the same commit.**

### 5.1 `ListingSnapshot` (output of S1)
```json
{
  "id": "ls_01J...",
  "source_url": "https://www.bol.com/nl/nl/p/…",
  "marketplace": "bol.com | amazon.nl | amazon.de | ebay | etsy | shopify | other | fixture",
  "fetched_at": "2026-10-27T09:14:02Z",
  "fetch_mode": "live | fixture",
  "title": "…",
  "brand": "… | null",
  "description_html": "…",
  "description_text": "…",
  "bullet_points": ["…"],
  "price_eur": 24.95,
  "currency": "EUR",
  "destination_countries": ["NL","DE"],
  "category_breadcrumb": ["Baby & Peuter", "Speelgoed", "Bouwspeelgoed"],
  "images": [{"url":"…","sha256":"…","role":"hero|packaging|warning|other"}],
  "seller_block_text": "… | null",
  "compliance_block_text": "… | null",
  "spec_table": [{"k":"EAN","v":"8712345678906"}],
  "raw_html_sha256": "…",
  "is_fixture": false
}
```

### 5.2 `ListingFields` (output of S2 — Nano + JSON schema)
Every field carries **presence**, an **evidence span** (so a human can check), and a **confidence**.
```json
{
  "listing_id": "ls_01J...",
  "fields": {
    "product_identifier": {
      "status": "PRESENT | ABSENT | AMBIGUOUS | UNPARSEABLE",
      "value": "8712345678906",
      "identifier_kind": "ean13 | gtin | model | batch | serial | other | none",
      "evidence_span": {"source": "spec_table|description|images|seller_block", "quote": "EAN: 8712345678906", "char_start": 0, "char_end": 22},
      "confidence": 0.97
    },
    "manufacturer_identity":        {"status":"…","value":"…","evidence_span":{…},"confidence":0.0},
    "manufacturer_contact_postal":  {"status":"…","value":"…","evidence_span":{…},"confidence":0.0},
    "manufacturer_contact_electronic":{"status":"…","value":"…","evidence_span":{…},"confidence":0.0},
    "responsible_person_identity":  {"status":"…","value":"…","evidence_span":{…},"confidence":0.0},
    "responsible_person_postal":    {"status":"…","value":"…","country_iso":"NL","in_eu27":true,"evidence_span":{…},"confidence":0.0},
    "responsible_person_electronic":{"status":"…","value":"…","evidence_span":{…},"confidence":0.0},
    "product_image_present":        {"status":"…","value":true,"evidence_span":{…},"confidence":0.0},
    "warnings_or_safety_info":      {"status":"…","value":["Niet geschikt voor kinderen onder 36 maanden"],"languages_detected":["nl"],"evidence_span":{…},"confidence":0.0},
    "instructions_language_ok":     {"status":"…","value":true,"evidence_span":{…},"confidence":0.0}
  },
  "model": "nvidia/nemotron-3-nano",
  "schema_ok": true,
  "ledger_id": "led_01J..."
}
```

### 5.3 `ObligationSet` (output of S3 — Ultra)
```json
{
  "listing_id": "ls_…",
  "product_class": "toy | childcare | electrical | battery_containing | magnet_containing | cosmetic_adjacent | food_contact | textile | other",
  "age_grading": "0-3 | 3-6 | 6-12 | 12+ | n/a",
  "harmonisation_legislation_applies": ["2009/48/EC (Toy Safety)"],
  "applicable_obligations": [
    {"rule_id":"RF-ART19-01","applies":true,"reason":"distance sale to EU consumers","citation_ids":["cit_03"]}
  ],
  "extra_warnings_required": ["choking hazard — small parts","magnet ingestion warning"],
  "destination_language_requirements": [{"country":"NL","language":"nl"},{"country":"DE","language":"de"}],
  "applicability_confidence": 0.88,
  "abstain": false,
  "abstain_reason": null
}
```

### 5.4 `RecallTwin` (output of S4)
```json
{
  "listing_id": "ls_…",
  "candidates": [
    {
      "alert_number": "SR/02365/26",
      "publication_date": "2025-03-11",
      "notifying_country": "DE",
      "country_of_origin": "CN",
      "category": "Toys",
      "product": "Magnetic building set",
      "brand": "…", "barcode": "…",
      "risk_types": ["INGESTION","CHOKING"],
      "danger_verbatim": "…",
      "measures": "Recall of the product from end users",
      "image_urls": ["…"],
      "alert_url": "https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/…",
      "similarity": 0.83,
      "similarity_basis": "embedding_cosine"
    }
  ],
  "shared_failure_mode": {
    "verdict": "SHARES | POSSIBLY_SHARES | DOES_NOT_SHARE | UNDETERMINED",
    "reasoning": "…",
    "cited_alert_numbers": ["SR/02365/26"],
    "required_by_gate": "reasoning must reference ≥1 cited_alert_number that exists in candidates"
  }
}
```

### 5.5 `Verdict` (output of S6 — the gate; deterministic)
```json
{
  "run_id": "run_01J…",
  "listing_id": "ls_…",
  "verdict": "WOULD_BE_SUPPRESSED | AT_RISK | COMPLIANT | UNDETERMINED",
  "headline": "2 of 5 required fields missing",
  "action_first": {
    "primary": "Add the EU responsible person block to your listing",
    "copy_targets": [
      {"marketplace":"amazon","label":"Amazon Product Compliance field block","text":"…"},
      {"marketplace":"bol","label":"bol.com Productveiligheid block","text":"…"}
    ],
    "deadline_hint": "Marketplaces typically allow 14–30 days after a compliance notice; an authority order gives the marketplace 2 working days (Art. 22(4))"
  },
  "findings": [
    {
      "id":"f_01","severity":"BLOCKING|MAJOR|MINOR|INFO",
      "rule_id":"RF-ART19-02",
      "statement":"No economic operator established in the Union is identified on the offer",
      "citation_ids":["cit_03","cit_07"],
      "gate_checks_passed":["citation_resolves","citation_not_expired"],
      "evidence":{"quote":"…","source":"listing"},
      "fix":"Add name, registered trademark, postal address and electronic contact of your EU responsible person"
    }
  ],
  "gate": {
    "checks_run": 14, "checks_passed": 12, "checks_failed": 2,
    "rejected_claims": [{"claim":"…","reason":"citation_missing"}],
    "abstain": false,
    "abstain_reason": null
  },
  "artifact": {"sha256":"…","bytes":48213,"generated_in_sandbox":true,"network_disabled_during_validation":true,"sandbox_operation_id":"…"},
  "cost": {"total_usd":0.041,"by_model":{"nano":0.002,"super":0.009,"ultra":0.030},"tavily_calls":3,"cached_token_savings_usd":0.006},
  "timings_ms": {"fetch":1820,"extract":910,"applicability":4180,"recall_twin":2260,"tavily":1440,"gate":3,"artifact":6120,"total":16733}
}
```

### 5.6 `Rule` (the deterministic rule table — `data/gpsr-rules.v0.json`)
```json
{
  "rule_id": "RF-ART19-02",
  "field_key": "responsible_person_identity",
  "title": "EU responsible economic operator identified on the offer",
  "legal_basis": {"instrument":"Regulation (EU) 2023/988","article":"Art. 19(…)","verify":"REQUIRED — copy exact paragraph from EUR-Lex in A-T04"},
  "source_quote": "«VERBATIM FROM EUR-Lex — MUST BE FETCHED, NEVER WRITTEN FROM MEMORY»",
  "source_url": "https://eur-lex.europa.eu/eli/reg/2023/988/oj/eng",
  "source_retrieved_at": null,
  "applies_when": {"distance_sale": true, "destination_in_eu": true},
  "severity_if_missing": "BLOCKING",
  "detector": "field_presence",
  "validators": ["eu27_or_eea_country", "non_placeholder_text", "has_postal", "has_electronic"],
  "fix_template": "Add: {responsible_person_name}, {registered_trademark}, {postal_address}, {electronic_contact}",
  "marketplace_mapping": {"amazon":"Product Compliance → EU Responsible Person","bol":"Productveiligheid → Verantwoordelijke economische acteur","ebay":"Item specifics → EU responsible person"},
  "human_verified": false,
  "human_verified_by": null,
  "human_verified_at": null
}
```

---

## 6. Model & platform usage matrix (this table goes in README and in the video)

| Model / feature | Stage | Job | Why this tier | Measured (fill in) |
|---|---|---|---|---|
| Nemotron 3 **Nano** | S2 extract_fields; S4 pre-filter | High-volume field extraction, JSON-schema constrained | Cheapest; the task is extraction not reasoning | cost/call, p95 latency |
| Nemotron 3 **Super** | S4 recall_twin reasoning | "Does my product share this alert's failure mode?" over top-k | Mid-tier is sufficient for matching; ~10× cheaper than Ultra | |
| Nemotron 3 **Ultra** | S3 applicability; final verdict on flagged items | Which obligations apply; multi-standard reasoning | Only ~15% of items need it — **and we only invoke it when Nano's confidence < 0.75 or the category is regulated** | |
| Vision model | S2 (photo → CE mark / warning label / small-parts hazard detection) | Evidence the listing text can't give | | |
| Embedding model | S4 candidate retrieval | Semantic match over ~20 years of alerts | | |
| **Structured output / JSON mode** | S2, S3, S4 | Makes the deterministic gate possible | | schema-violation rate |
| **Cached Tokens** | All stages | The GPSR legal preamble is repeated in every call | | cache-hit %, $ saved |
| **Token Factory Sandboxes** | S7 | Generate + validate the compliance pack **with guest networking disabled**; download bytes and hash | Proves the artifact is self-consistent and not silently calling the internet | |
| **Sandboxes branching** | A/B | One immutable image → `gate_on` and `gate_off` branches → same 120 cases → false-accept delta | Turns a claim into an experiment | |
| **Serverless Job** | Batch | 150–250 live listings overnight → original aggregate statistics | Track text explicitly encourages this | n, % non-compliant per field |
| **Serverless Endpoint** | Deploy | Host the backend at a public URL through judging | Track text explicitly encourages this | |
| **Tavily** | S5 | Runtime check: is the cited harmonised standard current? national penalty rules? new guidance? | Load-bearing, not decoration → Best Use of Tavily | calls, $, % results used |

---

## 7. The deterministic gate — pseudocode

```python
# backend/app/gate/gate.py  — PURE PYTHON. NO LLM CALLS INSIDE THIS MODULE.

VERDICT_ORDER = ["WOULD_BE_SUPPRESSED", "AT_RISK", "COMPLIANT", "UNDETERMINED"]

def evaluate(listing, fields, obligations, twins, tavily, rules) -> Verdict:
    checks, rejected = [], []

    # 1. Every finding must cite something that resolves and is fresh.
    for claim in proposed_findings(fields, obligations, twins, tavily, rules):
        cites = [citations.get(c) for c in claim.citation_ids]
        if any(c is None for c in cites):
            rejected.append(Rejected(claim, "citation_missing")); continue
        if any(c.expired(now()) for c in cites if c.ttl_seconds):
            rejected.append(Rejected(claim, "citation_expired")); continue
        if claim.requires_quote and not any(c.quote and c.quote.strip() for c in cites):
            rejected.append(Rejected(claim, "citation_has_no_quote")); continue
        checks.append(Passed(claim))

    # 2. Numbers must come from measurements, never from model prose.
    if fields.ean and not ean13_checksum_ok(fields.ean):
        checks.append(Finding("RF-ID-CHK", "BLOCKING", "Identifier fails EAN-13 checksum"))
    if fields.responsible_person_postal.country_iso:
        if fields.responsible_person_postal.country_iso not in EU27_PLUS_EEA:
            checks.append(Finding("RF-RP-EU", "BLOCKING", "Responsible person is not established in the Union"))

    # 3. Warning languages must cover destination countries.
    required = {lang_for(c) for c in listing.destination_countries}
    have = set(fields.warnings.languages_detected)
    if required - have:
        checks.append(Finding("RF-LANG", "MAJOR", f"Warnings missing for {sorted(required-have)}"))

    # 4. No placeholder survived into the artifact.
    if PLACEHOLDER_RE.search(artifact_text):
        checks.append(Finding("RF-PLACEHOLDER", "BLOCKING", "Generated pack still contains placeholder text"))

    # 5. Abstain loudly rather than guess.
    if obligations.abstain or obligations.applicability_confidence < 0.60:
        return Verdict("UNDETERMINED", abstain=True,
                       abstain_reason=obligations.abstain_reason or "applicability_confidence_below_threshold",
                       action_first="We could not establish which obligations apply. Do not rely on this run — "
                                    "see LIMITATIONS.md §abstention. Escalate to a compliance professional.")
    if twins.shared_failure_mode.verdict == "UNDETERMINED" and listing.category_is_high_risk:
        return Verdict("UNDETERMINED", abstain=True, abstain_reason="recall_twin_undetermined_high_risk_category")

    # 6. Verdict from severity, deterministically.
    blocking = [f for f in checks if f.severity == "BLOCKING" and f.passed is False]
    major    = [f for f in checks if f.severity == "MAJOR"    and f.passed is False]
    if blocking: return Verdict("WOULD_BE_SUPPRESSED", findings=checks, rejected=rejected)
    if major:    return Verdict("AT_RISK",             findings=checks, rejected=rejected)
    return Verdict("COMPLIANT", findings=checks, rejected=rejected)
```

**The gate must be shown rejecting something on camera.** Prepare a fixture where a plausible-looking finding has
no citation, and show `gate.rejected_claims` populated. This directly answers Suchismita's question to Telltale:
*"what happens when the evidence is thin?"*

---

## 8. Repository layout

Exactly as in `_shared/platform-capabilities.md §7`, plus:

```
backend/app/stages/
  s1_fetch_listing.py   s2_extract_fields.py   s3_applicability.py
  s4_recall_twin.py     s5_live_currency.py    s6_gate.py         s7_artifact.py
backend/app/gate/{gate.py,rules_loader.py,validators.py}
backend/app/sandbox/{client.py,images.py,branching.py,artifacts.py}
backend/app/tools/tavily.py
backend/app/citations.py        backend/app/tf/{client.py,ledger.py,cache.py}
data/rules/gpsr-rules.json      data/corpus/safety_gate.duckdb
data/fixtures/listings/*.json   data/fixtures/gate_rejections/*.json
jobs/{Dockerfile,batch_run.py}  frontend/src/{tokens.css,routes/,components/}
runs/{ledger.jsonl,reports/,artifacts/}
```

---

## 9. Phase plan & exit criteria

| Phase | Window | Exit criterion (gate) |
|---|---|---|
| **0 — Commit & de-risk** | Sun 26 Oct, now → 23:00 | Repo public + `LICENSE` at root + CI green; credits confirmed; `data/model-catalog.snapshot.json` committed; Safety Gate endpoint returns ≥1 parsed alert; `tokens.css` authored; rules table v0 committed with ≥8 rules; hook doc written; 10 fixtures cached |
| **1 — Contracts** | Sun 23:00 → Mon 09:00 | Schemas frozen; citation registry + ledger live; every stage has a golden-fixture test; `make check` green from a clean clone |
| **2 — Spine** | Mon 09:00 → Mon 23:00 | **One real listing → verdict card on screen, end to end.** Screen-record it. Ugly is fine, incomplete is not |
| **3 — Proof** | Tue 28 Oct all day | Sandbox artifact validated with network off + hashed; branch A/B numbers; batch job launched (n≥150); ledger aggregates incl. all-Ultra counterfactual; eval set scored; 3 interviews done |
| **4 — Polish** | Wed 29 Oct 08:00 → 16:00 | **FEATURE FREEZE.** All UI states; accessibility pass; deployed; demo reachable from fresh incognito on another device; LIMITATIONS has real numbers |
| **5 — Package** | Wed 16:00 → Thu 30 Oct 18:00 | Video ≤2:50 public; README complete; Devpost copy + feedback written; clean-clone test passed; **SUBMITTED** |

---

## 10. Task tickets

> Dispatch format: give the agent the ticket block + the listed CONTEXT files + the rules block from
> `_shared/agent-delegation-protocol.md §2`.

### Phase 0 — Commit & de-risk (Sun 26 Oct)

```
ID: A-T01   TITLE: Bootstrap repo, licence, CI, Makefile
PHASE: 0    OWNER: devops-agent   DEPENDS_ON: —   BLOCKS: everything
CONTEXT: _shared/platform-capabilities.md §7 ; _shared/submission-checklist.md §A
DELIVERABLE: repo root with LICENSE (Apache-2.0), README.md stub, .gitignore, .env.example,
             Makefile (check/lint/test/run/deploy/batch), .github/workflows/ci.yml,
             backend/pyproject.toml (uv), frontend/package.json
SPEC: Layout per §8. CI runs ruff + pytest + tsc --noEmit + vite build on every push.
      .env.example lists NEBIUS_API_KEY, NEBIUS_BASE_URL, NEBIUS_MODEL_{NANO,SUPER,ULTRA,VISION,EMBED},
      TAVILY_API_KEY, SANDBOX_PROJECT_ID, and NOTHING ELSE. .env in .gitignore.
      Makefile target `check` = lint + typecheck + test + build.
ACCEPTANCE: `make check` passes on an empty skeleton; LICENSE renders on the repo page top;
            a fresh clone + `uv sync && npm ci && make check` succeeds.
VERIFY: git clone <url> /tmp/t && cd /tmp/t && make check
```

```
ID: A-T02   TITLE: Confirm credits and snapshot the authenticated model catalog
PHASE: 0    OWNER: backend-agent  DEPENDS_ON: A-T01   BLOCKS: A-T06, A-T09
CONTEXT: _shared/platform-capabilities.md §1, §2
DELIVERABLE: scripts/snapshot_catalog.py ; data/model-catalog.snapshot.json ; docs/MODEL-USAGE.md (skeleton)
SPEC: Call the authenticated /v1/models endpoint on Token Factory. Dump every model with id, context length,
      pricing fields as returned, and any capability flags. Then make ONE trivial chat completion against
      Nemotron 3 Ultra, Nano and Super each, and log all three to runs/ledger.jsonl.
      Write into docs/MODEL-USAGE.md the exact IDs you will pin.
ACCEPTANCE: snapshot committed; three ledger lines exist with real token counts and cost_usd > 0;
           the three model IDs appear verbatim in .env.example comments.
VERIFY: jq -r '.[].id' data/model-catalog.snapshot.json | grep -i nemotron | head
TODO_VERIFY: If any Nemotron tier is absent from your catalog, record it in docs/DISCREPANCIES.md and pick the
             nearest available NVIDIA open model — the rules require ≥1 NVIDIA open-source model, not specifically Ultra.
```

```
ID: A-T03   TITLE: Author the design system (tokens.css) — NOT a stock theme
PHASE: 0    OWNER: frontend-agent DEPENDS_ON: A-T01   BLOCKS: A-T13, A-T23
CONTEXT: _shared/judging-rubric.md §3 (the "Claude-built app" quote) ; _shared/agent-delegation-protocol.md §6 (design fragment)
DELIVERABLE: frontend/src/tokens.css ; frontend/src/components/primitives.tsx ; docs/DESIGN.md
SPEC: Brief = EU safety signage + customs paperwork. Palette: hazard amber #FFB300, Safety-Gate red #D32F2F,
      deep slate #12161C, paper white #F7F5F0, plus a compliant-green #1B7F4B and an undetermined-grey #6B7280.
      Type: heavy grotesque display face for verdicts (Archivo / Space Grotesk via a self-hosted or system stack —
      NO external font CDN, the demo must not depend on third-party network at judge time), monospace for
      citations and field values (ui-monospace stack). 4px spacing scale. Radii 2px and 8px only — hard-edged,
      bureaucratic, not soft-SaaS. Dark theme default, light theme available.
      Primitives: VerdictBanner, SeverityChip, CitationPill, FieldRow, CopyButton, ProgressRail, StopButton,
      EvidenceDrawer, StatBlock, MarketplaceSegmentedControl.
      FORBIDDEN: purple→pink gradients; glassmorphism/blur; emoji as iconography; centred hero + 3 feature cards;
      raw Tailwind colour classes in components (components may only use var(--…)); lorem ipsum anywhere.
ACCEPTANCE: docs/DESIGN.md explains the metaphor in 5 sentences; every primitive renders in both themes in a
            Storybook-less /dev/tokens route; a screenshot of the verdict banner is committed to docs/img/.
VERIFY: cd frontend && npm run build && npx tsc --noEmit
```

```
ID: A-T04   TITLE: Build the GPSR rule table v0 from EUR-Lex (verbatim, fetched)
PHASE: 0    OWNER: data-agent     DEPENDS_ON: A-T01   BLOCKS: A-T10, A-T21
CONTEXT: SPEC §2, §5.6 ; _shared/agent-delegation-protocol.md §4 (cite-or-abstain)
DELIVERABLE: data/rules/gpsr-rules.json ; scripts/fetch_eurlex.py ; docs/LEGAL-SOURCES.md
SPEC: Fetch Regulation (EU) 2023/988 from https://eur-lex.europa.eu/eli/reg/2023/988/oj/eng .
      Extract Articles 4, 9, 19, 22 and 44. Copy each relevant sub-paragraph VERBATIM into source_quote.
      Record source_url, source_retrieved_at and sha256 of the fetched document.
      Produce ≥12 rules: RF-ART19-01..0n (each required field of the distance-sales offer),
      RF-ART4-* (who the responsible person may be), RF-ART9-* (identifier, contact, instructions language),
      RF-ART22-* (why the marketplace acts within 2 working days), RF-LANG-* (destination language),
      RF-ID-CHK (EAN-13 checksum), RF-RP-EU (EU-27/EEA residency), RF-PLACEHOLDER.
      Every rule: applies_when, severity_if_missing, detector, validators, fix_template, marketplace_mapping.
      human_verified = false for all. A HUMAN then verifies ≥5 and sets the flags (A-T04c).
      ⚠️ NEVER write a source_quote from memory. If the fetch fails, the rule gets
      source_quote: "TODO_VERIFY(EUR-Lex Art. …)" and is EXCLUDED from the gate until filled.
ACCEPTANCE: ≥12 rules with non-empty source_quote that is not TODO_VERIFY; sha256 of the fetched text committed;
            docs/LEGAL-SOURCES.md lists each article with the URL and retrieval timestamp.
VERIFY: jq '[.rules[] | select(.source_quote|startswith("TODO_VERIFY"))] | length' data/rules/gpsr-rules.json
```

```
ID: A-T04c  TITLE: Human spot-check of 5 legal quotes (HUMAN TASK, not an agent)
PHASE: 0    OWNER: human (legal-minded teammate)  DEPENDS_ON: A-T04  BLOCKS: A-T21
SPEC: Open EUR-Lex yourself. Verify 5 rules' source_quote is verbatim and the article number is right.
      Set human_verified=true, your name, and the timestamp. Fix any mismatch.
ACCEPTANCE: 5 rules flagged verified; a short note in docs/LEGAL-SOURCES.md on what you corrected.
```

```
ID: A-T05   TITLE: Safety Gate / RAPEX ingestion spike (de-risk the corpus TODAY)
PHASE: 0    OWNER: data-agent     DEPENDS_ON: A-T01   BLOCKS: A-T14, A-T19
CONTEXT: data/safety-gate-schema.md
DELIVERABLE: scripts/fetch_safety_gate.py ; data/corpus/safety_gate_sample.parquet ; docs/DATA-SOURCES.md
SPEC: The public endpoints to try, in order:
        (a) https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en   (weekly XML, no key)
        (b) the JSON API the portal itself uses (discover it in the browser devtools Network tab)
        (c) the data.europa.eu dataset registration for RAPEX
      Parse ONE weekly report end to end. Confirm these fields populate: alert number/reference, publication
      date, notifying country, product category, product name, brand, model, barcode, risk type(s), danger
      (verbatim), measures, country of origin, image URLs, alert detail URL.
      Write the parsed rows to Parquet. Commit the sample (it is public EU data — confirm licence in
      docs/DATA-SOURCES.md; EU data is generally reusable under CC-BY-4.0, verify and attribute).
ACCEPTANCE: ≥30 parsed alerts in the sample Parquet with risk_types and danger populated for ≥90% of rows;
            docs/DATA-SOURCES.md records the working endpoint, the retrieval date, and the reuse licence.
VERIFY: python -c "import pandas as pd; d=pd.read_parquet('data/corpus/safety_gate_sample.parquet'); print(len(d), d.columns.tolist())"
KILL CRITERION: if by Sun 20:00 no endpoint yields parseable alerts, escalate — SPEC §20 pivot P1 activates.
```

```
ID: A-T06   TITLE: Token Factory client wrapper + append-only ledger + cached-token accounting
PHASE: 0    OWNER: backend-agent  DEPENDS_ON: A-T02   BLOCKS: all stages
CONTEXT: _shared/platform-capabilities.md §2, §7 (ledger contract)
DELIVERABLE: backend/app/tf/client.py ; backend/app/tf/ledger.py ; backend/app/tf/cache.py ;
             backend/tests/test_ledger.py
SPEC: One async wrapper around chat.completions and embeddings. It MUST: pin the model from env; enforce
      response_format/JSON schema where requested; retry with exponential backoff on 429/5xx respecting the
      documented rate limits; time every call; append one ledger line per call exactly per the contract;
      capture usage incl. cached tokens; classify status ∈ ok|error|truncated|schema_violation|gate_rejected.
      cache.py: structure the system prompt so the static legal preamble is a stable prefix (maximise cache hits)
      and compute savings_usd from cached vs uncached price.
      ledger.py exposes aggregates(): totals by model and stage, p50/p95 latency, cache-hit rate, failure counts,
      and a counterfactual cost of routing EVERY stage to Ultra.
ACCEPTANCE: 10 calls in a test produce 10 well-formed ledger lines; aggregates() returns a real number for
            all_ultra_counterfactual_usd; a truncated response is classified as "truncated", not "ok".
VERIFY: cd backend && uv run pytest tests/test_ledger.py -q
```

```
ID: A-T07   TITLE: Write the hook doc, persona doc and the one-sentence insight (CONTENT)
PHASE: 0    OWNER: content-agent  DEPENDS_ON: —   BLOCKS: A-T23, A-T45, A-T48
DELIVERABLE: docs/HOOK.md
SPEC: One page. (1) The 30-second hook, scripted, with the exact on-screen strings. (2) The persona in her own
      words — no adjectives about her being "busy". (3) The one-sentence insider insight. (4) The single
      takeaway. (5) A "cut list": five features we deliberately are NOT building and why.
      Language test: could a judge who has never heard of GPSR repeat the takeaway after one reading?
ACCEPTANCE: docs/HOOK.md ≤ 1 page; read aloud in ≤45 seconds; the insight sentence contains no hedge words.
```

```
ID: A-T08   TITLE: Cache 10 real listing fixtures
PHASE: 0    OWNER: data-agent     DEPENDS_ON: A-T05   BLOCKS: A-T15, A-T23
DELIVERABLE: data/fixtures/listings/*.json (10 files) + data/fixtures/listings/INDEX.md
SPEC: 10 real EU-marketplace listings for consumer products: 3 childcare/toys, 2 chargers/electrical,
      2 homeware, 1 cosmetic-adjacent, 1 textile, 1 with a KNOWN-GOOD complete compliance block (positive
      control). Save the full ListingSnapshot incl. images (downloaded locally, hashed).
      INDEX.md records for each: URL, retrieval date, category, and your manual note on which Art. 19 fields
      are present. Include at least 2 that are missing the EU responsible person.
      Respect robots.txt and marketplace ToS; cache once, do not hammer. If a marketplace blocks automated
      fetch, hand-save the rendered HTML from your own browser and mark fetch_mode="fixture".
ACCEPTANCE: 10 fixtures load as valid ListingSnapshot; ≥2 positive and ≥6 negative on responsible-person presence.
VERIFY: cd backend && uv run pytest tests/test_fixtures.py -q
```

### Phase 1 — Contracts (Sun night → Mon 09:00)

```
ID: A-T09   TITLE: Freeze core schemas
PHASE: 1    OWNER: backend-agent  DEPENDS_ON: A-T04, A-T05, A-T08  BLOCKS: all
DELIVERABLE: schemas/core-schemas.json ; backend/app/models.py (Pydantic v2 mirrors) ; backend/tests/test_schemas.py
SPEC: Transcribe SPEC §5 exactly into JSON Schema + Pydantic. Add a schema-version field. Write round-trip tests
      from every fixture. After this ticket, schemas are FROZEN — changes need their own ticket updating all consumers.
ACCEPTANCE: every fixture in data/fixtures validates; test asserts the frozen version string.
VERIFY: cd backend && uv run pytest tests/test_schemas.py -q
```

```
ID: A-T10   TITLE: Citation registry
PHASE: 1    OWNER: backend-agent  DEPENDS_ON: A-T04, A-T09  BLOCKS: A-T21
DELIVERABLE: backend/app/citations.py ; backend/tests/test_citations.py
SPEC: Registry per §5/§4-of-protocol. register(kind, locator, quote, retrieved_at, sha256, ttl, trust) → cit_id.
      get(cit_id) → Citation | None. expired(now) honours ttl_seconds per kind (regulation: 30d; official_dataset:
      7d; web_search: 24h; fetched_document: 7d; measurement: none; model_derived: NOT REGISTRABLE — a
      model-derived claim may never be a citation source of record). Persist to runs/citations.jsonl, loadable.
      A test must assert that registering trust="model_derived" raises.
ACCEPTANCE: registry survives a process restart; TTL expiry works; model_derived rejected.
VERIFY: cd backend && uv run pytest tests/test_citations.py -q
```

```
ID: A-T11   TITLE: Stage protocol + RunContext + pipeline runner with SSE
PHASE: 1    OWNER: backend-agent  DEPENDS_ON: A-T06, A-T09  BLOCKS: A-T16..A-T22
DELIVERABLE: backend/app/stages/base.py ; backend/app/pipeline.py ; backend/tests/test_pipeline.py
SPEC: StageResult/Stage protocol per agent-delegation-protocol §3. RunContext carries listing, destination
      countries, run_id, citation registry handle, ledger handle, an abort Event and a budget (max_usd).
      Pipeline runs stages in order, emits SSE events {stage, status, elapsed_ms, partial} so the UI can show
      real progress, honours the abort Event (STOP button), and short-circuits to UNDETERMINED if any stage
      abstains. Budget guard: if projected spend exceeds max_usd, stop and abstain with reason "budget_exceeded".
ACCEPTANCE: a fake 3-stage pipeline emits ordered SSE events; abort mid-run yields a partial Verdict with
            abstain=true; budget guard triggers.
VERIFY: cd backend && uv run pytest tests/test_pipeline.py -q
```

```
ID: A-T12   TITLE: Backend skeleton — FastAPI app, config, health, CORS
PHASE: 1    OWNER: backend-agent  DEPENDS_ON: A-T11  BLOCKS: A-T22
DELIVERABLE: backend/app/main.py ; backend/app/config.py
SPEC: pydantic-settings config from .env. Endpoints: GET /healthz (returns model IDs pinned + credits flag),
      POST /api/check (stub → 501 for now), GET /api/runs/{run_id}/events (SSE), GET /api/ledger/summary.
      CORS allows the deployed frontend origin AND localhost. No auth, no user accounts.
ACCEPTANCE: /healthz returns the pinned model IDs; uvicorn boots; OpenAPI docs render.
VERIFY: cd backend && uv run uvicorn app.main:app --port 8000 & sleep 3 && curl -s localhost:8000/healthz
```

```
ID: A-T13   TITLE: Frontend skeleton — routing, layout, theme switch, dev proxy
PHASE: 1    OWNER: frontend-agent DEPENDS_ON: A-T03, A-T12  BLOCKS: A-T23
DELIVERABLE: frontend/src/{App.tsx,routes/,lib/api.ts} ; frontend/vite.config.ts
SPEC: Routes: / (landing = the checker, nothing else), /report/:runId, /batch, /dev/tokens. Vite proxy
      /api → http://localhost:8000 so the browser NEVER calls localhost directly in production.
      Theme switch persisted to localStorage. No analytics, no third-party scripts, no external fonts.
ACCEPTANCE: npm run dev proxies to the backend; all four routes render; no external network requests in the
            built bundle (verify with a network trace).
VERIFY: cd frontend && npm run build && grep -rEo "https?://[a-z0-9.-]+" dist/assets | sort -u
```

```
ID: A-T14   TITLE: Full Safety Gate corpus ingest → DuckDB + embedding index
PHASE: 1    OWNER: data-agent     DEPENDS_ON: A-T05, A-T06  BLOCKS: A-T19
DELIVERABLE: scripts/ingest_safety_gate.py ; data/corpus/safety_gate.duckdb ; data/corpus/alerts.embeddings.parquet
SPEC: Ingest ≥52 weekly reports (target: 2023–2026, so the corpus reflects the GPSR era; more if time allows).
      Normalise risk_types to a controlled vocabulary (map the source's values; keep the original string too).
      Embed product + danger text with the Token Factory embedding model; store vectors in Parquet with the
      alert number as key. DuckDB for filtered search (by category, risk type, country, date) then cosine
      re-rank in Python — do NOT stand up a vector database server.
      Log ingestion stats to docs/DATA-SOURCES.md: rows, date range, % with images, vocabulary size, embedding cost.
ACCEPTANCE: ≥3,000 alerts ingested; embeddings exist for ≥95%; a category+keyword query returns top-10 in <300 ms.
VERIFY: python scripts/query_corpus.py --category Toys --q "magnetic building blocks" --k 5
COST NOTE: embedding a few thousand short texts is cents. Log the actual number.
```

```
ID: A-T15   TITLE: Golden-fixture test harness + eval set scaffolding
PHASE: 1    OWNER: eval-agent     DEPENDS_ON: A-T08, A-T09  BLOCKS: A-T37
DELIVERABLE: backend/tests/golden/ ; backend/tests/conftest.py ; eval/labels.v0.csv
SPEC: For each of the 10 fixtures, a golden expected ListingFields and expected Verdict, hand-labelled.
      conftest provides offline mode: model calls replayed from recorded responses (VCR-style) so tests never
      burn credits and never flake. eval/labels.v0.csv = 120 rows × columns (fixture_or_url, expected_verdict,
      expected_missing_fields, labelled_by, labelled_at).
ACCEPTANCE: `pytest -q --offline` runs the full suite with zero network and zero cost; golden tests fail if the
            extractor is stubbed out.
VERIFY: cd backend && uv run pytest -q --offline
```

### Phase 2 — Spine (Mon 27 Oct)

```
ID: A-T16   TITLE: S1 fetch_listing
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T11, A-T08  BLOCKS: A-T22
DELIVERABLE: backend/app/stages/s1_fetch_listing.py ; tests/test_s1.py
SPEC: Input URL or fixture id. Playwright headless Chromium for JS-rendered marketplaces, httpx fallback.
      Extract title/brand/description/bullets/price/spec table/images/seller block/compliance block/category
      breadcrumb. Download images, sha256 them, store under runs/blobs/. Handle: paywalls, cookie banners
      (accept-minimal), geo-blocks, 404, timeout(20s). On any failure → StageResult(ok=False, abstain=True,
      abstain_reason="fetch_failed:<code>"). NEVER fabricate listing content.
      Always offer the 10 fixtures as one-click samples so the demo never depends on live fetch.
ACCEPTANCE: 8 of 10 fixture URLs re-fetch and produce a valid ListingSnapshot OR fall back to the cached
            fixture with fetch_mode="fixture"; a 404 yields abstain, not an exception.
VERIFY: cd backend && uv run pytest tests/test_s1.py -q
```

```
ID: A-T17   TITLE: S2 extract_fields (Nemotron Nano + JSON schema)
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T11, A-T15  BLOCKS: A-T21, A-T22
DELIVERABLE: backend/app/stages/s2_extract_fields.py ; backend/app/prompts/extract_fields.md ; tests/test_s2.py
SPEC: Single Nemotron Nano call, response_format=json_schema against ListingFields. Prompt includes ONLY the
      field definitions and the listing text — not the whole regulation (that's S3's job, and keeping the prompt
      small is what makes Nano viable). Every field must return an evidence_span with a verbatim quote from the
      input; a field whose quote cannot be located in the input by exact substring match is forced to
      status=UNPARSEABLE and confidence=0. That substring check is code, in this module, not the model's word.
      Vision sub-call for hero + packaging images: detect CE mark presence, warning pictograms, printed
      responsible-person block. Register every quote as a citation (kind=fetched_document / measurement).
ACCEPTANCE: on the 10 golden fixtures, field-level accuracy ≥0.85 offline-replayed; every PRESENT field has an
            evidence_span.quote that substring-matches the source; hallucinated-quote test passes (inject a fake
            quote in a mocked response → module downgrades it to UNPARSEABLE).
VERIFY: cd backend && uv run pytest tests/test_s2.py -q
```

```
ID: A-T18   TITLE: S3 applicability (Nemotron Ultra, conditionally invoked)
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T17, A-T04  BLOCKS: A-T21
DELIVERABLE: backend/app/stages/s3_applicability.py ; backend/app/prompts/applicability.md ; tests/test_s3.py
SPEC: Invoke Ultra ONLY when: S2 min-confidence < 0.75, OR the category is regulated (toys, childcare,
      electrical, battery/magnet-containing, cosmetic-adjacent, food-contact), OR destination countries include
      a member state with a known high penalty ceiling. Otherwise emit a rule-table-only ObligationSet from
      Nano and LOG THE SAVING in the ledger note. This conditional escalation is the cost-control story —
      instrument it so you can report "Ultra invoked on 31 of 214 runs".
      Ultra receives: the rules table (relevant subset only), the extracted fields, the category breadcrumb.
      Returns ObligationSet. applicability_confidence is REQUIRED; if the model omits it or returns <0.60, abstain.
ACCEPTANCE: escalation logic unit-tested on both branches; ledger notes record skip-vs-invoke; on 5 golden
            fixtures the obligation sets match hand labels.
VERIFY: cd backend && uv run pytest tests/test_s3.py -q
```

```
ID: A-T19   TITLE: S4 recall_twin (embeddings → DuckDB → Nemotron Super)
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T14, A-T17  BLOCKS: A-T21, A-T23
DELIVERABLE: backend/app/stages/s4_recall_twin.py ; backend/app/prompts/recall_twin.md ; tests/test_s4.py
SPEC: Embed the listing's product description + detected category. DuckDB filtered search (same category or
      adjacent, publication_date ≥ 2019) → top 20 → cosine re-rank → top 5. Nemotron Super receives the listing
      summary + the 5 alerts' verbatim danger text and answers shared_failure_mode with
      verdict ∈ SHARES|POSSIBLY_SHARES|DOES_NOT_SHARE|UNDETERMINED, reasoning, and cited_alert_numbers.
      GATE PRECONDITION enforced here: cited_alert_numbers must be a subset of the 5 provided. If not, reject the
      response and retry once, then abstain. Register each used alert as a citation (kind=official_dataset,
      locator=alert number, quote=danger verbatim, retrieved_at=ingest date, ttl=7d).
      UI payload must include the alert's image URL so the recall photo can sit beside the product photo.
ACCEPTANCE: on 3 fixtures with known recalled analogues, SHARES or POSSIBLY_SHARES is returned with a valid
            citation; a mocked response citing a non-existent alert is rejected and leads to abstain.
VERIFY: cd backend && uv run pytest tests/test_s4.py -q
```

```
ID: A-T20   TITLE: S5 live_currency (Tavily — the $3,000 bonus)
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T18  BLOCKS: A-T21
DELIVERABLE: backend/app/tools/tavily.py ; backend/app/stages/s5_live_currency.py ; tests/test_s5.py
SPEC: Three load-bearing runtime queries per run:
      (1) is the harmonised standard cited in ObligationSet still current / has it been superseded?
      (2) what are the current national penalty provisions in each destination country?
      (3) is there Commission or national-authority guidance published in the last 90 days for this product class?
      Use Tavily search + extract. Register each used result as kind=web_search with ttl=24h. Results that are
      stale or off-topic are RECORDED AS REJECTED with a reason (the Telltale review praised showing
      "5 proposed, 5 backed, 0 rejected" — show your rejections too).
      If Tavily is unreachable: the run continues but every claim that depended on it downgrades to
      "verify this" and the Verdict cannot be COMPLIANT (it becomes AT_RISK with reason "live_check_unavailable").
      Log every call: query, results_returned, results_used, results_rejected, latency, cost.
ACCEPTANCE: a run performs ≥3 logged Tavily calls; /api/runs/{id} exposes them; with Tavily disabled via env the
            verdict downgrades as specified rather than failing.
VERIFY: cd backend && uv run pytest tests/test_s5.py -q && jq 'select(.kind=="tavily.search")' runs/ledger.jsonl | head
```

```
ID: A-T21   TITLE: S6 the deterministic gate
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T10, A-T17, A-T18, A-T19, A-T20  BLOCKS: A-T22, A-T28
DELIVERABLE: backend/app/gate/{gate.py,rules_loader.py,validators.py} ; tests/test_gate.py
SPEC: Implement SPEC §7 exactly. NO LLM calls in this module — enforce with a test that monkeypatches the TF
      client to raise and asserts the gate still runs. Validators: eu27_or_eea_country (ISO-3166 list embedded,
      no network), ean13_checksum, gtin_checksum, non_placeholder_text (regex for TODO/lorem/XXXX/example.com),
      language_covers_destinations (ISO-639-1 → member-state official language map, embedded),
      citation_resolves, citation_not_expired, confidence_threshold.
      Populate gate.rejected_claims with the reason for every dropped claim. Implement all four verdicts and
      both abstention paths. Deterministic: same input → byte-identical output (test it).
ACCEPTANCE: 100% of golden fixtures produce the hand-labelled verdict; determinism test passes; a fixture with
            an uncited claim populates rejected_claims; the gate module imports no LLM client.
VERIFY: cd backend && uv run pytest tests/test_gate.py -q
```

```
ID: A-T22   TITLE: POST /api/check wiring the full pipeline
PHASE: 2  OWNER: backend-agent  DEPENDS_ON: A-T16..A-T21  BLOCKS: A-T23, G2 gate
DELIVERABLE: backend/app/main.py (endpoint) ; tests/test_api_check.py
SPEC: Accepts {url?, fixture_id?, destination_countries[], marketplace?}. Creates a run, returns run_id
      immediately, streams stages over SSE, and writes the final Verdict to runs/verdicts/{run_id}.json.
      Concurrent-safe: N simultaneous runs must not interfere (slash-agent lost points on a single-user lockout).
      Global budget guard: refuse new runs when remaining credits < $2 with a clear 503 message.
ACCEPTANCE: 3 concurrent curl runs each complete with distinct run_ids and no cross-contamination;
            the fixture path completes in <25 s.
VERIFY: for i in 1 2 3; do curl -s -XPOST localhost:8000/api/check -d '{"fixture_id":"fx_toy_01"}' & done; wait
```

```
ID: A-T23   TITLE: Frontend — the checker page (verdict above the fold)
PHASE: 2  OWNER: frontend-agent DEPENDS_ON: A-T03, A-T13, A-T22  BLOCKS: G2 gate
DELIVERABLE: frontend/src/routes/CheckRoute.tsx + components
SPEC: Above the fold, in order, nothing else: (1) the input — URL field with a bright submit button that
      activates on paste, plus 10 one-click sample chips; (2) VerdictBanner with the verdict, the headline, and
      the severity colour; (3) the primary action with CopyButton per marketplace; (4) the recalled-twin card
      with the two photos side by side. BELOW the fold, collapsed by default: EvidenceDrawer with findings as
      rows, each a SeverityChip + statement + CitationPills that expand INLINE (never navigate away).
      ProgressRail shows the real stage from SSE with elapsed ms, plus a StopButton that actually aborts.
      No unexplained control anywhere — every dropdown gets a tooltip (Telltale lost a point on this).
      Timing target: paste → verdict visible ≤ 12 s for a fixture.
ACCEPTANCE: a teammate who has never seen it reaches the verdict and copies the fix without being spoken to,
            in ≤60 s (time it, record it); StopButton aborts a live run; layout survives 360 px width.
VERIFY: cd frontend && npm run build && manual timed test logged in reports/A-T23.TASK_REPORT.md
```

```
ID: A-T24   TITLE: Frontend — citation pills, evidence drawer, cost panel
PHASE: 2  OWNER: frontend-agent DEPENDS_ON: A-T23  BLOCKS: A-T38
SPEC: CitationPill shows kind icon + locator; expanding shows the verbatim quote, retrieved_at, trust level, and
      an external link that opens in a new tab with rel=noopener. A small "Run cost" panel (collapsible, bottom
      of the drawer) shows this run's tokens by model, cost, cache savings and p95 latency — the ops-persona
      touch Jackie praised in k9s terms. Show gate.rejected_claims as a distinct "Dropped (uncited)" section —
      this is a trust feature, not an error log.
ACCEPTANCE: rejected claims visible and visually distinct; cost panel numbers match the ledger line for the run.
VERIFY: compare UI panel against jq on runs/ledger.jsonl for the same run_id
```

```
ID: A-T25   TITLE: Demo hardening — concurrency, fixtures-first, no lockouts
PHASE: 2  OWNER: devops-agent   DEPENDS_ON: A-T22  BLOCKS: G4 gate
SPEC: The public demo must survive 6 judges clicking at once. Run queue with per-run isolation; fixtures served
      from cache with zero network; live fetch behind a 20 s timeout that falls back to the nearest fixture with
      a visible "live fetch timed out — showing cached sample" notice (honest, not silent). Rate limit by IP.
      No login, no invite code.
ACCEPTANCE: 6 parallel fixture runs all succeed; a live-fetch timeout degrades visibly and honestly.
VERIFY: locust or a bash loop of 6 concurrent requests; results in the ticket report
```

### Phase 3 — Proof (Tue 28 Oct)

```
ID: A-T26   TITLE: S7 artifact generation inside a Token Factory Sandbox
PHASE: 3  OWNER: sandbox-agent  DEPENDS_ON: A-T21, A-T22  BLOCKS: A-T27
DELIVERABLE: backend/app/sandbox/{client.py,images.py,artifacts.py} ; backend/app/stages/s7_artifact.py ;
             sandbox/image/{Dockerfile,validate.py,templates/}
SPEC: Build one reusable Sandbox image containing: the frozen rules table, validate.py, the HTML/PDF templates,
      and WeasyPrint. Resolve its immutable image UUID and commit it to docs/MODEL-USAGE.md.
      Per run: inject the Verdict JSON, generate the compliance pack =
        (a) per-marketplace information blocks (Amazon Product Compliance / bol.com Productveiligheid /
            eBay item specifics / Allegro / Kaufland field layouts),
        (b) multilingual warning text for each destination country,
        (c) a printable A4 label sheet with product identifier + manufacturer + responsible person + QR to the
            traceability record,
        (d) a one-page "what to do, in order" checklist with the real application routes.
      Retain the artifact in the image, download the bytes, sha256 locally and compare with the Sandbox-reported
      hash. Store under runs/artifacts/.
ACCEPTANCE: artifact generated for all 10 fixtures; local hash == sandbox hash; image UUID pinned and reused
            across runs (prove "prepare once, reuse safely").
VERIFY: cd backend && uv run pytest tests/test_s7.py -q && ls -la runs/artifacts | head
```

```
ID: A-T27   TITLE: Sandbox validator with the guest network DISABLED  ← the showpiece
PHASE: 3  OWNER: sandbox-agent  DEPENDS_ON: A-T26  BLOCKS: A-T28, A-T45
DELIVERABLE: sandbox/image/validate.py ; backend/app/sandbox/network_off.py ; tests/test_sandbox_network_off.py
SPEC: Re-run validate.py inside the Sandbox with the guest network disabled (per
      sandboxes/guides/configure-networking-and-secrets). The validator re-checks, with NO network access:
      responsible-person country ∈ EU-27/EEA; every EAN/GTIN checksum; every warning's language code covers a
      destination country; no placeholder text; every marketplace block has all required keys; every citation
      locator is well-formed; the PDF renders and contains the QR. Emit a signed validation report JSON.
      The point: **the artifact is provably self-consistent without any ability to phone home.**
      Show `network: disabled` in the UI and in the video.
ACCEPTANCE: validator runs with networking off and returns a report; a deliberately corrupted artifact (test
            injects a bad checksum) FAILS validation and the run's verdict cannot be COMPLIANT; the UI displays
            "validated offline · sha256 …".
VERIFY: cd backend && uv run pytest tests/test_sandbox_network_off.py -q
```

```
ID: A-T28   TITLE: Sandbox branching A/B — gate ON vs gate OFF  ← the experiment
PHASE: 3  OWNER: sandbox-agent  DEPENDS_ON: A-T21, A-T26  BLOCKS: A-T45, A-T48
DELIVERABLE: scripts/ab_gate.py ; runs/reports/ab-gate.json ; docs/img/ab-gate-chart.svg ; tests/test_ab.py
SPEC: Save ONE immutable Sandbox image containing the frozen rules table and the 120-case eval set. Branch it
      twice (sandboxes/guides/branch-compare-and-recover, cookbook try-two-coding-fixes):
        branch A: gate enabled      branch B: gate bypassed (model output becomes the verdict directly)
      Run the identical 120 cases down both branches. Compute: false-accept rate (verdict COMPLIANT or AT_RISK
      when the hand label says fields are missing), false-reject rate, UNDETERMINED rate, mean cost, mean latency.
      Publish the delta as a bar chart. Recover from the known-good branch afterwards.
      THIS IS YOUR TECHNOLOGICAL IMPLEMENTATION HEADLINE. Put the chart in the README's first screen and in the video.
ACCEPTANCE: ab-gate.json contains both arms with n=120 each; the chart renders; the README states the delta in
            one sentence with real numbers.
VERIFY: python scripts/ab_gate.py --report && jq '.arms | map({arm, n, false_accept_rate})' runs/reports/ab-gate.json
```

```
ID: A-T29   TITLE: Marketplace adapters
PHASE: 3  OWNER: backend-agent  DEPENDS_ON: A-T26  BLOCKS: A-T31
DELIVERABLE: backend/app/adapters/{amazon.py,bol.py,ebay.py,allegro.py,kaufland.py,shopify.py} ; tests/test_adapters.py
SPEC: One adapter per marketplace: given a Verdict, emit the exact field names and layout that platform's
      compliance UI expects, plus a plain-text block ready to paste. Derive field names from each platform's own
      public seller help pages — fetch and cite them (kind=web_search, ttl=7d). Where a platform's field name
      cannot be confirmed, output a generic labelled block and mark it TODO_VERIFY. Do NOT invent Amazon field names.
ACCEPTANCE: 6 adapters with ≥1 confirmed citation each; copy-to-clipboard text is UTF-8 clean and paste-safe.
VERIFY: cd backend && uv run pytest tests/test_adapters.py -q
```

```
ID: A-T30   TITLE: Multilingual warning generation + language validation
PHASE: 3  OWNER: backend-agent  DEPENDS_ON: A-T21  BLOCKS: A-T26
SPEC: For each destination country, generate the required warnings in that member state's consumer language
      using Nemotron Super, then VALIDATE with a deterministic language-id check (a language-detection library
      or a stopword/orthography test) that the output is actually in that language. A mismatch → the warning is
      rejected and the finding becomes MAJOR "warning language could not be verified". Never ship an
      unverified translation as if it were legal text; label generated translations
      "machine-generated — have a native speaker confirm before use". That label is an honesty signal judges reward.
ACCEPTANCE: NL/DE/FR/ES/IT/PL covered; a mocked wrong-language output is rejected; every generated string
            carries the machine-generated label in the artifact.
VERIFY: cd backend && uv run pytest tests/test_warnings.py -q
```

```
ID: A-T31   TITLE: Batch study as a Nebius Serverless Job  ← Potential Impact evidence
PHASE: 3  OWNER: devops-agent   DEPENDS_ON: A-T22, A-T29  BLOCKS: A-T32
DELIVERABLE: jobs/Dockerfile ; jobs/batch_run.py ; docs/BATCH-STUDY.md
SPEC: Package the pipeline as a container; submit as a Nebius Serverless Job. Input: a seed list of 150–250 live
      EU marketplace listing URLs across 3 categories (childcare/toys, chargers/electrical, homeware) — the same
      categories the Commission's 2026 sweep targeted, so your numbers are comparable to theirs.
      Run S1→S6 (skip S7 artifact to save cost). Be polite: ≤1 req/2s per host, honour robots.txt, cache blobs.
      Emit runs/reports/batch-YYYYMMDD.json with per-field non-compliance rates, per-marketplace rates,
      per-country rates, verdict distribution, recall-twin hit rate, total tokens and cost, and wall time.
      Handle partial failure honestly: report n_completed and n_failed separately. NEVER pad.
ACCEPTANCE: job completes; n_completed ≥ 150; per-field rates computed; total cost logged and under budget.
VERIFY: nebius serverless job logs <id> | tail -50 ; jq '.summary' runs/reports/batch-*.json
FALLBACK: if the job platform is not usable in time, run the same script locally as a long process and say so
          honestly in docs/BATCH-STUDY.md. A real n=150 local run beats an unfinished Serverless Job.
```

```
ID: A-T32   TITLE: Batch report page + charts
PHASE: 3  OWNER: frontend-agent DEPENDS_ON: A-T31  BLOCKS: A-T45
SPEC: /batch renders: the headline stat ("of N live listings, X% were missing the EU responsible person"),
      a per-field bar chart, a per-marketplace table, the verdict distribution, and the Commission's 58% figure
      beside yours for comparison — with both cited. Include the methodology box: n, categories, dates,
      fetch mode, exclusions, and known biases. A methodology box is what turns a number into research.
ACCEPTANCE: numbers on the page match runs/reports/batch-*.json exactly; both citations present with dates.
VERIFY: diff the rendered values against jq output (scripted check)
```

```
ID: A-T33   TITLE: Ledger aggregates + the all-Ultra counterfactual
PHASE: 3  OWNER: backend-agent  DEPENDS_ON: A-T06, A-T31  BLOCKS: A-T45, A-T48
DELIVERABLE: scripts/ledger_report.py ; docs/MODEL-USAGE.md (complete)
SPEC: From runs/ledger.jsonl produce: total requests/tokens/cost; per-model and per-stage cost; cache-hit rate
      and $ saved; p50/p95 latency per model; failure counts by class; and **the counterfactual cost of routing
      every stage to Ultra** — computed from real Ultra prices and the actual token volumes. Publish the table.
      This is the exact comparison the judges asked slash-agent for and it did not have.
ACCEPTANCE: docs/MODEL-USAGE.md contains a table with real numbers, the counterfactual row, and a one-sentence
            interpretation; GET /api/ledger/summary returns the same JSON.
VERIFY: python scripts/ledger_report.py --markdown > docs/MODEL-USAGE.md && grep -c "US\$" docs/MODEL-USAGE.md
```

```
ID: A-T34   TITLE: Cached Tokens — measure, don't assume
PHASE: 3  OWNER: backend-agent  DEPENDS_ON: A-T06  BLOCKS: A-T33
SPEC: Restructure prompts so the static legal preamble + rules subset is a byte-identical prefix across calls,
      per docs.tokenfactory.nebius.com/cached-tokens. Measure cached_tokens from the API response over ≥50 calls.
      Report cache-hit rate and $ saved. If caching does not apply or does not engage, **say so plainly in
      LIMITATIONS.md** — a negative result reported honestly is worth more than a fabricated saving.
ACCEPTANCE: ≥50 calls measured; cached_tokens reported; savings_usd in the ledger report OR an honest negative
            finding documented.
VERIFY: jq -s 'map(select(.request.cached_tokens>0)) | length' runs/ledger.jsonl
```

```
ID: A-T35   TITLE: Abstention paths + the "thin evidence" demo
PHASE: 3  OWNER: eval-agent     DEPENDS_ON: A-T21  BLOCKS: A-T48
DELIVERABLE: data/fixtures/thin_evidence/*.json ; tests/test_abstention.py
SPEC: Build 6 fixtures that SHOULD produce UNDETERMINED: a benign product with no compliance issue and no
      recalled analogue; a listing in a language the extractor can't parse; a category outside the rules table;
      a listing where the responsible person is ambiguous; a Tavily outage; a budget exhaustion. Verify the gate
      abstains with a clear reason and a routing instruction.
      This answers, on camera, the question Suchismita actually asked Telltale: *"what happens when the evidence
      is thin… how does this app build trust?"*
ACCEPTANCE: 6/6 abstain correctly with distinct reason codes; the UI shows a calm, non-alarming UNDETERMINED
            state that says what to do next.
VERIFY: cd backend && uv run pytest tests/test_abstention.py -q
```

```
ID: A-T36   TITLE: Talk to 3 real people (HUMAN TASK — highest ROI per hour in the whole build)
PHASE: 3  OWNER: human          DEPENDS_ON: A-T23 (needs something to show)  BLOCKS: A-T45, A-T48
SPEC: Find 3 people in the target audience: an Etsy/bol.com seller, a small importer, a marketplace ops or
      compliance person, a chamber-of-commerce advisor, or a trade-body contact. Dutch/German sellers are ideal.
      Show them the running demo. Ask, in this order:
        1. What happens today when a listing gets suppressed? How do you find out? What does it cost you?
        2. Which of these fields do you actually struggle with?
        3. Would you pay for this? What would you pay? Who else has this problem?
        4. What is wrong with it?
      Record (with permission) one 20-second clip OR one quotable sentence + their first name and role.
      Write reports/A-T36.INTERVIEWS.md with the raw notes. Feed findings back into the UI copy within the hour.
ACCEPTANCE: 3 conversations documented; ≥1 usable quote with explicit permission; ≥1 change made to the product
            as a result, noted in docs/DECISIONS.md.
NOTE: Ricky, verbatim: *"even if you're not a subject matter expert in the field you're building for, you should
      be going out and talking to potential customers before you build any features."* This ticket is 25% of
      Potential Impact and costs nothing but an afternoon.
```

```
ID: A-T37   TITLE: Eval — measure the gate, not the vibes
PHASE: 3  OWNER: eval-agent     DEPENDS_ON: A-T15, A-T21, A-T28  BLOCKS: A-T44, A-T45
DELIVERABLE: eval/run_eval.py ; runs/reports/eval.json ; docs/EVAL.md
SPEC: Label 120 cases twice (two independent label passes — two teammates, or a teammate plus a careful agent
      pass, kept separate). Report Cohen's kappa. Then compute, per class: precision/recall/F1 for the gate's
      verdict vs the label, and per-field extraction accuracy. Report the confusion matrix. Flag any class with
      <5 examples as INSUFFICIENT and do NOT report an accuracy number for it.
ACCEPTANCE: kappa reported; confusion matrix committed; INSUFFICIENT classes flagged; docs/EVAL.md states plainly
            what the system is not good at.
VERIFY: python eval/run_eval.py --report && jq '.kappa, .per_class' runs/reports/eval.json
```

### Phase 4 — Polish (Wed 29 Oct) — FEATURE FREEZE AT THE START OF THIS PHASE

```
ID: A-T38  TITLE: Onboarding — samples, first-run explainer, tooltips
PHASE: 4  OWNER: frontend-agent DEPENDS_ON: A-T24  BLOCKS: G4
SPEC: Assay lost points for having no onboarding; Telltale gained them for sample prompts. Ship: 10 one-click
      sample chips with a thumbnail and a 4-word label; a dismissible first-run overlay that says in 2 sentences
      what this is and what to paste; a tooltip on EVERY control including the destination-country selector
      (Telltale's unexplained dropdown); an inline "what is an EU responsible person?" explainer that expands
      without navigating away.
ACCEPTANCE: a first-time user completes a check with zero instruction (timed, 3 people, median ≤60 s).
```

```
ID: A-T39  TITLE: Empty / loading / error / partial-failure states
PHASE: 4  OWNER: frontend-agent DEPENDS_ON: A-T38  BLOCKS: G4
SPEC: Every state designed, none left to a spinner: empty (before first run), loading (ProgressRail with the
      real stage name + elapsed + StopButton), stage-failed-but-run-continues (visible inline notice, e.g.
      "live regulatory check unavailable — verdict downgraded"), full error (with a retry and the reason),
      budget exhausted, rate limited, and the UNDETERMINED state. Never show a raw stack trace (Assay showed a
      `standard error` live to the judges).
ACCEPTANCE: 7 states each have a designed component and a screenshot in docs/img/states/.
```

```
ID: A-T40  TITLE: Accessibility pass (and make it visible)
PHASE: 4  OWNER: frontend-agent DEPENDS_ON: A-T39  BLOCKS: G4
SPEC: Full keyboard navigation with a visible focus ring; skip link; ARIA labels and roles on the verdict banner
      (role="status" aria-live="polite"); colour is never the only signal — every severity chip carries a text
      label and a distinct glyph; contrast ≥4.5:1 for body text (verify, don't assume); prefers-reduced-motion
      respected; form labels associated; the recall-photo comparison has alt text describing both images.
      Then: add an "Accessibility" line to the video script and a paragraph to README + Next Steps.
      Ricky, verbatim: accessibility *"gets glazed over"* unless you call it out.
ACCEPTANCE: axe-core (or manual audit) reports 0 critical/serious violations; keyboard-only run completes;
            a screen-reader pass reads the verdict correctly.
VERIFY: cd frontend && npx @axe-core/cli http://localhost:5173 --exit
```

```
ID: A-T41  TITLE: Responsive + cross-browser pass
PHASE: 4  OWNER: frontend-agent DEPENDS_ON: A-T40  BLOCKS: G4
SPEC: 360 px, 768 px, 1280 px, 1920 px. Chrome, Firefox, Safari. The photo-pair comparison must survive narrow
      widths (stack vertically). No horizontal scroll anywhere.
ACCEPTANCE: screenshots at 4 widths committed; no layout break; a phone-on-cellular check by a teammate passes.
```

```
ID: A-T42  TITLE: Deploy — backend on a Nebius Serverless Endpoint, frontend on a static host
PHASE: 4  OWNER: devops-agent   DEPENDS_ON: A-T25, A-T41  BLOCKS: G4, G5
SPEC: Containerise the backend; deploy as a **Nebius Serverless Endpoint** (named in the track text → free
      Technological Implementation points) and expose its public URL. Deploy the frontend to Cloudflare Pages /
      Vercel / Netlify free tier. Point VITE_API_BASE at the endpoint. CORS configured for the exact frontend
      origin. Health check pinned to the deployed URL.
ACCEPTANCE: the deployed demo works from a fresh incognito window AND from a phone on cellular, with no
            localhost reference anywhere in the built bundle.
VERIFY: grep -rn "localhost\|127.0.0.1" frontend/dist || echo "clean"; curl -s $DEMO/healthz
FALLBACK: if Serverless Endpoint deployment is not achievable by Wed 12:00, deploy the backend to any always-free
          host and document the deviation in docs/DISCREPANCIES.md. A working demo beats a prestigious one.
```

```
ID: A-T43  TITLE: Durability hardening — the demo must still work on 15 December
PHASE: 4  OWNER: devops-agent   DEPENDS_ON: A-T42  BLOCKS: G5
SPEC: The rules require the project to remain available to judges free and without restriction until judging
      ends (1–15 Dec 2026). Therefore: no login; no expiring signed URLs; fixture-first so the demo works even
      if marketplaces block you; keep ≥$10 of Token Factory credits unspent for judge-time runs; pin all
      dependency versions; write docs/JUDGE-RUNBOOK.md with the exact steps and the expected result of each;
      add an uptime check that pings the demo hourly and posts to a Discord webhook; verify the video is public
      (not unlisted); verify the repo stays public.
ACCEPTANCE: docs/JUDGE-RUNBOOK.md exists and a non-teammate follows it successfully; uptime check running;
            credits remaining ≥$10 confirmed in the ticket report.
```

```
ID: A-T44  TITLE: LIMITATIONS.md with real failure cases
PHASE: 4  OWNER: content-agent  DEPENDS_ON: A-T37, A-T35  BLOCKS: G5
CONTEXT: _shared/templates/LIMITATIONS.template.md ; _shared/judging-rubric.md §3
SPEC: Populate with real numbers from eval.json and ab-gate.json, plus ≥3 concrete failure cases with
      screenshots: a listing the gate got wrong, a recall-twin false positive, a language the extractor mishandled.
      Include: what is NOT covered (product categories outside the rules table, non-EU destinations, harmonised
      legislation beyond the ones implemented); the legal-status disclaimer (screening tool, not legal advice);
      the abstention behaviour and its rate; the batch study's known biases; the accessibility gaps and the plan.
      Ricky + Suchismita + Aditya all said, on the record, that publishing failure cases reads as **rigor**.
ACCEPTANCE: every claim in LIMITATIONS.md is backed by a number, a citation or a screenshot; a sceptical read
            finds no unbacked sentence.
```

```
ID: A-T45  TITLE: README.md — complete, with all required highlights
PHASE: 4  OWNER: content-agent  DEPENDS_ON: A-T33, A-T31, A-T28, A-T42  BLOCKS: G5
CONTEXT: _shared/templates/README.template.md ; the submission requirements list in SPEC §12
SPEC: Must contain, in this order: the one-sentence problem; the 30-second gif/screenshot of the verdict;
      the insider insight; **how NVIDIA Nemotron models are used (the tiering table with real costs)**;
      **where Token Factory accelerated the workflow (Sandboxes network-off + branching, cached tokens,
      batch, structured output — named explicitly)**; **other Nebius services used (Serverless Endpoint,
      Serverless Job)**; the A/B chart; the batch study headline with its citation; quickstart that a judge can
      run in ≤5 minutes; architecture diagram; the ledger contract; evaluation results incl. kappa;
      links to LIMITATIONS.md and docs/JUDGE-RUNBOOK.md; the legal disclaimer; data attribution
      (EU Safety Gate reuse licence + CC-BY attribution); licence.
ACCEPTANCE: a clean clone + README quickstart works; all six required highlight areas present with real numbers;
            no unbacked superlative survives the sceptical read.
VERIFY: git clone <url> /tmp/r && cd /tmp/r && make demo   # the README's own quickstart, automated
```

```
ID: A-T46  TITLE: docs/ — MODEL-USAGE, DECISIONS, DISCREPANCIES, DATA-SOURCES, LEGAL-SOURCES, DESIGN
PHASE: 4  OWNER: content-agent  DEPENDS_ON: A-T33  BLOCKS: G5
SPEC: DECISIONS.md = one line per significant decision + the alternative rejected + why. DISCREPANCIES.md =
      every place live docs or data disagreed with our assumptions (this is also raw material for the Devpost
      feedback prize). DESIGN.md = the metaphor and the forbidden list.
ACCEPTANCE: ≥15 decisions logged; ≥3 discrepancies logged.
```

```
ID: A-T47  TITLE: Privacy, ToS and safety review
PHASE: 4  OWNER: human + backend-agent  DEPENDS_ON: A-T31  BLOCKS: G5
SPEC: Confirm: no personal data of sellers is stored beyond what the listing publishes; blobs are deleted after
      N days; scraping respects robots.txt and rate limits and marketplace ToS — document the position honestly,
      including where you are uncertain; the product carries a prominent "not legal advice" disclaimer on every
      verdict and in the artifact; no output could be mistaken for an official EU communication (do not use the
      EU emblem or the Safety Gate logo in a way that implies endorsement — that is a trademark problem and the
      video rules forbid unlicensed third-party marks).
ACCEPTANCE: docs/PRIVACY-AND-TOS.md written; disclaimer visible in UI and artifact; no EU emblem/logo usage.
```

### Phase 5 — Package (Wed 29 Oct 16:00 → Thu 30 Oct 18:00)

```
ID: A-T48  TITLE: Video script + shot list (≤2:50)
PHASE: 5  OWNER: content-agent + human  DEPENDS_ON: G4  BLOCKS: A-T49
CONTEXT: _shared/templates/video-script.template.md ; docs/HOOK.md
SPEC: Structure and timings:
      0:00–0:18  the problem. On screen: "58% of 1,700 offers checked across 35 EU marketplaces showed
                 manufacturer + EU responsible person + product ID together. Commission sweep, 7 Sept 2026."
                 Then the persona quote from A-T36.
      0:18–0:50  THE WOW, unbroken screen capture, real-time: paste a live listing → verdict → recalled twin
                 with both photos → Copy for Amazon. No cuts during the verdict reveal.
      0:50–1:25  how it works: architecture diagram; name all four Nemotron tiers on screen; show the Sandbox
                 running with the network disabled; show the sha256 match.
      1:25–1:55  the proof: the A/B gate-on vs gate-off chart; the batch study n and headline; the ledger table
                 incl. the all-Ultra counterfactual cost; cached-token savings.
      1:55–2:20  the gate rejecting a claim, and an UNDETERMINED abstention on thin evidence — deliberately.
      2:20–2:40  LIMITATIONS: the real failure case, said out loud. Next steps incl. the accessibility plan and
                 the browser extension the Telltale judges asked for.
      2:40–2:50  the insider insight, verbatim: "Compliance is not a checklist problem, it's a recall-prior problem."
      RULES: no copyrighted music; no third-party trademarks you can't use; public YouTube; captions on;
             record at 1080p; keep the cursor slow and deliberate.
ACCEPTANCE: script ≤2:50 read aloud at natural pace; every shot has a numbered entry and an owner.
```

```
ID: A-T49  TITLE: Shoot and edit the video
PHASE: 5  OWNER: human          DEPENDS_ON: A-T48  BLOCKS: G5
SPEC: Shoot in one pass per shot; do not live-edit. Upload PUBLIC to YouTube. Verify duration ≤2:59 and that the
      link works in a logged-out browser.
ACCEPTANCE: public URL; ≤3:00; the wow shot is unbroken; captions present.
KILL CRITERION: if not shot by Wed 29 Oct 20:00, cut to the 90-second minimum: problem → wow → architecture →
                insight. A submitted rough video beats an unsubmitted perfect one.
```

```
ID: A-T50  TITLE: Devpost submission copy
PHASE: 5  OWNER: content-agent  DEPENDS_ON: A-T45  BLOCKS: G5
CONTEXT: _shared/templates/README.template.md §devpost
SPEC: Title; tagline (≤80 chars); "Inspiration" (the 58% stat + the persona, with the source dated);
      "What it does"; "How we built it" (the tiering table, Sandbox network-off, branching A/B, Serverless
      Job/Endpoint, cached tokens — with real numbers); "Challenges we ran into" (≥3, specific and technical);
      "Accomplishments that we're proud of" (the A/B delta, the batch n, the abstention rate);
      "What we learned" (the insider insight + one thing about the platform);
      "What's next for RedFlag"; the required explanation of Nebius/Nemotron usage; built-with tags.
      Every number must match the README exactly — judges cross-check.
ACCEPTANCE: all sections present; no number disagrees with the README; no unbacked superlative.
```

```
ID: A-T51  TITLE: Devpost feedback section (10 × $100 + swag — 20 minutes of work)
PHASE: 5  OWNER: human          DEPENDS_ON: docs/DISCREPANCIES.md  BLOCKS: G5
CONTEXT: _shared/templates/devpost-feedback.template.md
SPEC: Judged on completeness, viability and potential impact. Write specific, technical, constructive feedback:
      what the Sandboxes branching API let you do that nothing else could; where the docs were ambiguous (quote
      the page); what Cached Tokens actually saved you, with numbers; the model-catalog/pricing discoverability
      experience; rate-limit behaviour under batch load; what you'd want next (e.g. a branch-diff view, cheaper
      embedding tiers, a Sandbox image registry); Tavily result-quality observations with a concrete query.
      Include the numbers. Vague praise scores nothing.
ACCEPTANCE: ≥400 words, ≥6 specific points, ≥4 with numbers or quoted doc URLs, ≥1 concrete feature request.
```

```
ID: A-T52  TITLE: Final verification sweep
PHASE: 5  OWNER: human + eval-agent  DEPENDS_ON: everything  BLOCKS: G5
SPEC: (1) clean clone → README quickstart → works; (2) fresh incognito → demo → aha in ≤60 s; (3) phone on
      cellular → demo works; (4) video public and ≤3:00; (5) LICENSE at repo root, visible on the repo page;
      (6) every number in README == Devpost copy == video; (7) credits remaining ≥$10; (8) uptime check running;
      (9) LIMITATIONS.md present with real numbers; (10) feedback section written.
ACCEPTANCE: all 10 checked off in reports/A-T52.FINAL.md with evidence (screenshots, command output).
```

```
ID: A-T53  TITLE: SUBMIT
PHASE: 5  OWNER: human          DEPENDS_ON: A-T52  BLOCKS: —
SPEC: Submit on Devpost. Screenshot the confirmation. Email it to every teammate. Then stop touching the demo
      except to keep it alive until 15 Dec.
ACCEPTANCE: submission confirmed, not a draft. Target Thu 29 Oct 18:00 CEST — 25 h before the deadline.
```

---

## 11. Test & verification plan

| Layer | What | Where |
|---|---|---|
| Unit | each stage, each validator, the gate's determinism, citation TTL, ledger classification | `backend/tests/` |
| Contract | every fixture validates against the frozen schemas | `tests/test_schemas.py` |
| Golden | 10 fixtures → expected ListingFields + expected Verdict, replayed offline | `backend/tests/golden/` |
| Adversarial | hallucinated quote → downgraded; uncited claim → rejected; wrong-language warning → rejected; bad checksum → BLOCKING | `tests/test_gate.py`, `tests/test_s2.py` |
| Abstention | 6 fixtures that must produce UNDETERMINED | `tests/test_abstention.py` |
| Integration | 3 concurrent end-to-end runs | `tests/test_api_check.py` |
| Eval | 120 cases, double-labelled, kappa + confusion matrix | `eval/` |
| Experiment | Sandbox branch A/B, n=120 per arm | `scripts/ab_gate.py` |
| Load | 6 parallel demo users | `scripts/load_demo.py` |
| Durability | clean clone + incognito + mobile | `reports/A-T52.FINAL.md` |
| CI | ruff + pytest + tsc + build on every push | `.github/workflows/ci.yml` |

**Offline mode is mandatory.** `pytest -q --offline` must run the whole suite with zero network and zero credits,
replaying recorded model responses. Without it, agents will burn your $50 on test runs by Tuesday.

---

## 12. Devpost submission copy — required elements

Map each requirement to where it lives:

| Requirement | Where |
|---|---|
| What you created, why, how it works | Devpost description ← A-T50, sourced from README |
| Track | Best Apps and Agents |
| Working demo URL | Deployed frontend (A-T42) + docs/JUDGE-RUNBOOK.md (A-T43) |
| Demo video ≤3:00, public YouTube | A-T49 |
| Public repo with open-source licence visible at the top | A-T01 (`LICENSE` at root) |
| README with setup instructions + run guidance | A-T45 |
| Highlight Nemotron usage / where Token Factory accelerated you / other Nebius services | A-T45 §"How NVIDIA Nemotron models are used" + §"Where Token Factory accelerated the workflow" + `docs/MODEL-USAGE.md` |
| Feedback on Nebius/NVIDIA tools | A-T51 |
| Pre-existing project explanation | N/A — new build (state this explicitly) |
| City selection | Only if you attended a Builders & Brews event (Amsterdam was 25 Sep) |

---

## 13. Design system (summary — full brief in A-T03)

**Metaphor:** EU safety signage meets customs paperwork. Bureaucratic, hard-edged, high-contrast. The object
being judged is a *listing*, so render it as a mock marketplace card — the judge recognises the artefact instantly.

| Token | Value | Use |
|---|---|---|
| `--hazard` | `#FFB300` | AT_RISK, warnings, primary CTA background |
| `--blocked` | `#D32F2F` | WOULD_BE_SUPPRESSED, BLOCKING findings |
| `--compliant` | `#1B7F4B` | COMPLIANT |
| `--undetermined` | `#6B7280` | UNDETERMINED, abstention |
| `--slate` | `#12161C` | Dark theme background |
| `--paper` | `#F7F5F0` | Light theme background / document surfaces |
| Display face | heavy grotesque | VerdictBanner headlines only |
| Mono face | `ui-monospace` stack | citation locators, field values, hashes, costs |

**Rules:** colour is never the only signal (a11y); every control has a tooltip; evidence expands inline and never
navigates away; the verdict banner uses `aria-live="polite"`; no external fonts, no third-party scripts, no
analytics — the demo must not depend on anyone else's network in December.

---

## 14. Risk register & pivots

| # | Risk | Likelihood | Detection | Mitigation | Pivot if it fires |
|---|---|---|---|---|---|
| R1 | Safety Gate endpoints unreachable/unparseable | Medium | **A-T05, Sun 20:00** | Try 3 endpoints; fall back to the data.europa.eu registration; fall back to a hand-curated 200-alert CSV from the public portal | **P1:** drop recall-twin, keep the deterministic Art. 19 gate + Tavily live checks. Still viable, lower ceiling. Or pivot to **Idea B** |
| R2 | Marketplaces block automated fetch | High | A-T08, A-T16 | 10 cached fixtures always available; live fetch is a bonus, never the demo path | Demo runs entirely on fixtures; say so honestly |
| R3 | EUR-Lex text extraction fails | Low | A-T04 | Save the HTML from a browser; parse manually; the rules table only needs ~12 verbatim quotes | Human types the 12 quotes from the official PDF |
| R4 | Batch job can't run on Serverless in time | Medium | A-T31, Tue 18:00 | Run the identical script as a local long process | Publish n=150 local; document the deviation honestly |
| R5 | Credits exhausted | Low | Ledger budget guard | Nano-first, Ultra only on escalation, cached tokens, offline test mode | Reduce batch to n=50 and say so |
| R6 | Nemotron tier unavailable in your catalog | Low | **A-T02, Sun** | Snapshot the real catalog first | Use the nearest available NVIDIA open model; document in DISCREPANCIES.md. The rule is "≥1 NVIDIA open-source model", not "specifically Ultra" |
| R7 | Legal accuracy challenged | Medium | A-T04c, A-T47 | Verbatim quotes only, human spot-check, prominent "not legal advice" disclaimer, abstain rather than guess | Narrow scope to one product category you can get right |
| R8 | Design ships looking generic | Medium | A-T03 review, A-T41 | Own tokens authored first; forbidden list enforced; a human eyeballs every screen | Cut a feature and spend the hours on UI. Design is 25% |
| R9 | Demo dies before 15 Dec | Medium | A-T43 | Fixture-first; credits reserved; uptime ping; judge runbook | Ship a downloadable build + a recorded walkthrough as backup |
| R10 | Scope creep | **High** | Every phase gate | Component-justification table in §4; feature freeze at Phase 4; anti-gold-plating prompt fragment | Cut to the hook. Nothing else |

---

## 15. Team allocation & parallelisation

Assuming 4 people (adjust by merging lanes):

| Person | Lanes | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|---|---|---|---|
| **P1 — lead/backend** | backend, gate | A-T01, A-T02, A-T06 | A-T09, A-T10, A-T11, A-T12 | A-T17, A-T18, A-T21, A-T22 | A-T29, A-T30, A-T33, A-T34 | A-T43 | A-T52, A-T53 |
| **P2 — data/infra** | data, jobs, sandbox | A-T04, A-T05 | A-T14 | A-T16, A-T19, A-T20 | A-T26, A-T27, A-T28, A-T31 | A-T42 | A-T49 (edit) |
| **P3 — frontend/design** | frontend | A-T03 | A-T13 | A-T23, A-T24 | A-T32 | A-T38, A-T39, A-T40, A-T41 | A-T49 (shoot) |
| **P4 — eval/content** *(or you)* | eval, content, legal | A-T07, A-T04c, A-T08 | A-T15 | A-T25 | A-T35, A-T36, A-T37 | A-T44, A-T45, A-T46, A-T47 | A-T48, A-T50, A-T51 |

**Critical path:** A-T05 → A-T14 → A-T19 → A-T21 → A-T22 → A-T23 → **G2** → A-T26 → A-T27/A-T28 → A-T45 → A-T48 → A-T49 → submit.
**The G2 thin slice (Monday night) is the insurance policy.** If it works, you cannot fail to submit something good.

**Agent dispatch limits:** at most 4 concurrent agent sessions, one per lane, never two in the same directory.
Integrate at phase gates only, by a human.

---

## 16. Definition of Done — project level

- [ ] All 53 tickets DONE or explicitly parked with a reason in `docs/DECISIONS.md`
- [ ] `make check` green from a clean clone
- [ ] Deployed demo reaches the aha in ≤60 s for a stranger, on desktop and mobile
- [ ] Ledger covers ≥95% of model calls; `docs/MODEL-USAGE.md` has real numbers including the all-Ultra counterfactual
- [ ] A/B gate experiment published with n=120 per arm
- [ ] Batch study published with n≥150 and a methodology box
- [ ] ≥3 real interviews, ≥1 quote with permission, ≥1 resulting product change
- [ ] `LIMITATIONS.md` with real failure cases, numbers and screenshots
- [ ] Sandbox artifact validated **with networking disabled** and hash-verified
- [ ] Abstention demonstrably works and is shown on camera
- [ ] Accessibility audited and called out in the video
- [ ] `LICENSE` at repo root; repo public; video public ≤3:00
- [ ] `docs/JUDGE-RUNBOOK.md` followed successfully by a non-teammate
- [ ] Devpost feedback section written with ≥4 numbers
- [ ] **Submitted by Thu 29 Oct 18:00 CEST**
