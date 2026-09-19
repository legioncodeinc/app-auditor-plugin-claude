<!-- ───────────────────────────────  HERO  ─────────────────────────────── -->

<h1 align="center">Audit My App with Claude</h1>

<p align="center">
  <strong>Your app already contains a design system. Make it visible.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/plugin-webapp--capture%201.0.0-F7A823?style=flat-square" alt="webapp-capture 1.0.0">
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Cowork%20%7C%20claude.ai-6E6A62?style=flat-square" alt="Works with Claude Code, Cowork, claude.ai">
  <a href="LICENSE.md"><img src="https://img.shields.io/github/license/legioncodeinc/app-auditor-plugin-claude?style=flat-square" alt="AGPL-3.0-or-later license"></a>
</p>

<p align="center">
  <a href="https://github.com/legioncodeinc">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/brand/legion-logo-dark.svg">
      <img src="assets/brand/legion-logo-light.svg" alt="Legion Code" height="34">
    </picture>
  </a>
</p>

<p align="center"><em>Designed and built by <a href="https://github.com/legioncodeinc">Legion Code Inc.</a></em></p>

<p align="center">
  <img src="assets/media/audit-my-app.jpg" alt="Audit My App with Claude illustrated app-auditing workspace">
</p>

---

Audit My App with Claude turns a running web application into a documented component library, measured design tokens, organized screenshots, demo videos, and actionable UI inconsistency findings.

Inspect what users actually see. Find mismatched colors, inconsistent spacing, and components that behave like they were built by five different teams. Package the results for Claude Design or map them to shadcn/ui.

Designed and built by Legion Code Inc.

**I am Legion. We are Legion.**

## Quick start

```bash
claude plugin marketplace add legioncodeinc/app-auditor-plugin-claude
claude plugin install webapp-capture@legioncodeinc
```

Then start Claude Code in a project where your app is running:

```text
/webapp-capture doctor
/webapp-capture all http://localhost:3000
```

The first command reports missing local requirements and their fixes. The second opens intake and dry-run steps before capturing the full app.

## What you get

Type `/webapp-capture` in Claude Code, answer a few questions, log in once in a browser window, and Claude does the rest.

| Route | Command | You get |
| --- | --- | --- |
| **Demo** | `/webapp-capture demo http://localhost:3000` | A 1080p MP4 walkthrough with captions, sharp key screenshots, a narration script paced for voiceover, and an ffmpeg script to re-cut it |
| **Screenshots** | `/webapp-capture screenshots http://localhost:3000` | Every page and every real tab, scrolled top to bottom, named by route: `dashboard-billing-001.png`, `dashboard-billing__invoices-001.png` |
| **Component library** | `/webapp-capture library http://localhost:3000` | One folder per unique component: purpose, anatomy, variants, measured styles, markup, screenshots, icons. Plus a ledger and candidate design tokens in the DTCG 2025.10 format, ready for a design-system AI |
| **Claude Design handoff** | runs automatically at the end of `library`, `audit`, `shadcn`, and `all` | One zip with the component library, tokens, audit findings, page screenshots, and `CLAUDE-DESIGN-INSTRUCTIONS.md`. Upload it to Claude Design and say "Read CLAUDE-DESIGN-INSTRUCTIONS.md and follow it" to get a brand token guide and design system |
| **shadcn/ui map** | `/webapp-capture shadcn http://localhost:3000` | Every captured component mapped to shadcn/ui components, variants, and subcomponents, the new variants and custom tokens you need, the exact `npx shadcn@latest add` command, and a `globals.css` theme in OKLCH that makes shadcn/ui look like your app |
| **Inconsistency audit** | `/webapp-capture audit http://localhost:3000` | Near-identical colors that should be one token, sprawling type and spacing scales, components rendered five different ways, and the hardcoded values in your code that cause it |
| **Everything** | `/webapp-capture all http://localhost:3000` | All of the above, in order |
| **Check setup** | `/webapp-capture doctor` | What is missing on this machine and the exact fix for each item |

The package is built from measured values, never guesses. It reads the rendered page, not your source, so it works with React, Svelte, Vue, Next.js, Rails, plain HTML: anything that runs in a browser.

## Proven on a real app

The first production run captured an 87-route AI gateway dashboard: 107 page states, 25,698 elements, grouped into 948 visual groups and merged into **252 documented components**, with 255 icon glyphs, candidate tokens, and a 74-finding visual audit. Findings included seven near-identical white overlays used 1,678 times, eight different fills for "primary" buttons, and three incompatible treatments for destructive actions.

## Installation

