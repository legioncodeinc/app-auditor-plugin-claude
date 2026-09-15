# Integrate Percy with Playwright and Javascript | BrowserStack Docs
- URL: https://www.browserstack.com/docs/percy/playwright/getting-started/nodejs/integrate-your-tests
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Setup overview

Integrating Percy with Playwright (Node.js) requires: creating a Percy project, setting environment variables, installing dependencies, and updating test scripts.

## Installation steps

1. Create a Percy project (sign in to Percy, create a Web project). Percy generates a project token.
2. Set the token as an environment variable:
   ```bash
   export PERCY_TOKEN="<your token here>"
   ```
3. Install the SDK:
   ```bash
   npm install @percy/playwright
   ```

## percySnapshot API

```javascript
const percySnapshot = require('@percy/playwright');
await percySnapshot(page, 'Example Site');
```

Signature: `percySnapshot(page, name, options?)`
- `page` (required) — a Playwright page instance.
- `name` (required) — unique identifier for the snapshot.
- `options` (optional) — configuration settings for the individual snapshot.

## Running tests

```bash
npx percy exec -- <command to run the test script file>
```
This wraps test execution and automatically uploads captured snapshots to Percy for comparison.

## How Percy detects visual diffs

When `percySnapshot()` runs, Percy does not screenshot the live browser directly. Instead, it serializes the page: the full DOM, all CSS, and every asset (images, fonts, stylesheets) needed to reconstruct that exact page state. Percy then re-renders that serialized DOM across its own set of browsers/widths in the cloud and diffs the resulting renders against baseline snapshots, displaying side-by-side comparisons.

## Review workflow

After a build runs, the Percy project dashboard displays snapshot comparisons for that build, allowing reviewers to approve or reject visual changes before merging. Approved changes become the new baseline for future comparisons.

## Notes for webapp-capture-stinger

Percy's DOM-serialization approach (rather than a literal screenshot of the rendered browser) is a materially different capture strategy from pixelmatch/Playwright/BackstopJS/Argos, which diff actual rendered pixel screenshots. This matters for headless-capture design: Percy needs all assets reachable/inlined for accurate re-render, and won't capture things that only exist as rendered pixels without a DOM/CSS representation (e.g. certain canvas/WebGL content) as faithfully as a pixel-screenshot approach would.
