import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { appendPrivate, mkdirPrivate, writePrivate } from "../lib/demo-cues.mjs";

const root = fs.mkdtempSync(path.join(os.tmpdir(), "webapp-private-"));
test.after(() => fs.rmSync(root, { recursive: true, force: true }));

test("private writes are owner-only and tighten an existing file", () => {
  const file = path.join(root, "a", "ledger.json");
  writePrivate(file, "first");
  assert.equal(fs.statSync(file).mode & 0o777, 0o600);
  assert.equal(fs.statSync(path.dirname(file)).mode & 0o777, 0o700);
  fs.chmodSync(file, 0o644);
  writePrivate(file, "second, longer text");
  writePrivate(file, "third");
  assert.equal(fs.readFileSync(file, "utf8"), "third");
  assert.equal(fs.statSync(file).mode & 0o777, 0o600);
  appendPrivate(file, " plus");
  assert.equal(fs.readFileSync(file, "utf8"), "third plus");
  const big = Buffer.alloc(3 * 1024 * 1024, 7);
  writePrivate(path.join(root, "a", "sheet.png"), big);
  assert.equal(fs.statSync(path.join(root, "a", "sheet.png")).size, big.length);
});

test("private writes refuse symlinks, hard links and symlinked directories", () => {
  const outside = path.join(root, "outside.txt");
  fs.writeFileSync(outside, "unchanged outside sentinel");
  const dir = mkdirPrivate(path.join(root, "demo"));
  fs.symlinkSync(outside, path.join(dir, "findings.md"));
  assert.throws(() => writePrivate(path.join(dir, "findings.md"), "x"), /symlink/);
  assert.throws(() => appendPrivate(path.join(dir, "findings.md"), "x"), /symlink/);
  fs.linkSync(outside, path.join(dir, "ledger.json"));
  assert.throws(() => writePrivate(path.join(dir, "ledger.json"), "x"), /linked or unusual file/);
  assert.throws(() => appendPrivate(path.join(dir, "ledger.json"), "x"), /linked or unusual file/);
  fs.symlinkSync(root, path.join(dir, "review"));
  assert.throws(() => mkdirPrivate(path.join(dir, "review")), /symlinked output directory/);
  assert.throws(() => writePrivate(path.join(dir, "review", "REVIEW.md"), "x"), /symlinked output directory/);
  assert.equal(fs.readFileSync(outside, "utf8"), "unchanged outside sentinel");
});
