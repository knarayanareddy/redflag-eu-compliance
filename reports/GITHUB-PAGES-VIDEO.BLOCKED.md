# GitHub Pages / video blockers: source verification and recording prerequisites

## Precise questions

1. Can a source owner provide the official Safety Gate record for `A12/00123/24` and verify the stated magnetic pinch/bowel-perforation risk wording?
2. Can an authorized reviewer confirm the Commission sweep statistic and GPSR applicability citation before those claims are narrated as facts?
3. Can a runner with Playwright Chromium and ffmpeg/libx264 installed generate and review the requested MP4 after the Pages build is merged and deployed?

## What I checked / tried

- Built the static Pages rendition with `make build-pages`; TypeScript and Vite completed successfully. Confirmed `frontend/dist/index.html` references `/redflag-eu-compliance/assets/...`, the local preview route returns HTTP 200, and the built static bundle has no `/v1/listings/screen` API route string.
- Added a GitHub Pages workflow triggered by pushes to `main`, plus the `make build-pages` target. This branch's workflow has not yet run on `main`; the public Pages URL is not verified live.
- Created a seven-shot script with durations 20+25+25+25+23+27+20 = 165 seconds. Added Playwright/TSX dependencies and `scripts/record-demo.ts`.
- Attempted `cd frontend && npm run record:demo`. The static build completed, but Playwright exited with `Executable doesn't exist at /home/user/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell`. The environment also has no `ffmpeg` executable. No `docs/media/redflag-demo.mp4` was produced.
- No external safety/regulatory source request was made. The repository has no official alert fixture for the requested alert number, and source claims remain unverified.

## Output observed / safe state

- The Pages build is ready to deploy after merge; the API-backed app is not used by the static build.
- Three demo product titles are labeled synthetic. The alert number and hazard wording from the prompt appear only as an unverified reference with an explicit no-match/no-official-record disclaimer.
- The demo's “hold” is an illustrative evidence-state UI, not an official suppression or compliance decision.
- The video script and recorder source exist; the MP4 artifact does not.

## Two options

1. **Complete the public demo/video with provenance:** provide the official alert record and source citations, install Playwright Chromium plus ffmpeg/libx264 on a runner, record and review the 165-second capture, then merge and confirm Pages deployment.
2. **Keep the current honest preview:** deploy the static demo without asserting an official alert match or legal result; retain the recording script and have the video task run later in an environment with the required binaries.

Do not present the unverified alert reference or 58% project-note claim as established fact to make the demo appear complete.
