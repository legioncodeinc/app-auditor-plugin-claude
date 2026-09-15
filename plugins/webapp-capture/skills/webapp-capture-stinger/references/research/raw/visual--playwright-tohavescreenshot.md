# Visual comparisons | Playwright (toHaveScreenshot)
- URL: https://playwright.dev/docs/test-snapshots ; option reference: https://playwright.dev/docs/api/class-locatorassertions ; https://playwright.dev/docs/api/class-snapshotassertions
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (versioned docs site, current as of Playwright's latest release referenced 2026)

## Core functionality

Playwright Test's `toHaveScreenshot()` enables visual regression testing by comparing screenshots against reference baselines. On the initial run it generates the golden/reference image; subsequent runs validate new screenshots against that stored reference. Playwright uses the `pixelmatch` library internally for pixel comparison.

## Threshold semantics (options for toHaveScreenshot / toMatchSnapshot)

**threshold**: "An acceptable perceived color difference in the YIQ color space between the same pixel in compared images, between zero (strict) and one (lax)." Default is `0.2`. This maps to pixelmatch's own per-pixel `threshold` option — it controls how different two individual pixels must be before they're counted as "different," not how many differing pixels are tolerated overall.

**maxDiffPixels**: "An acceptable amount of pixels that could be different." Default is unset (no limit beyond internal defaults). This is an absolute pixel count.

**maxDiffPixelRatio**: "An acceptable ratio of pixels that are different to the total amount of pixels, between 0 and 1." Default is unset. Because it's relative to image size, it's more likely to yield consistent results across a wide range of image sizes, whereas `maxDiffPixels` is a constant value that gives finer control on individual tests.

Both `maxDiffPixels` and `maxDiffPixelRatio` are configurable globally via `TestConfig.expect` or per-assertion call.

Example:
```ts
await expect(page).toHaveScreenshot('screenshot.png', {
  maxDiffPixelRatio: 0.01, // allow 1% pixel difference
  threshold: 0.2,
});
```

## Other relevant options

- **animations**: `"disabled"` (default) or `"allow"`. When disabled, finite CSS animations are fast-forwarded to completion and infinite animations are canceled to their initial state before the screenshot, preventing animation-timing flakiness.
- **caret**: `"hide"` (default) or `"initial"` — controls whether the text cursor is hidden during capture.
- **mask**: locators to mask (overlaid with a pink box `#FF00FF`) — used to blot out dynamic content (timestamps, ads, etc.) that would otherwise cause spurious diffs.
- **scale**: `"css"` (default, one pixel per CSS pixel) or `"device"` (one pixel per device pixel) — affects screenshot pixel density on high-DPI screens.
- **stylePath**: path to a stylesheet applied at capture time, for hiding dynamic elements or normalizing properties for consistency.

## Updating baselines

```
npx playwright test --update-snapshots
```
Use this after an intentional UI change to regenerate the reference/golden images.

## Non-image snapshots

`toMatchSnapshot()` compares text or binary data (not just images), auto-detecting content type for the appropriate comparison algorithm.

## Flakiness guidance

The docs state directly: "Browser rendering can vary based on the host OS, version, settings, hardware, power source (battery vs. power adapter), headless mode, and other factors. For consistent screenshots, run tests in the same environment where the baseline screenshots were generated." Recommended practices to reduce flakiness:
- Generate and compare screenshots in the same environment (e.g., same Docker image / CI runner) as where baselines were created — cross-OS/cross-hardware rendering differences are a primary flake source.
- Disable animations (`animations: "disabled"`) so in-flight CSS transitions don't cause nondeterministic pixel diffs.
- Mask or hide inherently dynamic regions (timestamps, live data, ads) rather than trying to tune thresholds around them.
- Wait for fonts/images to load before capturing to avoid FOUC-driven diffs.
- Use `maxDiffPixelRatio`/`maxDiffPixels` to absorb minor sub-pixel rendering noise rather than relying solely on a very lax per-pixel `threshold`.

## Notes for webapp-capture-stinger

- `threshold` (per-pixel, YIQ color-space based) and `maxDiffPixelRatio`/`maxDiffPixels` (aggregate) are orthogonal knobs: the former decides whether an individual pixel counts as "different" at all (fed to pixelmatch), the latter decides how many/what proportion of such different pixels is tolerated before the whole comparison fails.
- Since Playwright's screenshot diffing is pixelmatch under the hood, the semantics documented in pixelmatch's own README (threshold 0–1, includeAA, diffColor) directly explain what Playwright's `threshold` option is tuning.
