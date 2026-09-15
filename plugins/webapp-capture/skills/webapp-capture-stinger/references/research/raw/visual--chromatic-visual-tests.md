# Visual tests | Chromatic docs
- URL: https://docs.chromatic.com/docs/visual/ (also https://www.chromatic.com/docs/visual/)
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## What Visual Tests are

"Visual Tests are a powerful tool for catching visual regressions and ensuring your app functions as expected." They work by capturing snapshots of every test within a cloud browser environment. Whenever code is pushed, Chromatic compares the new snapshots to baseline versions to identify visual changes.

## How it works

Described as "before-and-after" snapshots of the app's interface:
1. Capture a "perfect" before image — this becomes the baseline.
2. After code changes, capture an "after" snapshot.
3. Compare the after snapshot pixel-by-pixel against the baseline, revealing any visual differences.

## Snapshot capture in cloud browsers

"Chromatic renders your UI components in a cloud-based browser" and "takes a snapshot for each test, with all tests running simultaneously to save you time."

## Visual difference detection

Pixel-by-pixel comparison methodology. When code changes occur, "Chromatic generates new snapshots and compares them to the baselines" through automated diffing that surfaces any visual variation between current state and the established baseline.

## Review and verification workflow

On detecting changes, users are prompted to evaluate whether modifications are intentional. The system notifies teams of unexpected changes "so they can fix them quickly." Users approve intentional visual changes (promoting them to the new baseline) or address unintended regressions found in the comparison.

## CI integration

Visual tests run both locally via the Storybook addon interface and within CI pipelines — "can also run these tests in CI," enabling automated visual validation as part of the development workflow.

## TurboSnap and other features

TurboSnap (only re-snapshotting stories affected by a given code change, to save CI time/cost) and flake-reduction tooling are referenced in the docs navigation but not elaborated in the fetched excerpt; consult the dedicated TurboSnap docs page for details when implementing.

## Notes for webapp-capture-stinger

Chromatic is Storybook-centric: it snapshots individual component stories rather than full pages by default, which differs from Argos/Percy/Playwright's page-level or element-level screenshot model. Relevant if webapp-capture-stinger needs to inventory components in isolation vs. full-page flows.
