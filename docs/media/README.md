# Demo media

`redflag-demo.mp4` is the generated silent walkthrough. It is H.264 at 1280×720 with a duration of 2:45; its seven timed sections correspond to [`video/script.md`](../../video/script.md). The narration and captions are intentionally separate human-editing tasks.

To regenerate it from `frontend/`:

```bash
npm ci
npx playwright install chromium ffmpeg
npm run record:demo
```

The system ffmpeg used for MP4 conversion must include `libx264`; set `FFMPEG_PATH` if it is not on `PATH`. The recording displays a fixture verified for synthetic-demo use only, not an authenticated Safety Gate record.
