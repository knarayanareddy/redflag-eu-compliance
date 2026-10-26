# EU Safety Gate (RAPEX) — ingestion specification

The recall-prior corpus. **Ticket A-T05 (spike) and A-T14 (full ingest).**

---

## 1. What it is

**Safety Gate** is the EU rapid alert system for dangerous non-food products, formerly RAPEX. National market
surveillance authorities notify the Commission; the Commission publishes alerts weekly (Fridays) plus immediate
publications for serious risks. Operated by DG JUST. Participants: EU-27 + EEA (NO, IS, LI).

Fields per alert (as observed in the portal's own data): alert reference/number, weekly report reference,
publication date, notifying country, product category, product name (generic and specific), brand, model/type,
batch number, barcode, **risk type(s)**, **risk level**, **danger** (the authority's own words describing why the
product is dangerous), **measures taken**, country of origin, description text, image URLs, and a URL to the
alert detail page or the recall notice.

Volume: **4,671 alerts in 2025** — a record, +13% YoY. Corpus goes back to **2005**. Target ingest window for
this project: **2019 → present** (≥3,000 alerts; ideally ≥15,000 if the endpoint is fast), because that reflects
the modern product mix and the GPSR era.

---

## 2. Candidate endpoints — try in this order, record which works

| # | Endpoint | Auth | Format | Notes |
|---|---|---|---|---|
| **a** | `https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en` | **none** | XML, one weekly report | Documented as public and logged-out by multiple third-party scrapers. **Try first.** |
| **b** | The JSON API the portal itself uses — discover it in browser DevTools → Network on `https://ec.europa.eu/safety-gate-alerts/screen/webReport` | none | JSON | Richer/structured. Reverse-engineer the request shape and record it in `docs/DATA-SOURCES.md`. Do not use login-gated or internal-only endpoints. |
| **c** | Alert detail endpoint pattern: `https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/{id}` | none | JSON/HTML | For per-alert enrichment |
| **d** | `https://data.europa.eu/data/datasets/rapex-rapid-alert-system-non-food` | none | registration record with weekly XML and XLSX download links | Fallback + licence/attribution metadata |
| **e** | `https://public.opendatasoft.com/explore/assets/healthref-europe-rapex-en/` | none | ODS dataset built from weekly reports since 2015 | Second fallback |

**Also useful (non-EU, for a comparative chart, optional):** US CPSC recall CSV export at
`https://www.cpsc.gov/Recalls` — downloadable CSV of recalls and product safety warnings. If you ingest it, you
can say *"we compared EU and US recall patterns for this product class"* — a strong original-research beat.
Only if time allows.

**Politeness / legality:**
- One request per weekly report, sequential, with a delay (≥1 s). Do not parallelise against a Commission endpoint.
- Public, logged-out endpoints only. No credentials, no CAPTCHA solving, no bypassing rate limits.
- Record the **reuse licence** in `docs/DATA-SOURCES.md`. European Commission data is generally reusable under
  **CC-BY-4.0** unless stated otherwise — **confirm this on the portal/data.europa.eu page and attribute
  correctly in the README, the artifact footer and the video.** Do not copy the alert *images* into your repo;
  hotlink or store only a URL plus a hash, and attribute.
- EU emblem / Safety Gate logo: **do not use** in a way implying endorsement. Video rules forbid unlicensed
  third-party marks.

---

## 3. Target schema (DuckDB table `alerts`)

| Column | Type | Nullable | Notes |
|---|---|---|---|
| `alert_number` | VARCHAR **PK** | no | e.g. `SR/02365/26`. Unique per run |
| `report_reference` | VARCHAR | yes | e.g. `Report-2026-39` |
| `publication_date` | DATE | no | |
| `notifying_country` | VARCHAR(2) | no | ISO-3166 alpha-2 of the EU/EEA state that raised it |
| `country_of_origin` | VARCHAR(2) | yes | Where the product was made |
| `category` | VARCHAR | no | Portal category, e.g. `Toys`, `Electrical appliances and equipment`, `Cosmetics`, `Childcare articles and children's equipment` |
| `category_norm` | VARCHAR | no | Your controlled vocabulary (see §4) |
| `product` | VARCHAR | no | Short description, e.g. "Toy figure" |
| `product_specific` | VARCHAR | yes | Full product name as given |
| `brand` | VARCHAR | yes | |
| `model` | VARCHAR | yes | |
| `batch_number` | VARCHAR | yes | |
| `barcode` | VARCHAR | yes | EAN/GTIN — enables exact matching against a listing's identifier |
| `risk_types` | VARCHAR[] | no | Controlled vocabulary, see §4 |
| `risk_types_raw` | VARCHAR[] | no | Original strings, preserved |
| `risk_level` | VARCHAR | yes | e.g. `Serious risk` |
| `danger` | TEXT | no | **Verbatim authority wording. This is the field you embed and reason over.** |
| `measures` | TEXT | yes | e.g. `Recall of the product from end users`; `Withdrawal from the market` |
| `description` | TEXT | yes | Commission alert text as published |
| `image_urls` | VARCHAR[] | yes | Links only — do not rehost |
| `alert_url` | VARCHAR | no | Detail page or recall notice |
| `sold_online` | BOOLEAN | yes | If the portal exposes it — very useful, since your persona sells online |
| `retrieved_at` | TIMESTAMPTZ | no | |
| `source_endpoint` | VARCHAR | no | Which of (a)–(e) |
| `embedding` | FLOAT[1536] *(or your model's dim)* | yes | In a sibling Parquet, not in DuckDB, for simplicity |

Sibling file: `data/corpus/alerts.embeddings.parquet` — columns `alert_number`, `text_embedded`, `model`, `vector`.
`text_embedded` = `category_norm + " | " + product + " | " + danger` (the danger text carries the failure mode).

---

## 4. Controlled vocabularies (normalise, but keep the raw)

**`category_norm`** — map portal categories onto the product classes your rule table understands:
`toy`, `childcare`, `electrical_appliance`, `charger_or_power_supply`, `battery_containing`, `magnet_containing`,
`cosmetic`, `food_contact_material`, `textile`, `lighting`, `hand_tool`, `furniture`, `jewellery`,
`personal_protective_equipment`, `pyrotechnic`, `other`.

**`risk_types`** — the portal uses values such as `Chemical`, `Choking`, `Cuts`, `Electric shock`, `Fire`,
`Injury`, `Strangulation`, `Suffocation`, `Burns`, `Hearing`, `Microbiological`, `Thermal`. Enumerate what you
actually find and freeze the list; do not guess. Record the observed value → normalised value mapping in
`data/corpus/vocabulary.md` with counts.

---

## 5. Retrieval algorithm (S4 `recall_twin`)

```
1. Build query text from the listing: category_norm + product title + first 400 chars of description
   + any detected attributes (magnets, button cell, small parts, charger, cosmetic ingredient class).
2. Hard filters in DuckDB (cheap, deterministic, explainable):
     publication_date >= 2019-01-01
     AND category_norm IN (listing.category_norm, *adjacent categories from a small hand-written map)
     AND (barcode = listing.identifier  →  EXACT MATCH, short-circuit to top of results)
3. Cosine re-rank over the filtered candidate embeddings → top 20.
4. Diversify: keep at most 3 per (notifying_country, risk_type) pair so you don't return 20 near-duplicates.
5. Take top 5 → hand to Nemotron Super with the verbatim `danger` text.
6. Super returns shared_failure_mode.verdict + reasoning + cited_alert_numbers.
   HARD PRECONDITION (enforced in code, not in the prompt): cited_alert_numbers ⊆ the 5 provided.
   Violation → retry once → then abstain.
7. Register each used alert as a citation: kind=official_dataset, locator=alert_number,
   quote=danger (verbatim), retrieved_at=ingest timestamp, ttl=7d, trust=official_secondary.
```

**Exact-barcode short-circuit matters.** If a listing's GTIN matches a Safety Gate barcode, that is not a
"twin" — that is *your product is under recall*. Surface it as a distinct, higher-severity finding:
`RF-RECALL-EXACT`. Almost every compliance tool stops at this check; you do it AND go further.

---

## 6. Ingestion stats to publish (this is your methodology box)

`docs/DATA-SOURCES.md` must record:

- endpoint used, and the exact request shape
- retrieval date and time (CEST)
- weekly reports ingested, date range covered
- alert count; % with `danger` populated; % with `barcode`; % with `image_urls`
- category distribution (top 15 with counts)
- risk_type distribution (all, with counts)
- notifying-country distribution (top 10)
- embedding model + dimension + total tokens + **total cost in USD**
- the reuse licence and the exact attribution string
- known gaps (e.g. older alerts English-only; images not rehosted; `sold_online` availability)

Publishing this is what converts "we used a public dataset" into original research — and it is directly
responsive to Selena's *"credible, specific case"* and Suchismita's *"what did you learn that someone outside
the problem wouldn't know."*

---

## 7. Acceptance test for A-T05 (the Sunday spike)

```bash
python scripts/fetch_safety_gate.py --reports 1 --out data/corpus/safety_gate_sample.parquet
python - <<'PY'
import pandas as pd
d = pd.read_parquet('data/corpus/safety_gate_sample.parquet')
assert len(d) >= 20, f"only {len(d)} alerts"
for col in ['alert_number','publication_date','notifying_country','category','product','risk_types','danger','alert_url']:
    assert col in d.columns, col
    assert d[col].notna().mean() >= 0.9 or col in ('barcode','brand','image_urls'), f"{col} sparse: {d[col].notna().mean()}"
print("OK", len(d), "alerts;", d['category'].value_counts().head(3).to_dict())
PY
```

If this fails by **Sun 26 Oct 20:00**, escalate and trigger pivot **P1** in `SPEC.md §14`.
