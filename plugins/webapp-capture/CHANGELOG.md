# Changelog

All notable changes to the Webapp Capture plugin are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.0.0] - 2026-10-23

### Added

- Demo actions for real app flows: `select` by option label, `check` and `uncheck`, pointer `drag` between selectors or points with stepped moves, native `dragTo`, `scrollElement` for calendar grids and other scroll containers (`x`, `y`, or `intoView`), `waitFor` a selector or text, and `confirmDialog`, which clicks the named button only when the dialog text matches `expect` and otherwise cancels.
- Read-only per-scene `verify` checks (visible, hidden, text, count).
- A write ledger: scenes that can change data are declared in `writes[]` with a description and an expected effect, and each needs user approval. `writes-report.json` compares the expected effect with the actual checks, and later write scenes are skipped after a mismatch or failure.
- Retakes: `<output.demo>/<slug>.ledger.json` remembers attempted writes. A rerun that would repeat them is refused and lists them; `--retake` (or `RETAKE=1`) records into `<slug>-take-N`.
- `findings.md` with a failure screenshot for every failed or mismatched scene.
- A DOM cursor overlay for headless video (`video.cursor`), cursor parking after clicks and drags (`video.parkAt`), and cursor restore after navigation.
- `timeline.json`, an editable `segments.tsv` (reorder, trim, delete, or splice clips from `clips/`), `assembly.conf` with an end frame hold (`video.endHoldMs`, default 1500), and scene titles in `titles.srt`.
- Narration fit report (`narration/fit.md`) at the plan pace, and Eleven v4 clip texts: one file per cue, bracketed audio tags kept, SSML breaks converted with a warning, domains spelled out, and a manifest without a hardcoded model id.
- `demo/build-cues.mjs` to rebuild captions, titles, and narration after editing segments, and `demo/review-demo.mjs` for per-scene contact sheets and a masked text-hit review.
- Unit tests for demo plans, narration, nested output paths, and `make-video.sh`, plus a real Chromium test of the new actions and verify checks.
- Finish demos in ChatGPT: `/webapp-capture handoff` runs `demo/chatgpt-handoff.mjs`, which packages a reviewed demo with `CHATGPT-INSTRUCTIONS.md`, an intro brief and `finish_video.py`. The script places one ElevenLabs clip per caption line at its cue time, puts an intro in front, shifts captions, and writes `finished/demo-final.mp4`.
- `demo-intro-video` skill: intro and B-roll from free stock sites (licenses and APIs checked 2026-10-23) or seven Replicate video models, with prompt patterns and frame review.
- Bundled `replicate_video` MCP server, ported from Character Action Studio 1.0.0 (Legion Code Inc., AGPL-3.0-or-later) with its schemas, model guides, production doctor, frame review script and tests. ChatGPT desktop manifests (`plugin.json`, `mcp.json`, `.codex-plugin/plugin.json`) load the same folder.
- Easier Replicate token setup: an optional sensitive `userConfig` field in Claude Code (`claude plugin configure webapp-capture@legioncodeinc`, or `/plugin` then Installed then Configure options), and `set_token.py`, which saves the token with hidden typing to an owner-only file outside every project that the MCP launcher reads when the environment variable is unset.
- README sections: common prompts, finishing in ChatGPT, what runs in parallel, free B-roll sites, and pricing and selling on Upwork and Fiverr (sources checked 2026-10-23).
- The beginner path uses the Claude desktop app's Code tab: Claude installs the free tools after a permission prompt, and the app's Terminal panel is used once to add the plugin marketplace. Terminal use is an optional alternative.
- Six numbered beginner guides in `docs/` (install, first demo video, screenshots and audits, finishing in ChatGPT, making money, fixing problems), each with next and previous links and step checks, plus a guide index, tables of contents in both READMEs, and a ChatGPT local marketplace file (`.agents/plugins/marketplace.json`). The branded PDF now holds all six guides and a reference appendix, with a clickable contents page and PDF bookmarks.
- `docs/USAGE-GUIDE.md`, a usage guide with Mermaid diagrams covering what the plugin installs, a first run, every route, and the demo safety model, plus a Legion Code Inc. branded PDF of it built by `tools/build-guide-pdf.mjs`.

### Changed

