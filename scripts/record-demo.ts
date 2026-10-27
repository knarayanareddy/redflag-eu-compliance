#!/usr/bin/env node
/**
 * Record the static, client-side demo. The resulting capture is silent; use
 * video/script.md for narration. Prerequisites: npm ci, `npx playwright install chromium`,
 * and ffmpeg with libx264 available on PATH. Run from frontend/ with `npm run record:demo`.
 */
import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import { mkdir, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const frontend = join(root, 'frontend');
const outputDirectory = join(root, 'docs', 'media');
const outputFile = join(outputDirectory, 'redflag-demo.mp4');
const requireFromFrontend = createRequire(join(frontend, 'package.json'));
const { chromium } = requireFromFrontend('playwright');
const staticDemoUrl = 'http://127.0.0.1:4173/redflag-eu-compliance/';

function runBuild() {
  const result = spawnSync('npm', ['run', 'build'], {
    cwd: frontend,
    env: { ...process.env, VITE_STATIC_DEMO: 'true' },
    stdio: 'inherit',
  });
  if (result.status !== 0) throw new Error('Static Pages build failed; refusing to record a stale demo.');
}

function pause(milliseconds: number) {
  return new Promise((resolvePause) => setTimeout(resolvePause, milliseconds));
}

async function waitForPreview() {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    try {
      const response = await fetch(staticDemoUrl);
      if (response.ok) return;
    } catch {
      // Preview server is still starting.
    }
    await pause(250);
  }
  throw new Error(`Static preview did not become available at ${staticDemoUrl}`);
}

async function timedShot(page: any, durationMs: number, action: () => Promise<void>) {
  const started = Date.now();
  await action();
  const remaining = durationMs - (Date.now() - started);
  if (remaining > 0) await page.waitForTimeout(remaining);
}

async function main() {
  runBuild();
  await mkdir(outputDirectory, { recursive: true });
  const temporaryDirectory = await mkdtemp(join(tmpdir(), 'redflag-demo-'));
  const preview = spawn('npm', ['run', 'preview', '--', '--host', '127.0.0.1', '--port', '4173', '--strictPort'], {
    cwd: frontend,
    stdio: 'inherit',
    env: process.env,
    detached: process.platform !== 'win32',
  });
  let browser: any;
  try {
    await waitForPreview();
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 1,
      recordVideo: { dir: temporaryDirectory, size: { width: 1280, height: 720 } },
    });
    const page = await context.newPage();
    await page.goto(staticDemoUrl, { waitUntil: 'networkidle' });

    // Seven timed sections mirror the 2:45 shot list in video/script.md.
    await timedShot(page, 20_000, async () => {
      await page.getByRole('heading', { name: /Screen the evidence/i }).waitFor();
      await page.locator('.source-caveat').scrollIntoViewIfNeeded();
    });
    await timedShot(page, 25_000, async () => {
      await page.getByRole('button', { name: 'Screen Listing' }).click();
    });
    await timedShot(page, 25_000, async () => {
      await page.getByRole('heading', { name: /Safety Gate reference/i }).scrollIntoViewIfNeeded();
    });
    await timedShot(page, 25_000, async () => {
      await page.getByRole('heading', { name: /Evidence snapshot/i }).scrollIntoViewIfNeeded();
    });
    await timedShot(page, 23_000, async () => {
      await context.setOffline(true);
      await page.getByText('OFFLINE — LOCAL SIMULATION').waitFor();
      await page.getByRole('button', { name: 'Screen Listing' }).click();
    });
    await timedShot(page, 27_000, async () => {
      await page.getByRole('heading', { name: /What this demo cannot verify/i }).scrollIntoViewIfNeeded();
    });
    await timedShot(page, 20_000, async () => {
      await context.setOffline(false);
      await page.locator('.marketplace-intro').scrollIntoViewIfNeeded();
    });

    const video = page.video();
    await context.close();
    const webmPath = await video.path();
    await browser.close();
    browser = undefined;

    const conversion = spawnSync('ffmpeg', [
      '-y', '-i', webmPath, '-t', '165', '-an', '-c:v', 'libx264', '-preset', 'veryfast',
      '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', outputFile,
    ], { stdio: 'inherit' });
    if (conversion.status !== 0) {
      throw new Error('MP4 conversion failed. Install ffmpeg with libx264 and rerun npm run record:demo.');
    }
    console.log(`Recorded silent demo video: ${outputFile}`);
  } finally {
    if (browser) await browser.close();
    if (preview.pid) {
      try {
        process.kill(process.platform === 'win32' ? preview.pid : -preview.pid, 'SIGTERM');
      } catch {
        // The preview process may already have exited.
      }
    }
    await rm(temporaryDirectory, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
