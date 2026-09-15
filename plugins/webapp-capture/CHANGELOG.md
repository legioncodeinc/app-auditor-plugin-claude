# Changelog

All notable changes to the Webapp Capture plugin are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

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
