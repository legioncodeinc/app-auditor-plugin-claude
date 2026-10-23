// Record a scripted product demo: one video per scene, 3x key screenshots, a write
// ledger with read-only verification, a privacy scan, an editable timeline, captions,
// scene titles, narration timings and Eleven v4 clip texts, plus the ffmpeg assembly
// script. The demo plan is human-approved JSON (see demo-plan.example.json).
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... PLAN=demo-plan.json node demo/record-demo.mjs [--retake]
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { gotoChecked, loadConfig, log, openApp, pad, settle, shotOptions, slugify } from "../lib/common.mjs";
import { clipWindow, findingEntry, isGuardrailError, maskText, planDigest, planTake, sceneKey, scanText, segmentsTsv, buildTimeline, validateDemoPlan, writesForScene } from "../lib/demo-plan.mjs";
import { countWords } from "../lib/narration.mjs";
import { DemoSceneError, installCursorOverlay, runAction, runVerify, visibleText } from "../lib/demo-actions.mjs";
import { assertSafeDemoTarget, demoDenyPattern } from "../lib/demo-guard.mjs";
import { appendPrivate, mkdirPrivate, redactPatterns, writeDemoCues, writePrivate } from "../lib/demo-cues.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const cfg = loadConfig();
if (!process.env.PLAN) throw new Error("Set PLAN=/path/to/demo-plan.json (see demo/demo-plan.example.json)");
const plan = validateDemoPlan(JSON.parse(fs.readFileSync(process.env.PLAN, "utf8")));
if (!cfg.output.demo) throw new Error("output.demo is required in the capture config for demo recordings");
const r = (s) => redactPatterns(cfg, maskText(s));
// Real clip length from ffprobe (frames / frame rate; Playwright webm often has no duration header).
const probeClipMs = (file) => {
  const r = spawnSync("ffprobe", ["-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets,r_frame_rate", "-of", "csv=p=0", file], { encoding: "utf8" });
  if (r.status !== 0) return NaN;
  const [rate, packets] = r.stdout.trim().split(",");
  const [num, den] = String(rate).split("/").map(Number);
  return (Number(packets) / (num / (den || 1))) * 1000;
};

// Write ledger: every take that attempted a write is remembered, so a rerun cannot
// silently repeat it (an accidental second appointment, a second drop).
const slug = slugify(plan.title || "demo") || "demo";
const ROOT = cfg.output.demo;
mkdirPrivate(ROOT);
const ledgerPath = path.join(ROOT, `${slug}.ledger.json`);
const ledger = fs.existsSync(ledgerPath) ? JSON.parse(fs.readFileSync(ledgerPath, "utf8")) : { title: plan.title, takes: [] };
const retake = process.argv.includes("--retake") || process.env.RETAKE === "1";
const decision = planTake(ledger, plan, slug, { retake });
if (decision.refuse) throw new Error(decision.message);
log(decision.message);
const OUT = path.join(ROOT, decision.dir);
if (fs.existsSync(OUT)) throw new Error(`${OUT} already exists. Move it aside; takes never overwrite earlier output.`);
const takeRecord = { take: decision.take, dir: decision.dir, startedAt: new Date().toISOString(), planDigest: planDigest(plan), attemptedWrites: [] };
ledger.takes.push(takeRecord);
const saveLedger = () => writePrivate(ledgerPath, JSON.stringify(ledger, null, 2));
saveLedger();
for (const sub of ["scenes", "screenshots", "failures"]) mkdirPrivate(path.join(OUT, sub));

const VIDEO = { width: plan.video?.width || 1920, height: plan.video?.height || 1080 };
const WPM = plan.narration?.wordsPerMinute || 140; // 130 to 150 wpm band (research: demo section)
const END_HOLD_MS = plan.video?.endHoldMs ?? 1500;
const parkAt = plan.video?.parkAt || { x: VIDEO.width - 40, y: VIDEO.height - 40 };
const cursor = plan.video?.cursor === true;
// Built-in deny list always applies; plan.safety.denyPattern only adds to it.
const DENY = demoDenyPattern(plan.safety?.denyPattern);
const guard = (locator, action) => assertSafeDemoTarget(locator, action, DENY);
const patterns = cfg.redact?.patterns || [];

const rows = [], report = [], privacy = [];
let writeBlocked = null, abort = null;
const findingsPath = path.join(ROOT, "findings.md");
const addFinding = (scene, kind, detail, evidence) => {
  if (!fs.existsSync(findingsPath)) writePrivate(findingsPath, "# Demo findings\n\nAppended by record-demo.mjs. Text is masked and redacted.\n\n");
  appendPrivate(findingsPath, r(findingEntry({ when: new Date().toISOString(), title: plan.title || slug, take: decision.dir, scene, kind, detail, evidence })));
};

