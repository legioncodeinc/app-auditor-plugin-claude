# Playwright | Argos Docs
- URL: https://argos-ci.com/docs/reference/playwright.md (also https://argos-ci.com/docs/playwright)
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Integration overview

Argos CI enhances Playwright testing by combining visual testing with debugging features. It manages screenshots in CI rather than locally — "There's no need to run tests locally or commit screenshots to your repository," keeping the repository focused on code rather than binary assets. A dashboard helps developers "spot discrepancies and understand visual changes without the need for cumbersome manual checks."

Argos also stabilizes fonts, images, animations, and loaders "to ensure stability and consistency in the screenshots captured."

## Setup

Add the Argos reporter to the Playwright config:

```ts
reporter: [
  ["@argos-ci/playwright/reporter",
   createArgosReporterOptions({ uploadToArgos: !!process.env.CI })
  ]
]
```

Stabilize text rendering across machines/CI with launch options:
```ts
use: {
  launchOptions: {
    args: ["--disable-lcd-text", "--font-render-hinting=none"]
  }
}
```
This ensures "glyphs render identically on your machine and on CI."

## Screenshot capture

```ts
await argosScreenshot(page, "homepage");
```

## Configuration options

- **threshold** — sensitivity setting, 0–1 scale; higher values reduce diff sensitivity; default 0.5.
- **fullPage** — defaults to `true`, captures the complete page.
- **element** — target specific elements via locators/selectors.
- **viewports** — define multiple viewport dimensions for responsive testing.
- **ariaSnapshot** — capture accessibility snapshots alongside screenshots.

## Stabilization options

Automatically handles UI stabilization by:
- Pausing animated GIFs on their first frame.
- Loading images with `srcset` attributes.
- Waiting for fonts and images to load.
- Hiding scrollbars, text carets, and spell-check indicators.
- Stabilizing sticky/fixed elements.

Customizable/disable-able via the `stabilize` option.

## Debugging capabilities

Test failures automatically capture:
- Failure screenshots, viewable in the Argos UI.
- Playwright traces, enabling "time travel" debugging through test steps.
- Test metadata (annotations, tags).

Enabled via:
```ts
use: {
  trace: "on-first-retry",
  screenshot: "only-on-failure"
}
```

## Visual difference detection

Argos uses a threshold-based comparison system. The `threshold` parameter (0–1) controls sensitivity: higher values require larger visual differences to trigger a flagged diff; lower values catch subtler changes.

## Advanced features

- Dynamic build names — generate multiple builds from one test suite.
- Helper attributes — `data-visual-test` (transparent / removed / blackout) to hide dynamic content from diffing.
- Responsive testing across multiple viewports automatically.
- CSP compatibility — bypass or whitelist Content-Security-Policy restrictions for script injection needed by the capture tooling.

## Review workflow

Developers access results through the Argos dashboard, where they compare screenshots side-by-side, review traces, and approve or reject visual changes before merging.
