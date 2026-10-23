# Webapp Capture

**Designed and built by [Legion Code Inc.](https://www.legioncodeinc.com)** Version 2.0.0. Licensed under AGPL-3.0-or-later.

Capture any running web app the way its users see it, then turn that capture into something people and AI agents can build on.

## Start here

New to AI tools? Follow the beginner guides in order. Each one says what to type, what you will see, and what to do if it goes wrong.

1. [Install everything](docs/01-install-everything.md)
2. [Your first demo video](docs/02-your-first-demo-video.md)
3. [Screenshots, library and audit](docs/03-screenshots-library-audit.md)
4. [Finish your video in ChatGPT](docs/04-finish-in-chatgpt.md)
5. [Make money with it](docs/05-make-money.md)
6. [Fix problems](docs/06-fix-problems.md)

Also: the [guide index](docs/README.md), the [usage reference](docs/USAGE-GUIDE.md), the [branded PDF of every guide](docs/webapp-capture-usage-guide.pdf), and the [repository README](../../README.md).

## Contents

- [Start here](#start-here)
- [Components](#components)
- [Usage](#usage)
- [Outputs](#outputs)
- [Safety model](#safety-model)
- [Replicate (only for AI-made intro clips)](#replicate-only-for-ai-made-intro-clips)
- [Troubleshooting](#troubleshooting)
- [Hive integration](#hive-integration)

## Components

| Component | Name when installed | Role |
| --- | --- | --- |
| Command | `/webapp-capture` (also `/webapp-capture:webapp-capture`) | Orchestrator instructions: intake, setup, login, dry run, route execution, watchdogs, verification, report, Ship Gate |
| Skill | `webapp-capture:webapp-capture-stinger` | Guides, references, prompts, research, and scripts |
| Agent | `webapp-capture:webapp-capture-worker-bee` | Runs script-heavy capture stages on the orchestrator's behalf |
| Skill | `webapp-capture:demo-intro-video` | Intro and B-roll for demos: free stock sources, Replicate model prompts, frame review, and `finish_video.py` |
| MCP server | `replicate_video` | Seven Replicate video model tools, a read-only production doctor, and model guides (ported from Character Action Studio). Needs Python 3.11+. A token is only needed to generate videos. |
| ChatGPT manifests | `plugin.json`, `mcp.json`, `.codex-plugin/plugin.json` | Let the ChatGPT desktop app load the same folder to finish demos |

## Usage

```text
/webapp-capture doctor
/webapp-capture screenshots http://localhost:3000
/webapp-capture demo http://localhost:3000 onboarding flow for new admins
/webapp-capture library https://staging.example.com
/webapp-capture audit http://localhost:3000
/webapp-capture shadcn http://localhost:3000
/webapp-capture all http://localhost:3000
/webapp-capture handoff
```

Claude asks for anything it cannot infer (environment, theme, output folder, sensitive regions), opens a browser window for you to log in, runs a small dry run and shows you the result, then runs the full route.

## Outputs

| Route | Default location | Contents |
| --- | --- | --- |
| screenshots | `library/design/screenshots/<route>/` | `<route>-001.png`, `<route>__<tab>-001.png`, `manifest.tsv` |
| demo | `library/design/demo/<title>/` (retakes in `<title>-take-N/`) | `demo.mp4`, `scenes/`, `screenshots/`, `failures/`, `timeline.json`, `segments.tsv`, `assembly.conf`, `writes-report.json`, `privacy-review.json`, `captions.vtt`, `titles.srt`, `narration/` (cues, fit report, Eleven v4 clip texts), `review/` (contact sheets, `REVIEW.md`), `script.md`, `plan.json`, `make-video.sh`; beside the folder: `<title>.ledger.json` and `findings.md` |
| library | `library/design/` | `components/<name>/` (component.md, code.html, styles.json, assets.json, screenshots), `ledger.json`, `tokens-raw.json`, `candidate.tokens.json`, `assets/` |
| audit | `library/requirements/reports/` | dated visual audit, code audit, and a combined inconsistency report |
| shadcn | `library/design/shadcn/` | `SHADCN-MAP.md`, `shadcn-map.json`, `globals.css` |
| Claude Design handoff | `library/design/<app>-claude-design-handoff-<date>.zip` | Library, tokens, audits, pages, shadcn map, `CLAUDE-DESIGN-INSTRUCTIONS.md` |

## Safety model

Read-only crawling by default, explicitly approved local or seeded onboarding, demo writes that are declared, approved one by one, verified, and recorded in a retake ledger, a masked privacy scan with per-scene contact sheets, human-only login, off-origin navigation blocking, theme guard, text redaction, screenshot masks, destructive-target and secret-field guards, and a Ship Gate before any commit. Details: `skills/webapp-capture-stinger/guides/00-foundation.md`.

## Replicate (only for AI-made intro clips)

### What is Replicate?

[Replicate](https://replicate.com) is a website that runs AI models for you in the cloud. Video models like Google Veo, Kling and Wan need huge, expensive computers. Replicate owns those computers and rents you a few seconds of time on them. This plugin talks to Replicate for you, so you never have to use its website to make a clip.

**Do I need it?** Only if you want an AI-made intro clip. Free stock B-roll does not need Replicate. Everything else in this plugin works without it.

**What does it cost?** You pay only for what you use ([billing](https://replicate.com/docs/topics/billing)). Each model shows its price on its page on replicate.com, and video models cost much more than image models, so check the price before you render. A few models can be tried for free, but after a bit Replicate asks you to set up billing (a card, or prepaid credit). If a run fails, you are not charged. If you cancel a run partway, you may still be charged for the time it ran. The plugin always asks before any paid render.

### Get your Replicate token (about 3 minutes)

A token is a long password that lets this plugin use your Replicate account. It starts with `r8_`. Treat it like a bank card number.

1. Go to [replicate.com](https://replicate.com) and sign up (or sign in).
2. Set up billing on the [billing page](https://replicate.com/account/billing) (a card, or prepaid credit). Video models will not run without it.
3. Open [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens). Replicate makes a default token when you sign up. You can use it, or click to create a new one named `webapp-capture` so you can turn it off later without breaking anything else.
4. Copy the token.
5. Save it in **one** of these places. Never paste it into a chat with Claude or ChatGPT.
   - **Claude desktop app (or Claude Code):** open the **Terminal** panel (title bar, or Ctrl and backtick), run `claude plugin configure webapp-capture@legioncodeinc`, and paste the token into the private field. Claude keeps it in your computer's secure credential store. Start a new session.
   - **ChatGPT:** open your computer's Terminal app (or the Claude app's Terminal panel), go to this plugin's folder, and run `python3 mcp/replicate-video/scripts/set_token.py --check`. Paste the token when it asks. The typing is hidden. The `--check` part makes one free, read-only call to confirm the token works. It saves the token to `~/.config/webapp-capture/replicate.env`, a file only you can read. Restart the app. Not sure where the plugin folder is? Ask Claude or ChatGPT: "Where is the webapp-capture plugin folder on this computer?"
   - **Advanced:** set `REPLICATE_API_TOKEN` in the environment that starts the app. It wins over the saved file.
6. Check it: ask Claude or ChatGPT to "check the Replicate video connection without generating anything." This runs the production doctor. It says whether a token is there but never shows it.

**Lost it or leaked it?** Delete that token on [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens), make a new one, and save it again. To remove it from this computer, run `python3 mcp/replicate-video/scripts/set_token.py --remove`.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `doctor` reports no Chromium | `npx playwright install chromium` in `skills/webapp-capture-stinger/scripts/` |
| Every route errors with `session expired` | Rerun the login step; the app's session timed out or uses session-only cookies |
| `theme check failed` | A tab click switched the theme: add that route to `tabs.noTabsOnRoutes` |
| Screenshots show empty states | Capture a seeded or real account; empty accounts render empty states |
| Shards killed or slow | Lower `browser.shards`; each headless browser needs roughly 1 GB of memory |
| A describe batch missing | `prepare-describe.mjs --pending` lists only the batches to rerun |
| Demo rerun refused: writes would repeat | Reset the data or pick new free slots, then rerun `record-demo.mjs --retake` |
| A demo write shows `mismatch` | Read `writes-report.json` and `findings.md`; fix the plan or data and retake |
| `narration/fit.md` reports OVERRUN | Shorten the line or lengthen the segment, then run `demo/build-cues.mjs` |
| A demo hangs on a live page | Add `waitFor` actions; the recorder never waits for network idle |
| Outputs nested as `library/design/library/design` | Output paths are relative to the config file; use the path `doctor` suggests |

Set `WEBAPP_CAPTURE_DEBUG=1` to print stack traces from any script.

## Hive integration

When The Hive's skills are installed (`beekeeper-suit`, `security-stinger`, `quality-stinger`, `github-repo-health-stinger`, `design-system-stinger`, `impeccable-stinger`), the command routes through them and hands work off to them. Without them, the plugin runs self-contained and performs equivalent review passes itself.

---

© 2026 Legion Code Inc. · [legioncodeinc.com](https://www.legioncodeinc.com)
