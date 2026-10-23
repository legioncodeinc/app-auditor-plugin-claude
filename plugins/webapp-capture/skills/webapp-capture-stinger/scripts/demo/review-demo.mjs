// Human privacy review for a recorded demo: tiles each scene clip into a contact sheet
// (ffmpeg) and lists the masked email, phone and redact.patterns hits found in page text
// per scene during recording. Nothing here changes the app. Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... DEMO_DIR=<output.demo>/<slug> [EVERY_SECONDS=2] node demo/review-demo.mjs
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import { loadConfig, log } from "../lib/common.mjs";
import { mkdirPrivate, redactPatterns, writePrivate } from "../lib/demo-cues.mjs";

const cfg = loadConfig();
if (!process.env.DEMO_DIR) throw new Error("Set DEMO_DIR to the recorded demo folder");
const dir = path.resolve(process.env.DEMO_DIR);
const every = Number(process.env.EVERY_SECONDS || 2);
if (!(every > 0 && every <= 30)) throw new Error("EVERY_SECONDS must be between 0 and 30");
const timeline = JSON.parse(fs.readFileSync(path.join(dir, "timeline.json"), "utf8"));
const review = mkdirPrivate(path.join(dir, "review"));

// ffmpeg writes to a pipe; this script owns the file, so ffmpeg never opens an output path.
const sheet = (clip) => new Promise((resolve, reject) => {
  if (!/^(?:scenes|clips)\/[A-Za-z0-9._-]+\.webm$/.test(clip) || clip.includes("..")) return reject(new Error(`refusing unexpected clip path ${clip}`));
  const input = path.join(dir, clip);
  const st = fs.lstatSync(input);
  if (!st.isFile() || st.isSymbolicLink() || st.nlink !== 1) return reject(new Error(`refusing linked or unusual clip ${clip}`));
  const child = spawn("ffmpeg", ["-v", "error", "-i", input, "-vf", `fps=1/${every},scale=480:-1,tile=4x4:padding=6:margin=6`, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"], { stdio: ["ignore", "pipe", "pipe"] });
  const chunks = []; let detail = "";
  child.stdout.on("data", (d) => chunks.push(d)); child.stderr.on("data", (d) => { detail += d; });
  child.once("error", reject);
  child.once("exit", (code) => code === 0 ? resolve(Buffer.concat(chunks)) : reject(new Error(`contact sheet failed for ${clip}: ${detail.slice(0, 300)}`)));
});

const lines = ["# Demo privacy review", "", `Contact sheets: one tile every ${every}s per scene. Check every tile for names, emails, phone numbers, hover cards and tooltips.`, ""];
const privacyFile = path.join(dir, "privacy-review.json");
const privacy = fs.existsSync(privacyFile) ? JSON.parse(fs.readFileSync(privacyFile, "utf8")) : { scenes: [] };
for (const scene of timeline.scenes) {
  lines.push(`## ${scene.id}: ${scene.title || ""} (${scene.status})`, "");
  if (scene.clip) {
    const name = `${String(scene.id).replace(/[^A-Za-z0-9._-]+/g, "-")}-sheet.png`;
    writePrivate(path.join(review, name), await sheet(scene.clip));
    lines.push(`- Sheet: review/${name}`);
  }
  const hits = privacy.scenes.find((s) => s.id === scene.id)?.hits || [];
  lines.push(hits.length ? `- Text hits for human review: ${hits.map((h) => `${h.kind} ${h.masked} x${h.count}${h.action ? ` (after action ${h.action})` : " (on load)"}`).join("; ")}` : "- Text hits: none found by the scan (pixels can still show data the scan cannot read)", "");
}
writePrivate(path.join(review, "REVIEW.md"), redactPatterns(cfg, lines.join("\n")));
const total = privacy.scenes.reduce((n, s) => n + s.hits.length, 0);
log(`review written to ${path.join(review, "REVIEW.md")}; ${total} masked text hit(s) to check`);
