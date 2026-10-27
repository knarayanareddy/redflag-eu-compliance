# Demo media output

`redflag-demo.mp4` is generated locally by `npm run record:demo` from `frontend/`. It is not committed from this run: Playwright's Chromium executable and `ffmpeg` with `libx264` are not installed in the current environment. Install Chromium with `npx playwright install chromium` and install ffmpeg, then rerun the command.

The generated capture is silent and trimmed to 165 seconds. Use `video/script.md` for a separately recorded narration. The task-supplied alert reference remains visibly labeled unverified in the static demo.
