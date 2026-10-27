# Devpost submission — draft (not yet published)

> This is a fact-bounded draft. Do not publish the 58% statistic or describe legal/recall outcomes as verified until the primary sources and datasets are reviewed. The public GitHub Pages URL is not confirmed live until the workflow completes and repository Pages settings are enabled.

## Project name

**RedFlag — Product-safety evidence preview for EU marketplace sellers**

## Tagline

**See what the listing says. See what the evidence cannot yet prove.**

## Inspiration

Marketplace sellers need to organize product identity, manufacturer/responsible-person contacts, and safety information before listing. RedFlag explores a pre-flight workflow that keeps source evidence and recall leads visible instead of returning an unsupported compliance decision.

A project note cites a Commission coordinated-sweep statistic of 58%, but the primary release and denominator have not been independently confirmed in this repository. This draft intentionally does not present it as a verified finding.

## What it does

- The backend prototype extracts structured fields from pasted listing text and abstains when legal source rules are unverified.
- Its S4 prototype can search a local Safety Gate corpus using deterministic keyword overlap; no official sample corpus is currently committed, so it reports that no recall comparison was made.
- A GitHub Pages build renders a static, client-side walkthrough with three synthetic, title-only sample products. It does not call the backend, fetch marketplace listings, or establish a legal or recall match.
- The screen separates a demo evidence hold from any actual statutory suppression decision.

## How we built it

The UI is React and Vite, with a static-mode build selected through `VITE_STATIC_DEMO=true`. The API is Python/FastAPI and uses deterministic extraction and a fail-closed rule gate. The Pages workflow publishes the static bundle; the Playwright script records a silent walkthrough, with voiceover and captions left to a human editor.

## Challenges and what we learned

The hard part is not drawing a warning card. A legal quotation, a provided checksum, a title-word overlap, or an unverified alert reference is not by itself evidence for a compliance or recall decision. The prototype keeps user-supplied legal quotations in an explicitly unverified state and does not fabricate alert records to make the demo look complete.

## What's next

1. Have a qualified reviewer verify the exact GPSR wording, provision mapping, retrieval time, and source-document digest against EUR-Lex.
2. Ingest and attribute a small real Safety Gate sample set with provenance, then evaluate retrieval against labeled cases.
3. Verify the coordinated-sweep statistic against the primary Commission release and record its exact denominator and wording.
4. Run the Pages deployment and review accessibility, source attribution, and the human-narrated video before publication.

## Demo and source

- Requested Pages URL: <https://knarayanareddy.github.io/redflag-eu-compliance/> — deployment status not yet verified.
- Source repository: <https://github.com/knarayanareddy/redflag-eu-compliance>
- Walkthrough script: [`video/script.md`](../video/script.md)
- Current implementation limits: [`README.md`](../README.md) and [`reports`](../reports)

## Limitations

RedFlag is a prototype, not legal advice, certification, or a product-sale determination. The legal quotes are not human-verified, the Safety Gate fixture corpus is absent, the static product examples are synthetic, and the video recorder produces no narration.
