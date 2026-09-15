# BackstopJS README
- URL: https://github.com/garris/BackstopJS (README fetched via https://raw.githubusercontent.com/garris/BackstopJS/master/README.md)
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): unknown

## Description

BackstopJS "automates visual regression testing of your webapp – comparing screenshots over time" to catch unintended UI changes.

## How visual differences are detected

BackstopJS uses Resemble.js for pixel-level comparison analysis, configurable with sensitivity settings. The `misMatchThreshold` property specifies what percentage of differing pixels will be tolerated before a test is marked failed (default: 0.1%). The comparison process generates visual diff overlays showing exactly where changes occurred, with options to adjust error color, transparency, and antialiasing detection in the output.

## Configuration structure

### Scenarios
- `label` (required) — used for screenshot naming/identification.
- `url` (required) — the endpoint/document under test.
- `referenceUrl` (optional) — an alternate environment to generate the reference from.
- `readySelector`, `readyEvent`, `delay` — synchronization before capture.
- `clickSelector`, `hoverSelector` — simulate user interaction before capture.
- `hideSelectors`, `removeSelectors` — handle dynamic content that would otherwise cause false diffs.
- `onBeforeScript`, `onReadyScript` — custom script execution hooks.

### Viewports
Array of `{label, width, height}` objects defining device breakpoints to test against.

### misMatchThreshold
Percentage (0.00%–100.00%) of acceptable pixel variance before test failure. Default 0.1%; tune per test requirements.

## Rendering engines

- **Puppeteer** (default) — Chrome Headless rendering, installed globally, suitable for most Chrome-based scenarios.
- **Playwright** — cross-browser support (Chromium, Firefox, WebKit). Requires switching `onBefore`/`onReady` scripts to Playwright defaults. Supports `storageState` for authentication (cookies/localStorage).

Both engines accept `engineOptions` for flags (`--no-sandbox`, headless mode, browser-specific params).

## Report/review UI workflow

### Interactive browser report
Generates an in-browser reporting interface with:
- Layout settings for print/screen viewing.
- Scenario filtering and display options.
- Reference / test / visual-diff comparison views.
- Interactive scrubber tool for side-by-side inspection.
- Approval mechanism for accepting results.

### Approve/reject workflow
`backstop approve` promotes passing test screenshots to reference status for future comparisons. Filtering via regex patterns on scenario filenames allows selective approval. A remote HTTP service enables interactive approval directly from the web report.

## CLI commands

- `backstop init` — scaffold a new project (config, URLs, viewports, interactions).
- `backstop reference` — generate reference screenshots without comparison (e.g. from an alternate environment, or to refresh all baselines).
- `backstop test` — capture new screenshots and compare against references; supports `--filter` (run specific scenarios) and `--docker` (containerized rendering for consistency).
- `backstop approve` — promote recent test results to reference status; supports `--filter`.
- `backstop openReport` — open the latest report in the browser without re-running tests.

## CI/CD integration

- Exit codes: 0 for success, 1 for failures — enables conditional CI branching.
- JUnit reporting: `"report": ["CI"]` generates XML reports for Jenkins/Travis-style integration; suite name customizable via `ci.testSuiteName`.
- `--docker` flag for consistent rendering across environments.
- Recommended `.gitignore` entries for test bitmaps while preserving reference files under version control.
