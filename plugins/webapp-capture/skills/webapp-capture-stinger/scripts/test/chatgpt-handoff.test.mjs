import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { writeDemoCues } from "../lib/demo-cues.mjs";

const script = new URL("../demo/chatgpt-handoff.mjs", import.meta.url).pathname;
const finish = new URL("../../../demo-intro-video/scripts/finish_video.py", import.meta.url).pathname;
const has = (bin, flag = "-version") => spawnSync(bin, [flag], { stdio: "ignore" }).status === 0;
const ready = has("ffmpeg") && has("ffprobe") && has("unzip", "-v");
const root = fs.mkdtempSync(path.join(os.tmpdir(), "webapp-handoff-"));
test.after(() => fs.rmSync(root, { recursive: true, force: true }));

const config = path.join(root, "capture.config.json");
fs.writeFileSync(config, JSON.stringify({ app: { origin: "http://127.0.0.1:9" }, auth: { storageState: "auth.json" }, browser: { viewport: { width: 800, height: 600 }, deviceScaleFactor: 1 }, routes: { discover: "list", list: ["/"] }, tabs: { selector: "[role=tab]" }, redact: { patterns: ["ACME-\\d+"] }, output: { inventory: "inv", demo: "demo" } }));

function demo(name, { reviewed = true } = {}) {
  const dir = path.join(root, "demo", name);
  fs.mkdirSync(path.join(dir, "scenes"), { recursive: true });
  fs.writeFileSync(path.join(dir, "timeline.json"), JSON.stringify({ title: "Book a job for ACME-42", wordsPerMinute: 140, tts: { style: "warm" }, scenes: [
    { id: "hook", title: "Hook", clip: "scenes/01-hook.webm", startMs: 0, durationMs: 4000, narration: "Here is the schedule." },
    { id: "book", title: "Book", clip: "scenes/02-book.webm", startMs: 4000, durationMs: 5000, narration: "Drag a job onto Tuesday." },
  ] }));
  fs.writeFileSync(path.join(dir, "segments.tsv"), "scenes/01-hook.webm\t0\t4000\thook\nscenes/02-book.webm\t0\t5000\tbook\n");
  writeDemoCues({}, dir);
  fs.writeFileSync(path.join(dir, "script.md"), "# Script\n");
  execFileSync("ffmpeg", ["-v", "error", "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30:duration=9", "-c:v", "libx264", "-pix_fmt", "yuv420p", path.join(dir, "demo-silent.mp4")]);
  if (reviewed) { fs.mkdirSync(path.join(dir, "review")); fs.writeFileSync(path.join(dir, "review", "REVIEW.md"), "# Demo privacy review\n"); }
  return dir;
}
const run = (dir, env = {}) => spawnSync(process.execPath, [script], { encoding: "utf8", env: { ...process.env, CAPTURE_CONFIG: config, DEMO_DIR: dir, ...env } });