The [quick start](#quick-start) is the recommended Claude Code installation path. The equivalent interactive commands are `/plugin marketplace add legioncodeinc/app-auditor-plugin-claude` and `/plugin install webapp-capture@legioncodeinc`.

### Plugin distribution for Claude Cowork

Download `dist/webapp-capture-plugin-1.0.0.zip` from this repository and upload it as a plugin. Use the `/webapp-capture` command from the plugin's commands.

### Skill-only distribution for claude.ai

Download `dist/webapp-capture-stinger-1.0.0.skill` and upload it under Settings, Capabilities, Skills. The skill carries the full procedure; script-based capture needs an environment that can run Node and a browser.

Verify downloads against `dist/SHA256SUMS`.

## Requirements

| Need | Why | Install |
| --- | --- | --- |
| Node 20 or newer | Runs the capture scripts | [nodejs.org](https://nodejs.org) |
| Chromium for Playwright | Headless browser | Claude runs `npx playwright install chromium` for you when missing |
| ffmpeg | Demo video assembly only | `brew install ffmpeg`, `apt install ffmpeg`, or `winget install ffmpeg` |
| A running copy of your app | The thing being captured | Local, staging, or a seeded demo account is best |

The plugin's script dependencies (Playwright core and sharp) install on first use.

## How it stays safe

- **You log in, Claude never does.** A real browser window opens; you sign in (MFA and SSO work). Claude never sees, types, or stores your password. The saved session is owner-only and checked for gitignore coverage.
- **Read-only by design.** Capture navigates pages, scrolls, and switches tabs. It never submits forms, flips settings, or clicks delete, restart, or logout. Anything that looks like a setting picker is excluded after a dry run.
- **Stays on your app.** Navigation to any other origin is blocked; popups are closed.
- **Secrets stay out.** Captured text passes redaction patterns seeded from GitHub secret scanning and the OWASP logging guidance. Sensitive screen regions are painted over with solid masks.
- **Demos need your approval.** The recorder refuses to run a demo plan you have not approved, and refuses destructive-looking clicks or typing into secret fields.
- **Nothing ships silently.** Every run ends with a report and a security, quality, and repository hygiene gate before anything is committed.

## What's inside

```text
.claude-plugin/marketplace.json          marketplace catalog (legioncodeinc)
plugins/webapp-capture/
  .claude-plugin/plugin.json             plugin manifest
  commands/webapp-capture.md             /webapp-capture orchestrator instructions
  agents/webapp-capture-worker-bee.md    agent for delegated capture runs
  skills/webapp-capture-stinger/
    SKILL.md                             the skill
    guides/                              foundation, demo, library, audit, shadcn procedures
    references/                          field tables, shadcn catalog, prompt templates, research archive
    scripts/                             doctor, session, parallel runner, capture, inventory, handoff, shadcn, demo, audits
dist/                                    Cowork plugin zip, claude.ai skill file, checksums
tools/build-dist.sh                      rebuilds dist/
```

## Build from source

```bash
git clone https://github.com/legioncodeinc/app-auditor-plugin-claude.git
cd app-auditor-plugin-claude
claude plugin validate ./plugins/webapp-capture
tools/build-dist.sh
```

## Support

For installation help and reproducible bug reports, see [SUPPORT.md](SUPPORT.md). Feature requests and fixes are welcome through GitHub Issues and pull requests.

## Support development

If this plugin saves you time, help us keep building.

Sponsor Legion Code Inc. to support maintenance, documentation, compatibility updates, and new capabilities for our open-source developer tools.

I am Legion. We are Legion.

Verified sponsorship links will be added after the corresponding funding accounts are active.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, validation, generated-distribution rules, and pull-request expectations. Please read [SECURITY.md](SECURITY.md) before reporting a vulnerability.

## Credits

Webapp Capture was designed and built by **[Legion Code Inc.](https://www.legioncodeinc.com)**: the capture pipeline, the component grouping and merge method, the safety model, the orchestration, and the research behind it. It stands on [Playwright](https://playwright.dev), [sharp](https://sharp.pixelplumbing.com), [FFmpeg](https://ffmpeg.org), and the [Design Tokens Community Group](https://www.designtokens.org) format.

## License

Licensed under the **GNU Affero General Public License v3.0 or later** ([AGPL-3.0-or-later](LICENSE.md)). Use it commercially or privately, free of charge. Keep the copyright and license notices intact, and if you modify it, share your changes under the same license.

© 2026 Legion Code Inc.

<p align="center"><strong>I am Legion. We are Legion.</strong></p>

<p align="center">#vibewithlegion</p>