- `record-demo.mjs` never waits for network idle (realtime pages never go idle) and relies on `waitFor` instead.
- `make-video.sh` is a static template that assembles from `segments.tsv`, preflights every output, and refuses linked inputs or existing outputs.
- `routes.discover` defaults to `nav-links` starting from `routes.startPath`, and the intake asks for the real post-login landing page.
- `doctor.mjs` warns when an output path repeats the config folder (for example `library/design/library/design`) and suggests the relative path, and notes that the earliest cookie expiry may be renewed by a refresh token.

- The default cut in `segments.tsv` is anchored on the clip length measured with `ffprobe`: it starts when navigation began, dropping the blank page Playwright records first, and ends at the true end of the clip instead of losing the last moments of each scene.
- The demo guard judges drag ends and dropdowns on their own name, so containers are no longer refused for the text of what they hold.
- `playwright-core` and `playwright` require 1.63 or newer, matching the lockfile and the `recordVideo.showActions` option the recorder uses.
- Chromium tests skip with a clear message when no Chromium build is installed.

### Security

- Demo outputs (ledger, `findings.md`, reports, cue files, review sheets) are written owner-only with `O_NOFOLLOW` and a link-count check, so a symlink or hard link planted in the output folder is refused.
- The demo guard resolves the real control text from the DOM before every pointer action; the built-in deny list always applies, and credential fields and secret-looking values are always refused.
- Each scene's visible text is scanned for emails, phone numbers, and `redact.patterns`; only masked hits are stored.

## [1.1.0] - 2026-09-22

### Added

- Recursive `crawl-links` route discovery with route caps, pathname filtering, and route-family tab exclusions.
- Explicitly approved local or seeded onboarding plans that run once before screenshot or inventory shards and capture evidence before each step.
- Ordered screenshot-manifest merging so successful retry runs supersede earlier errors or truncations.
- Optional project context files and onboarding screenshots in Claude Design handoffs.

### Changed

- Tab capture reloads the base route and resolves the current tab before each click, preventing state from leaking between captures.
- Scroll-container selection favors substantial overflow regions and ignores short nested controls.
- Token exports report the configured capture theme instead of assuming dark mode.
- Sharp is updated to 0.35.4 and the documented Node.js minimum is aligned to 20.9.

### Security

- Onboarding validates every action before navigation, retains the built-in destructive-click denylist when custom rules are added, rejects secret-looking live fields, and confines onboarding evidence to the screenshots directory.

## [1.0.0] - 2026-09-15

### Added

- `/webapp-capture` command: orchestrator instructions for demo, screenshots, library, audit, all, and doctor routes, with intake, dry run, watchdogs, verification, reporting, and a Ship Gate.
- `webapp-capture-stinger` skill: foundation, demo, component library, and inconsistency audit guides; reference tables; describe, merge, and reconcile prompt templates; an 83-source research archive with a cited distillation.
- `webapp-capture-worker-bee` agent for delegated capture runs.
- Scripts: `doctor`, `save-session` (human login, sessionStorage sidecar), `parallel` (memory-capped sharding), `screenshots`, inventory (`extract`, `cluster`, `tokens`, `tokens-dtcg`, `sheets`, `prepare-describe`, `prepare-merge`, `validate-merge`, `build`), `demo/record-demo` with ffmpeg assembly, and `audit` (visual and code).
- Safety: read-only crawling, off-origin navigation blocking, theme guard, text redaction seeded from GitHub secret scanning patterns and the OWASP never-log list, screenshot masks, demo plan approval gate, destructive-target and secret-field guards.
- Candidate design tokens in the DTCG Format Module 2025.10 shape.
- Claude Design handoff: `inventory/design-handoff.mjs` packages the library, tokens, audits, page screenshots, and the shadcn/ui map with a filled `CLAUDE-DESIGN-INSTRUCTIONS.md` brief into one zip (lossless WebP images), delivered at the end of every library-based route.
- shadcn/ui map route: `inventory/shadcn-prepare.mjs`, mapping and theme prompts, a shadcn/ui catalog, and `inventory/shadcn-build.mjs`, which validates every mapping and writes `SHADCN-MAP.md`, `shadcn-map.json`, and an OKLCH `globals.css` theme draft.

### Security

- Session files are written owner-only, checked for gitignore coverage by `save-session` and `doctor`, and never read by the agent.

Designed and built by Legion Code Inc.