test("handoff packages only what ChatGPT needs, redacted, with the stitch script", { skip: !ready && "ffmpeg, ffprobe or unzip missing" }, () => {
  const dir = demo("valid");
  const result = run(dir);
  assert.equal(result.status, 0, result.stderr);
  const zip = path.join(root, "demo", "valid-chatgpt-handoff.zip");
  assert.equal(fs.statSync(zip).mode & 0o777, 0o600);
  const listing = execFileSync("unzip", ["-Z1", zip], { encoding: "utf8" }).split("\n").filter((l) => l && !l.endsWith("/")).map((l) => l.replace(/^valid-chatgpt-handoff\//, "")).sort();
  assert.deepEqual(listing, ["CHATGPT-INSTRUCTIONS.md", "INTRO-BRIEF.md", "captions.vtt", "finish_video.py", "narration/cues.json", "narration/fit.md", "narration/tts-manifest.json", "narration/tts/01-hook.txt", "narration/tts/02-book.txt", "script.md", "timeline.json", "titles.srt", "video/demo-silent.mp4"]);
  const instructions = execFileSync("unzip", ["-p", zip, "valid-chatgpt-handoff/CHATGPT-INSTRUCTIONS.md"], { encoding: "utf8" });
  assert.match(instructions, /Title: \*\*Book a job for \[REDACTED\]\*\*/);
  assert.match(instructions, /\| 2 \| book \| 4\.3s \|/);
  assert.ok(!/\{\{\w+\}\}/.test(instructions), "unfilled placeholder");
  // A second run never overwrites the zip.
  const again = run(dir);
  assert.notEqual(again.status, 0);
  assert.match(again.stderr, /already exists/);
});

test("handoff refuses an unreviewed demo and linked inputs", { skip: !ready && "ffmpeg, ffprobe or unzip missing" }, () => {
  const unreviewed = run(demo("unreviewed", { reviewed: false }));
  assert.notEqual(unreviewed.status, 0);
  assert.match(unreviewed.stderr, /Run review-demo\.mjs and check every contact sheet first/);
  const linked = demo("linked");
  fs.renameSync(path.join(linked, "captions.vtt"), path.join(root, "captions-outside.vtt"));
  fs.symlinkSync(path.join(root, "captions-outside.vtt"), path.join(linked, "captions.vtt"));
  const result = run(linked);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /refusing linked input captions\.vtt/);
  assert.ok(!fs.existsSync(path.join(root, "demo", "linked-chatgpt-handoff.zip")));
});

test("finish_video.py places voice at cue time after the intro and shifts captions", { skip: (!ready || !has("python3", "--version")) && "python3, ffmpeg or unzip missing" }, () => {
  const dir = demo("finish");
  assert.equal(run(dir).status, 0);
  const work = path.join(root, "finish-unzip");
  fs.mkdirSync(work);
  execFileSync("unzip", ["-q", path.join(root, "demo", "finish-chatgpt-handoff.zip")], { cwd: work });
  const h = path.join(work, "finish-chatgpt-handoff");
  const tone = (file, seconds) => execFileSync("ffmpeg", ["-v", "error", "-f", "lavfi", "-i", `sine=frequency=500:duration=${seconds}`, path.join(h, "narration", "audio", file)]);
  tone("01-hook.mp3", 5); // longer than its 3.4s window
  const over = spawnSync("python3", [finish, "--dir", h, "--intro", "intro/intro.mp4"], { encoding: "utf8" });
  assert.notEqual(over.status, 0);
  assert.match(over.stderr, /01-hook\.mp3 is 5\.0s but cue 1 has 3\.4s/);
  fs.rmSync(path.join(h, "narration", "audio", "01-hook.mp3"));
  tone("01-hook.mp3", 1.5);
  tone("02-book.mp3", 2);
  execFileSync("ffmpeg", ["-v", "error", "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=24:duration=3", "-c:v", "libx264", "-pix_fmt", "yuv420p", path.join(h, "intro", "intro.mp4")]);
  const done = spawnSync("python3", [finish, "--dir", h, "--intro", "intro/intro.mp4"], { encoding: "utf8" });
  assert.equal(done.status, 0, done.stderr);
  const report = JSON.parse(done.stdout);
  assert.equal(report.introSeconds, 3);
  assert.ok(Math.abs(report.seconds - 12) < 0.2, `length ${report.seconds}`);
  assert.match(fs.readFileSync(path.join(h, "finished", "work", "captions.vtt"), "utf8"), /00:00:03\.300 --> /);
  const silence = spawnSync("ffmpeg", ["-i", path.join(h, "finished", "demo-final.mp4"), "-map", "0:a", "-af", "silencedetect=noise=-40dB:d=0.2", "-f", "null", "-"], { encoding: "utf8" }).stderr;
  const firstVoice = Number(silence.match(/silence_end: ([\d.]+)/)[1]);
  assert.ok(Math.abs(firstVoice - 3.3) < 0.05, `first voice at ${firstVoice}`);
  const streams = execFileSync("ffprobe", ["-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", path.join(h, "finished", "demo-final.mp4")], { encoding: "utf8" }).trim().split("\n").sort();
  assert.deepEqual(streams, ["audio", "subtitle", "video"]);
});
