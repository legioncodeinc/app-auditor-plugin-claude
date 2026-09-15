# jscpd: copy/paste detector for programming source code

- URL: https://github.com/kucherenko/jscpd
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): version 5.2.0 (per CITATION.cff in repo, year 2026)

Content below is extracted verbatim (with minor reformatting) from `README.md` and the linked `docs/rust.md` (CLI reference) at https://raw.githubusercontent.com/kucherenko/jscpd/master/README.md and https://raw.githubusercontent.com/kucherenko/jscpd/master/docs/rust.md.

## Tagline

> Copy/paste detector for programming source code. 220+ formats, language-aware tokenization, exact, renamed and near-miss clones, Rust engine, self-contained binary, AI-ready with MCP server and token-efficient reporter.

**Documentation:** https://jscpd.dev

jscpd reads code the way its language defines it, not as plain text. Each of the 224 formats is tokenized with its own comment and string syntax, so `#` in Python, `--` in SQL or `'` in Visual Basic opens a comment only where the language says so. JavaScript, TypeScript, JSX and TSX go through the [oxc](https://oxc.rs) parser, which handles template literals, regular expressions, JSX and decorators, and can erase TypeScript-only syntax so a `.ts` file matches its `.js` twin. Vue, Svelte, Astro, Markdown and Razor files are split into their embedded languages first, and each block is tokenized as the language it contains. Identifiers, keywords and literals are classified, which is what lets the renamed-clone pass replace names while keeping keywords in place.

On that token stream jscpd runs the [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm) algorithm to find duplicated blocks across files. Opt-in passes extend it to blocks that differ only in names or values (Type-2) and to copies with a few edited lines or the same function structure (Type-3), each reported with its kind and a similarity score.

## Quick Start

```bash
# macOS / Linux
curl -fsSL https://jscpd.dev/install.sh | bash

# Windows (PowerShell)
irm https://jscpd.dev/install.ps1 | iex

# No install — run once with npx (Node.js)
npx jscpd .
```

Then scan a project:

```bash
jscpd /path/to/code
```

### Other install methods

| Method | Command | Notes |
|--------|---------|-------|
| npm | `npm install -g jscpd` | Installs the `jscpd` command; prebuilt binary, no Node.js at runtime |
| npm (`cpd` command) | `npm install -g cpd` | Same binary, exposed as `cpd` |
| PyPI | `pip install jscpd` | Platform wheels with both commands; also `pipx install jscpd`, `uv tool install jscpd`, or `uvx jscpd .` to run without installing |
| Cargo | `cargo install jscpd` | Builds from crates.io; installs both `jscpd` and `cpd` |
| Homebrew | `brew install jscpd` | macOS / Linux |
| Nix | `nix run github:kucherenko/jscpd -- /path/to/code` | Or `nix profile install github:kucherenko/jscpd` |
| Docker | `docker run --rm -v "$PWD:/src" ghcr.io/kucherenko/jscpd .` | Multi-arch image built from the release binaries |

### GitHub Action

```yaml
- uses: kucherenko/jscpd@v5
  with:
    threshold: 5
```

Uploads SARIF results to GitHub Code Scanning by default.

## Features (from README)

- **Language-aware tokenization** for all 224 formats, the oxc parser for JavaScript/TypeScript/JSX/TSX, embedded-language extraction for Vue, Svelte, Astro, Markdown and Razor, keyword/identifier/literal classification
- **224 language formats** with cross-format detection (Vue SFC, Svelte, Astro, Markdown) and `--cross-formats` groups to match clones across JavaScript and TypeScript
- **Prebuilt for 8 platforms** (macOS arm64/x64, Linux arm64/x64 glibc and musl, Windows arm64/x64)
- **Type-2 clones** — `--ignore-identifiers`, `--ignore-literals` and `--ignore-annotations` find blocks that differ only in names, literal values or annotations, reported as `renamed`
- **Type-3 near-miss clones** — `--max-gap-lines N` merges a copy with a few inserted or changed lines into one `similar` clone with a similarity score; `--similarity 0.85` compares whole JavaScript/TypeScript functions by syntax-tree structure
- **Clone kinds in every reporter** — `exact`, `renamed` or `similar`; default runs report only `exact` clones and output is unchanged from earlier versions
- **15 reporters**: `console`, `console-full`, `json`, `xml`, `csv`, `html`, `markdown`, `badge`, `sarif`, `codeclimate`, `openmetrics`, `ai`, `xcode`, `threshold`, `silent`
- **Clone baseline** — gate CI on *new* duplication only via `--baseline .jscpd-baseline.json` with `--fail-on-new-clones[=N]`, or `--baseline-from-ref origin/main` without a committed file
- **Exit codes you can gate on** — unknown `--format`, missing scan path, or a reporter that cannot write exits 1; `--fail-on-empty` fails a scan that analyzed no files
- **GitLab-ready reporters** — `codeclimate` (`gl-code-quality-report.json`) and `openmetrics` (`jscpd-metrics.txt`)
- **Git blame** with side-by-side author comparison (`--blame --reporters console-full`)
- **`--history`** — duplication trend over git history
- **`--summary`** — codebase summary: top files/folders by tokens, lines, size, complexity
- **`--mcp`** — built-in MCP server over stdio
- **AI reporter** — token-efficient output for LLM pipelines (~79% fewer tokens than console)
- **`--skip-local`** / **`--skip-isolated`** — monorepo-aware duplication filtering
- **`--workers`** — control parallelism (default: all CPU cores)
- **Config discovery** — `.jscpd.json`, `.config/jscpd.json`, or the `jscpd` key in `package.json`
- **Symbolic links skipped unless `--follow-symlinks`** (v4 followed them by default)
- **Quiet in pipelines** — tips print only on an interactive terminal; `--no-tips`, `CI` or `JSCPD_NO_TIPS` switch them off

## Who Uses jscpd

The `jscpd` npm package is downloaded **10M+ times per month**, and ~5,000 repositories declare it on GitHub's dependents graph. Bundled by GitHub Super Linter, MegaLinter, and Codacy. Used directly (with a `.jscpd.json`) by projects including RimSort, Google Cloud Contact Center AI samples, and Drifty.

## Benchmark (from README, fixtures/ corpus, 547 files, 150+ formats, default thresholds)

| Tool | Time | Files | Clones | Dup Lines |
|------|------|-------|--------|-----------|
| jscpd | 84ms | 347 | 212 | 9,133 |
| jscpd-rs | 111ms | 360 | 222 | 10,317 |
| Duplo | 162ms | 319 | 518 | 13,049 |
| Fallow dupes | 164ms | 34 | 10 | 3,137 |
| Simian | 964ms | 547 | 424 | 15,351 |
| PMD CPD | 35.980s | 71 | 56 | 2,267 |

---

## CLI Reference (from docs/rust.md)

jscpd v5 is a Rust engine shipped as a self-contained binary: no runtime required, same CLI flags, reporters and `.jscpd.json` config as the earlier Node.js versions. It is distributed under two command names: `jscpd` (npm package `jscpd`) and `cpd` (npm package `cpd`, or via crates.io which installs both).

```bash
jscpd [OPTIONS] [PATH]...
cpd [OPTIONS] [PATH]...
```

### Options (selected, with defaults)

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--min-tokens` | `-k` | Minimum tokens in a clone | 50 |
| `--min-lines` | `-l` | Minimum lines in a clone | 5 |
| `--max-lines` | `-x` | Maximum source file lines | — |
| `--max-size` | `-z` | Skip files larger than SIZE (e.g. `1kb`, `1mb`, `100kb`) | no limit |
| `--mode` | `-m` | Detection mode: `mild`, `weak`, `strict` | `mild` |
| `--ignore-pattern` | | Comma-separated regular expressions; matched source text is excluded from clone detection | — |
| `--workers` | | Number of worker threads for parallel tokenization/detection | auto (all CPU cores) |
| `--no-colors` | | Disable ANSI color output | off |
| `--absolute` | `-a` | Use absolute paths in reports | off |
| `--follow-symlinks` | | Follow symbolic links while walking | off |
| `--ignore-case` | | Ignore case of symbols in code (experimental) | off |
| `--ignore-identifiers` | | Treat all identifiers as equal (Type-2 clones) | off |
| `--ignore-literals` | | Treat all string literals as equal and all numeric literals as equal | off |
| `--ignore-annotations` | | Skip annotations and decorators (`@Name`, `@Name(...)`) before detection | off |
| `--max-gap-lines` | | Merge clones of one file pair separated by at most N unmatched lines into one near-miss clone reported as `similar` | 0 (off) |
| `--similarity` | | Report JS/TS function pairs whose syntax-tree similarity reaches RATIO (0,1] as `similar` clones; `1` = exact matches only | 1 (off) |
| `--formats-exts` | | Custom format-to-extension mapping (e.g. `javascript:es,es6;dart:dt`) | — |
| `--formats-names` | | Custom format-to-filename mapping | — |
| `--cross-formats` | | Detect clones across formats: `;`-separated groups of `,`-separated formats. Preset `js-ts` = `javascript,jsx,typescript,tsx` | — |
| `--list` | | List all supported formats and exit | — |
| `--skip-local` | | Skip clones where both fragments are in the same directory | off |
| `--skip-isolated` | | Skip clones between different folders of the same isolation group | — |
| `--baseline` | | Clone baseline file (e.g. `.jscpd-baseline.json`) | — |
| `--update-baseline` | | Rewrite the baseline file from the current run (requires `--baseline`) | off |
| `--fail-on-new-clones` | | Exit 1 when more than N new clones are found (alone means N=0; requires `--baseline` or `--baseline-from-ref`) | — |
| `--fail-on-empty` | | Exit 1 when the scan analyzes no files | off |
| `--baseline-from-ref` | | Compare against an ephemeral baseline built from a git ref's tree (e.g. `origin/main`). Conflicts with `--baseline` | — |
| `--sarif-error-tokens` | | Report SARIF results as `error` for clones with at least this many tokens | — (all `warning`) |
| `--min-duplicated-lines` | | Minimum percentage of duplication to report (0-100) | 0 |
| `--mcp` | | Serve the Model Context Protocol over stdio | off |
| `--summary` | | Print a codebase summary | off |
| `--summary-top` | | Number of entries in each summary top list | 10 |
| `--summary-by` | | Summary sort metric: `tokens`, `lines`, `size`, `complexity` | `tokens` |
| `--history` | | Duplication trend over git history: scan every commit in RANGE | — |
| `--history-since` | | Select commits since DATE | — |
| `--history-every` | | Keep every Nth commit of the series, counted from the newest | 1 |
| `--history-limit` | | Maximum number of commits in the series | 30 |
| `--silent` | `-s` | Suppress console output | off |
| `--no-tips` | | Suppress tips and promotional messages | off |
| `--version` | `-V` | Print version | — |
| `--help` | `-h` | Print help | — |

### Reporters (15 built-in)

| Reporter | Output |
|----------|--------|
| `console` | Clone list + statistics table (default) |
| `console-full` | Clone list with source snippets; with `--blame` shows side-by-side author comparison |
| `json` | `report/jscpd-report.json` |
| `xml` | `report/jscpd-report.xml` |
| `csv` | `report/jscpd-report.csv` |
| `html` | `report/jscpd-report.html` |
| `markdown` | `report/jscpd-report.md` |
| `badge` | `report/jscpd-badge.svg` + `report/jscpd-lines-badge.svg` |
| `sarif` | `report/jscpd-report.sarif` (GitHub Code Scanning) |
| `codeclimate` (alias `gitlab`) | `report/gl-code-quality-report.json` |
| `openmetrics` | `report/jscpd-metrics.txt` |
| `ai` | Token-efficient output for LLM pipelines |
| `xcode` | Xcode-compatible warnings |
| `threshold` | Exit 1 if duplication percentage exceeds `--threshold` |
| `silent` | No console output |

File reporters write into the `--output` directory (default `report/`) using the `jscpd-report.*` prefix.

### Exit Codes

| Code | When |
|------|------|
| 0 | The scan ran and no gate fired; clones may still have been found and reported |
| 1 | `--threshold` exceeded; `--fail-on-new-clones` exceeded; `--fail-on-empty` and no file was analyzed; a reporter failed to write its output; a scan path does not exist; `--format` names a format that is not supported; an invalid flag combination or unreadable `--config` file |
| N | `--exit-code N` (default 1) when at least one clone was found |
| 2 | Command-line parse errors: an unknown flag or a missing value |

A scan that analyzes no files (paths exist but nothing matched `--format`/`--ignore`/`--pattern`, or every file was below `--min-tokens`) prints `Warning: jscpd analyzed no files` and exits 0. `--fail-on-empty` (config key `failOnEmpty`) turns that into an error.

### Examples

```bash
# Scan a directory
jscpd /path/to/source

# Tune sensitivity and pick reporters
cpd /path/to/source --min-tokens 30 --min-lines 3 --reporters console,json,html

# Git blame with side-by-side author comparison
cpd /path/to/source --blame --reporters console-full

# List supported formats
cpd --list

# Use multiple reporters with custom output
cpd ./src -r console,json,sarif -o ./reports

# Skip clones within the same directory
cpd --skip-local /path/to/source

# Monorepo: don't compare team-owned packages with each other
cpd . --skip-isolated "packages/team-a|packages/team-b"
```

### Config File

Options can also come from a `.jscpd.json` config file (camelCase keys; existing v4 config files work unchanged):

```json
{
  "path": ["./src"],
  "reporters": ["console", "json"],
  "minLines": 5,
  "minTokens": 50,
  "threshold": 0,
  "format": ["javascript", "typescript"],
  "ignore": ["**/node_modules/**"],
  "ignorePattern": ["generated by .*"],
  "ignoreIdentifiers": false,
  "ignoreLiterals": false,
  "ignoreAnnotations": false,
  "maxGapLines": 0,
  "gitignore": true,
  "mode": "mild"
}
```

Isolation groups use the nested-array form in the config file: `"skipIsolated": [["packages/a", "packages/b"]]`.

Config discovery order: `--config <path>` -> `.jscpd.json` -> `.config/jscpd.json` (also `.config/.jscpd.json`) -> the `jscpd` key in `package.json`.

### Ignoring Source Regions

For a one-off region, place `jscpd:ignore-start` and `jscpd:ignore-end` in comments valid for the source language:

```javascript
// jscpd:ignore-start
const generatedLookup = {
  alpha: 1,
  beta: 2,
};
// jscpd:ignore-end
```

### How Detection Works (summary of stages)

1. **Format detection** — file extension (or name like `Makefile`) selects one of 224 formats, which selects the tokenizer.
2. **Tokenization** — each format's own comment/string rules apply; JS/TS/JSX/TSX use the oxc parser; Vue/Svelte/Astro are split into embedded-language blocks; Markdown fences tokenize as their fenced language; Razor separates C# from HTML.
3. **What counts** — `--mode mild` (default) drops whitespace tokens, `--mode weak` also drops comments, `--mode strict` keeps every token.
4. **Normalization (opt-in)** — `--ignore-identifiers`, `--ignore-literals`, `--ignore-annotations`.
5. **Matching** — rolling Rabin-Karp hash over the token stream finds repeated windows of at least `--min-tokens` tokens and `--min-lines` lines.
6. **Near-miss passes (opt-in)** — `--max-gap-lines` and `--similarity`.

What jscpd does not do is semantic analysis: two functions that compute the same result with different code (Type-4 clones) are out of scope, as they are for every token-based detector.

## License

MIT (c) Andrey Kucherenko
