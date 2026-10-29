# Devpost submission — final-ready copy

> The Pages demo is reported live. Legal, recall, and Commission-statistic claims below are deliberately separated from synthetic demo behavior; do not remove those qualifications in publication.

## Project name

**RedFlag — Product-safety evidence preview for EU marketplace sellers**

## Tagline

**See what the listing says. See what the evidence cannot yet prove.**

## Inspiration

Marketplace sellers need to organize product identity, manufacturer/responsible-person contacts, and safety information before listing. RedFlag explores a pre-flight workflow that keeps source evidence and recall leads visible instead of returning unsupported compliance decisions.

The project notes cite a Commission coordinated-sweep statistic of 58%. The primary release and denominator have not been independently confirmed in this repository, so the statistic is disclosed as pending verification—not as an established project result.

## What it does

- The backend prototype extracts structured fields from pasted listing text and abstains when legal source rules are unverified.
- Its S4 prototype can search a local Safety Gate corpus using deterministic keyword overlap; no official corpus is committed, so an empty corpus produces no recall comparison.
- The GitHub Pages rendition, reported live by the project owner, is a static client-side walkthrough with three synthetic, title-only sample products and simulated S2 term extraction. It makes no API or marketplace requests.
- Product 1 shows a side-by-side comparison with a **verified synthetic demonstration fixture** using the user-supplied reference string `A12/00123/24`. Fixture verification means its synthetic fields and display flow were checked; it is **not** authenticated or cited as an official EU Safety Gate record. The word overlap is not a vector match or evidence of a shared defect.
- A simulated fail-closed demo hold shows how missing contact evidence can stop the local walkthrough. It is not an actual statutory suppression, CE determination, or marketplace action.

## How we built it

The UI is React and Vite. GitHub Pages builds it with `VITE_STATIC_DEMO=true`, so the demo runs entirely client-side. The API is Python/FastAPI and uses deterministic extraction and a fail-closed rule gate. The Playwright script records the visual walkthrough; the script produces silent video, and voiceover/captions require human editing.

## Challenges and what we learned

A legal quotation, a checksum, a title-word overlap, or a prompt-supplied alert reference is not by itself evidence for a compliance or recall decision. The demo keeps that distinction visible: its fixture is verified only as a synthetic artifact, while legal text and official recall provenance remain unresolved.

## What's next

1. Have a qualified reviewer verify the exact GPSR wording, provision mapping, retrieval time, and source-document digest against EUR-Lex.
2. Obtain and attribute official Safety Gate records, then evaluate recall retrieval against labeled cases.
3. Verify the coordinated-sweep statistic against the primary Commission release and record its exact denominator and wording.
4. Generate and review the silent screen capture, then add human-recorded narration and captions before external submission.

## Demo and source

- **Demo URL (reported live by the project owner):** [knarayanareddy.github.io/redflag-eu-compliance](https://knarayanareddy.github.io/redflag-eu-compliance/)
- **Source repository:** [github.com/knarayanareddy/redflag-eu-compliance](https://github.com/knarayanareddy/redflag-eu-compliance)
- **Walkthrough script:** [`video/script.md`](../video/script.md)
- **Implementation limits:** [`README.md`](../README.md) and [`reports`](../reports)

## Limitations

RedFlag is a prototype, not legal advice, certification, or a product-sale determination. GPSR rules remain unverified; the official Safety Gate corpus is absent; the Pages products and recall fixture are synthetic; no vector matching or live EUR-Lex/Safety Gate synchronization is performed. The recording script produces no narration.