for (const [i, scene] of plan.scenes.entries()) {
  const key = sceneKey(scene, i);
  const id = `${pad(i + 1, 2)}-${slugify(key) || "scene"}`;
  const writes = writesForScene(plan, key);
  const row = { id: key, title: r(scene.title || key), route: scene.route, narration: r(scene.narration || ""), clip: null, durationMs: 0, status: "ok" };
  rows.push(row);
  const skip = (reason) => {
    row.status = "skipped"; row.reason = reason;
    for (const w of writes) report.push({ id: w.id, scene: key, description: r(w.description), effect: r(w.effect), status: "skipped", reason, checks: [] });
    log(`scene ${id}: skipped (${reason})`);
  };
  if (abort) { skip("run aborted by a guardrail"); continue; }
  if (writes.length && writeBlocked) { skip(`earlier write scene "${writeBlocked}" did not verify`); continue; }

  const tmp = path.join(OUT, "scenes", `.${id}`);
  const { browser, context, page } = await openApp(
    { ...cfg, browser: { ...cfg.browser, viewport: VIDEO, deviceScaleFactor: 1 } },
    {
      slowMo: plan.video?.slowMo ?? 250, // human-watchable pacing
      // Headless video has no cursor. With video.cursor the DOM overlay draws one; otherwise
      // Playwright's showActions outlines each interacted element.
      recordVideo: { dir: tmp, size: VIDEO, ...(cursor ? {} : { showActions: plan.video?.showActions ?? { duration: 500, position: "top-right" } }) },
    },
  );
  if (cursor) await context.addInitScript(installCursorOverlay);
  const t0 = Date.now();
  const ctx = { guard, deny: DENY, settle: (p) => settle(p, 0, 600), parkAt, pointer: parkAt };
  // Every navigation reloads the overlay at its hidden start, so put it back where the pointer is.
  const restore = () => page.mouse.move(ctx.pointer.x, ctx.pointer.y).catch(() => {});
  page.on("load", restore);
  const hits = [];
  const scan = async (action) => {
    for (const h of scanText(await visibleText(page), patterns)) {
      const prev = hits.find((x) => x.kind === h.kind && x.masked === h.masked);
      if (prev) prev.count = Math.max(prev.count, h.count); else hits.push({ ...h, action });
    }
  };
  const failureShot = async () => {
    const file = path.join(OUT, "failures", `${id}.png`);
    await page.screenshot(shotOptions(cfg, page, { path: file }));
    fs.chmodSync(file, 0o600);
    return path.relative(ROOT, file);
  };
  let checks = [], evidence = null, loadedAt = null, endAt = null;
  try {
    if (writes.length) {
      // Recorded before any action runs: a crash mid-scene still counts as an attempt.
      takeRecord.attemptedWrites.push(...writes.map((w) => w.id));
      saveLedger();
    }
    // The cut starts when navigation starts: before that the clip is a blank about:blank page.
    loadedAt = Date.now();
    await gotoChecked(cfg, page, scene.route, { idleMs: 0, extraMs: 800 });
    await restore();
    await scan(0);
    for (const [j, a] of (scene.actions || []).entries()) {
      try { await runAction(page, a, ctx); } catch (e) { e.message = `action ${j + 1} (${a.type}): ${e.message}`; throw e; }
      if (a.screenshot) {
        const file = path.join(OUT, "screenshots", `${id}-${slugify(a.screenshot)}.png`);
        await page.screenshot(shotOptions(cfg, page, { path: file }));
        fs.chmodSync(file, 0o600);
      }
      await scan(j + 1);
    }
    for (const v of scene.verify || []) checks.push(await runVerify(page, v));
    const failed = checks.filter((c) => !c.pass);
    row.status = failed.length ? "mismatch" : writes.length ? "verified" : "ok";
    if (failed.length) {
      evidence = await failureShot().catch(() => null);
      row.error = r(failed.map((c) => `${c.check}: got ${c.actual}`).join("; "));
    }
    // Hold long enough for the narration at the plan's pace, plus caption lead and tail.
    const hold = Math.ceil((countWords(scene.narration) / WPM) * 60000) + 600;
    const elapsed = Date.now() - t0;
    if (elapsed < hold) await page.waitForTimeout(hold - elapsed);
  } catch (e) {
    const guardrail = !(e instanceof DemoSceneError) && isGuardrailError(e);
    row.status = guardrail ? "aborted" : "failed";
    row.error = r(e.message);
    if (guardrail) abort = e;
    evidence = await failureShot().catch(() => null);
  } finally {
    endAt = Date.now();
    page.off("load", restore);
    await context.close(); // video is flushed to disk only when the context closes
    await browser.close();
  }
  const webm = fs.existsSync(tmp) ? fs.readdirSync(tmp).find((f) => f.endsWith(".webm")) : null;
  if (webm) {
    const clip = path.join(OUT, "scenes", `${id}.webm`);
    fs.renameSync(path.join(tmp, webm), clip);
    fs.chmodSync(clip, 0o600);
    row.clip = `scenes/${id}.webm`;
    const win = clipWindow({ clipMs: probeClipMs(clip), wallMs: endAt - t0, loadedToEndMs: loadedAt ? endAt - loadedAt : NaN });
    Object.assign(row, { inMs: win.inMs, outMs: win.outMs, durationMs: win.outMs - win.inMs });
    if (!win.probed) log(`scene ${id}: ffprobe unavailable, so the cut uses wall-clock timing; check segments.tsv`);
  }
  fs.rmSync(tmp, { recursive: true, force: true });
  row.checks = checks.map((c) => ({ ...c, actual: r(c.actual), expected: r(c.expected) }));
  privacy.push({ id: key, hits });

  const writeStatus = { verified: "verified", mismatch: "mismatch" }[row.status] || "failed";
  for (const w of writes) report.push({ id: w.id, scene: key, description: r(w.description), effect: r(w.effect), status: writeStatus, checks: row.checks, ...(row.error ? { error: row.error } : {}) });
  if (writes.length && writeStatus !== "verified") writeBlocked = key;
  if (["failed", "mismatch", "aborted"].includes(row.status)) addFinding(key, row.status, row.error || "unknown error", evidence);
  log(`scene ${id}: ${row.status}, ${(row.durationMs / 1000).toFixed(1)}s${hits.length ? `, ${hits.length} masked text hit(s) for review` : ""}`);
}

