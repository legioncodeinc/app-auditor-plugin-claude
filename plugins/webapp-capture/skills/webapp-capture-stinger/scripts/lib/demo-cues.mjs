// Write captions, scene-title SRT, narration timings and TTS clips for a demo folder
// from its timeline.json and segments.tsv. Shared by record-demo.mjs and build-cues.mjs.
// Designed by Legion Code Inc.
import fs from "node:fs";
import path from "node:path";
import { editedSpans, parseSegments, titleCues, toSrt, toVtt } from "./demo-plan.mjs";
import { fitReport, narrationCues, ttsClips } from "./narration.mjs";

/** Apply redact.patterns to exported text. */
export function redactPatterns(cfg, text) {
  return (cfg?.redact?.patterns || []).reduce((v, p) => v.replace(new RegExp(p, "gi"), "[REDACTED]"), String(text));
}
/** Create a private directory; refuse when it (or the path to it inside the output) is a symlink. */
export function mkdirPrivate(dir) {
  if (fs.existsSync(dir) && fs.lstatSync(dir).isSymbolicLink()) throw new Error(`refusing symlinked output directory ${dir}`);
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  return dir;
}
// O_NOFOLLOW makes open() fail on a symlink; the link-count check catches hard links.
const openPrivate = (file, flags) => {
  mkdirPrivate(path.dirname(file));
  let fd;
  try { fd = fs.openSync(file, flags | fs.constants.O_NOFOLLOW, 0o600); }
  catch (e) { if (e.code === "ELOOP" || e.code === "EMLINK") throw new Error(`refusing to write through a symlink: ${file}`); throw e; }
  const st = fs.fstatSync(fd);
  if (!st.isFile() || st.nlink !== 1) { fs.closeSync(fd); throw new Error(`refusing to write a linked or unusual file: ${file}`); }
  fs.fchmodSync(fd, 0o600);
  return fd;
};
const writeAll = (fd, data) => {
  const buf = typeof data === "string" ? Buffer.from(data) : data;
  for (let off = 0; off < buf.length;) off += fs.writeSync(fd, buf, off, buf.length - off);
};
/** Owner-only write that never follows a symlink or writes through a hard link. */
export const writePrivate = (file, data) => {
  const fd = openPrivate(file, fs.constants.O_WRONLY | fs.constants.O_CREAT);
  try { fs.ftruncateSync(fd, 0); writeAll(fd, data); } finally { fs.closeSync(fd); }
};
export const appendPrivate = (file, text) => {
  const fd = openPrivate(file, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_APPEND);
  try { writeAll(fd, String(text)); } finally { fs.closeSync(fd); }
};

export function writeDemoCues(cfg, dir) {
  const timeline = JSON.parse(fs.readFileSync(path.join(dir, "timeline.json"), "utf8"));
  const segments = parseSegments(fs.readFileSync(path.join(dir, "segments.tsv"), "utf8"));
  const { spans, totalMs } = editedSpans(timeline, segments);
  const wpm = timeline.wordsPerMinute || 140;
  const cues = narrationCues(spans, { wordsPerMinute: wpm });
  const r = (s) => redactPatterns(cfg, s);
  writePrivate(path.join(dir, "captions.vtt"), r(toVtt(cues)));
  writePrivate(path.join(dir, "titles.srt"), r(toSrt(titleCues(spans))));
  writePrivate(path.join(dir, "narration", "cues.json"), r(JSON.stringify({ wordsPerMinute: wpm, totalMs, cues: cues.map(({ narration, ...c }) => c) }, null, 2)));
  writePrivate(path.join(dir, "narration", "fit.md"), r(fitReport(cues, { wordsPerMinute: wpm })));
  const { files, manifest } = ttsClips(cues, timeline.tts || {});
  // Cue numbers change when segments are reordered, so clear clip texts from an earlier build.
  const ttsDir = path.join(dir, "narration", "tts");
  if (fs.existsSync(ttsDir)) for (const name of fs.readdirSync(ttsDir)) {
    const p = path.join(ttsDir, name);
    if (/^\d{2}-[A-Za-z0-9._-]+\.txt$/.test(name) && fs.lstatSync(p).isFile()) fs.rmSync(p);
  }
  for (const f of files) writePrivate(path.join(dir, "narration", "tts", f.name), r(f.text));
  writePrivate(path.join(dir, "narration", "tts-manifest.json"), r(JSON.stringify(manifest, null, 2)));
  return { cues, totalMs, overruns: cues.filter((c) => c.status === "overrun") };
}
