// Package a recorded demo for ChatGPT to finish: voiceover (ElevenLabs), intro video
// (free B-roll or the Replicate video MCP), and the final stitch. The zip holds only what
// those steps need: the silent demo, captions, titles, narration texts and manifest, an
// intro brief, CHATGPT-INSTRUCTIONS.md and finish_video.py. It refuses to package a demo
// whose privacy review has not been written, because the zip leaves this machine.
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... DEMO_DIR=<output.demo>/<slug> [INTRO_BRIEF=brief.md] [OUT=<zip>] node demo/chatgpt-handoff.mjs
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { loadConfig, log, slugify } from "../lib/common.mjs";
import { redactPatterns, writePrivate } from "../lib/demo-cues.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const cfg = loadConfig();
if (!process.env.DEMO_DIR) throw new Error("Set DEMO_DIR to the recorded demo folder");
const dir = path.resolve(process.env.DEMO_DIR);
const need = (rel) => {
  const p = path.join(dir, rel);
  if (!fs.existsSync(p)) throw new Error(`missing ${rel} in ${dir}. ${rel === "demo-silent.mp4" ? "Run ./make-video.sh in the demo folder first." : rel.startsWith("review") ? "Run review-demo.mjs and check every contact sheet first: this zip leaves your machine." : "Record the demo and run build-cues.mjs first."}`);
  const st = fs.lstatSync(p);
  if (st.isSymbolicLink() || (st.isFile() && st.nlink !== 1)) throw new Error(`refusing linked input ${rel}`);
  return p;
};
need("review/REVIEW.md");
const timeline = JSON.parse(fs.readFileSync(need("timeline.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(need("narration/tts-manifest.json"), "utf8"));
const cues = JSON.parse(fs.readFileSync(need("narration/cues.json"), "utf8"));
const r = (s) => redactPatterns(cfg, s);

const slug = slugify(path.basename(dir)) || "demo";
const OUT = path.resolve(process.env.OUT || path.join(path.dirname(dir), `${slug}-chatgpt-handoff.zip`));
if (fs.existsSync(OUT)) throw new Error(`${OUT} already exists. Move it aside; earlier output is never overwritten.`);

const stage = fs.mkdtempSync(path.join(os.tmpdir(), "webapp-capture-handoff-"));
const root = path.join(stage, `${slug}-chatgpt-handoff`);
const copy = (rel, dest = rel) => writePrivate(path.join(root, dest), fs.readFileSync(need(rel)));
try {
  copy("demo-silent.mp4", "video/demo-silent.mp4");
  for (const rel of ["captions.vtt", "titles.srt", "script.md", "timeline.json", "narration/cues.json", "narration/fit.md", "narration/tts-manifest.json"]) copy(rel);
  for (const c of manifest.clips) copy(`narration/tts/${c.textFile}`);
  fs.mkdirSync(path.join(root, "narration", "audio"), { mode: 0o700 });
  fs.mkdirSync(path.join(root, "intro"), { mode: 0o700 });

  // The stitch script ships with the demo-intro-video skill; a skill-only install may not have it.
  const finish = path.join(here, "..", "..", "..", "demo-intro-video", "scripts", "finish_video.py");
  if (fs.existsSync(finish)) writePrivate(path.join(root, "finish_video.py"), fs.readFileSync(finish));
  else log("finish_video.py not found next to this skill (skill-only install?); the instructions still describe the stitch");

  const demoSeconds = (Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", need("demo-silent.mp4")], { encoding: "utf8" })) || 0).toFixed(1);
  const table = manifest.clips.map((c) => `| ${c.cue} | ${c.scene} | ${(c.startMs / 1000).toFixed(1)}s | ${(c.maxMs / 1000).toFixed(1)}s | \`narration/tts/${c.textFile}\` |`).join("\n");
  const template = fs.readFileSync(path.join(here, "..", "..", "references", "prompts", "chatgpt-finish.md"), "utf8");
  const fill = { TITLE: timeline.title || slug, DEMO_SECONDS: demoSeconds, CUE_COUNT: String(manifest.clips.length), WPM: String(cues.wordsPerMinute || timeline.wordsPerMinute || 140), DATE: new Date().toISOString().slice(0, 10), CUE_TABLE: table };
  writePrivate(path.join(root, "CHATGPT-INSTRUCTIONS.md"), r(template.replace(/\{\{(\w+)\}\}/g, (m, k) => fill[k] ?? m)));

  const brief = process.env.INTRO_BRIEF ? fs.readFileSync(path.resolve(process.env.INTRO_BRIEF), "utf8")
    : [`# Intro brief: ${timeline.title || slug}`, "", "Fill in or confirm with the user before making the intro.", "",
      "- Product and what it does: (one sentence)", "- Audience: (who watches this)", "- Brand colors: (hex values)",
      "- Length: 5 seconds", "- Custom footage required: no (use free stock B-roll unless this says yes)",
      "- Mood: calm, modern, trustworthy", "- Must avoid: text, logos, app screens, identifiable faces", ""].join("\n");
  writePrivate(path.join(root, "INTRO-BRIEF.md"), r(brief));

  // Zip: system zip, else tar with zip format (Windows 10+), as design-handoff.mjs does.
  try { execFileSync("zip", ["-qr", OUT, path.basename(root)], { cwd: stage, stdio: "ignore" }); }
  catch { execFileSync("tar", ["-a", "-cf", OUT, path.basename(root)], { cwd: stage, stdio: "ignore" }); }
  fs.chmodSync(OUT, 0o600);
  const files = execFileSync("find", [root, "-type", "f"], { encoding: "utf8" }).trim().split("\n").length;
  log(`handoff written to ${OUT} (${(fs.statSync(OUT).size / 1048576).toFixed(1)} MB, ${files} files). Open it in ChatGPT and say: "Read CHATGPT-INSTRUCTIONS.md and finish this demo video."`);
} finally {
  fs.rmSync(stage, { recursive: true, force: true });
}