// Timeline, edit list and assembly settings. Failed, aborted and mismatched scenes stay in
// timeline.json but are left out of segments.tsv so they do not reach the video by default.
const timeline = buildTimeline(rows);
writePrivate(path.join(OUT, "timeline.json"), JSON.stringify({ title: r(plan.title || slug), take: decision.take, wordsPerMinute: WPM, tts: plan.narration?.tts || {}, totalMs: timeline.totalMs, scenes: timeline.scenes }, null, 2));
const usable = timeline.scenes.filter((s) => s.clip && ["ok", "verified"].includes(s.status));
writePrivate(path.join(OUT, "segments.tsv"), segmentsTsv({ scenes: usable }));
writePrivate(path.join(OUT, "assembly.conf"), `# Read by make-video.sh\nend_hold_seconds=${Math.max(0, Math.round(END_HOLD_MS)) / 1000}\n`);
writePrivate(path.join(OUT, "writes-report.json"), JSON.stringify({ take: decision.take, generatedAt: new Date().toISOString(), writes: report }, null, 2));
writePrivate(path.join(OUT, "privacy-review.json"), JSON.stringify({ take: decision.take, note: "Masked hits only; raw page text is never stored. Run review-demo.mjs and check every tile.", scenes: privacy }, null, 2));
writePrivate(path.join(OUT, "plan.json"), r(JSON.stringify(plan, null, 2)));

const script = [`# ${r(plan.title || slug)}`, "", r(plan.summary || ""), "", `Take ${decision.take}. Narration pace: ${WPM} words per minute.`, ""];
for (const [i, s] of timeline.scenes.entries()) {
  script.push(`## Scene ${i + 1}: ${s.title} (${s.status})`, "", `- Route: \`${s.route}\``,
    s.clip ? `- Recorded length: ${(s.durationMs / 1000).toFixed(1)}s, starts at ${(s.startMs / 1000).toFixed(1)}s${usable.includes(s) ? "" : " (left out of segments.tsv)"}` : `- Not recorded${s.reason ? `: ${s.reason}` : ""}`,
    `- Narration needs about ${((countWords(s.narration) / WPM) * 60).toFixed(1)}s`,
    ...(s.checks || []).map((c) => `- Verify: ${c.check}: ${c.pass ? "pass" : `FAIL (got ${c.actual})`}`),
    ...(s.error ? [`- Error: ${s.error}`] : []), "", `> ${s.narration || "(no narration)"}`, "");
}
writePrivate(path.join(OUT, "script.md"), script.join("\n"));
const makeVideo = path.join(OUT, "make-video.sh");
writePrivate(makeVideo, fs.readFileSync(path.join(here, "make-video.sh"), "utf8"));
fs.chmodSync(makeVideo, 0o700);

if (usable.length) {
  const { cues, overruns } = writeDemoCues(cfg, OUT);
  log(`${cues.length} narration cue(s); see narration/fit.md`);
  for (const c of overruns) log(`OVERRUN cue ${c.index} (${c.scene}): needs ${(c.neededMs / 1000).toFixed(1)}s, has ${(c.availableMs / 1000).toFixed(1)}s`);
} else log("no usable scenes, so no captions or narration cues were written");

Object.assign(takeRecord, { finishedAt: new Date().toISOString(), statuses: Object.fromEntries(rows.map((s) => [s.id, s.status])) });
saveLedger();
const bad = report.filter((w) => w.status !== "verified");
if (bad.length) log(`${bad.length} write(s) not verified; see writes-report.json and ${findingsPath}`);
log(`demo take ${decision.take} written to ${OUT}`);
if (abort) throw abort;
