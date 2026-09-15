# Visual comparisons (guide) + expect(page).toHaveScreenshot() API reference
- URL: https://playwright.dev/docs/test-snapshots and https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1
- Fetched: 2026-09-15
- Source type: official docs (guide + API reference, sourced from microsoft/playwright docs/src/test-snapshots-js.md and docs/src/api/class-pageassertions.md + params.md macros on the `main` branch)
- Last updated (if shown): unknown

## GUIDE: Visual comparisons

### Introduction

Playwright Test includes the ability to produce and visually compare screenshots using `await expect(page).toHaveScreenshot()`. On first execution, Playwright test will generate reference screenshots. Subsequent runs will compare against the reference.

```js title="example.spec.ts"
import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveScreenshot();
});
```

> **Warning**: Browser rendering can vary based on the host OS, version, settings, hardware, power source (battery vs. power adapter), headless mode, and other factors. For consistent screenshots, run tests in the same environment where the baseline screenshots were generated.

### Generating screenshots

When you run above for the first time, test runner will say:

```txt
Error: A snapshot doesn't exist at example.spec.ts-snapshots/example-test-1-chromium-darwin.png, writing actual.
```

That's because there was no golden file yet. This method took a bunch of screenshots until two consecutive screenshots matched, and saved the last screenshot to file system. It is now ready to be added to the repository.

The name of the folder with the golden expectations starts with the name of your test file:

```bash
drwxr-xr-x  5 user  group  160 Jun  4 11:46 .
drwxr-xr-x  6 user  group  192 Jun  4 11:45 ..
-rw-r--r--  1 user  group  231 Jun  4 11:16 example.spec.ts
drwxr-xr-x  3 user  group   96 Jun  4 11:46 example.spec.ts-snapshots
```

The snapshot name `example-test-1-chromium-darwin.png` consists of a few parts:

- `example-test-1.png` - an auto-generated name of the snapshot. Alternatively you can specify snapshot name as the first argument of the `toHaveScreenshot()` method:
    ```js
    await expect(page).toHaveScreenshot('landing.png');
    ```
- `chromium-darwin` - the browser name and the platform. Screenshots differ between browsers and platforms due to different rendering, fonts and more, so you will need different snapshots for them. If you use multiple projects in your configuration file, project name will be used instead of `chromium`.

The snapshot name and path can be configured with `TestConfig.snapshotPathTemplate` in the playwright config.

Snapshots are stored as PNG by default. Give the snapshot a name with the `.webp` extension to store it in the WebP format instead, it is also lossless:

```js
await expect(page).toHaveScreenshot('landing.webp');
```

> Note that `toHaveScreenshot()` also accepts an array of path segments to the snapshot file such as `expect().toHaveScreenshot(['relative', 'path', 'to', 'snapshot.png'])`. However, this path must stay within the snapshots directory for each test file (i.e. `a.spec.js-snapshots`), otherwise it will throw.

### Updating screenshots

Sometimes you need to update the reference screenshot, for example when the page has changed. Do this with the `--update-snapshots` flag.

```bash
npx playwright test --update-snapshots
```

### Hover effects

Screenshots capture any hover effects present in the page at the moment. To avoid hover effects, move the mouse to a position that does not trigger them, or hover an element that has no effects, before taking the screenshot:

```js
await page.mouse.move(-1, -1);
await expect(page).toHaveScreenshot();
```

### Options

#### maxDiffPixels

Playwright Test uses the pixelmatch library. You can pass various options to modify its behavior:

```js title="example.spec.ts"
import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveScreenshot({ maxDiffPixels: 100 });
});
```

If you'd like to share the default value among all the tests in the project, you can specify it in the playwright config, either globally or per project:

```js title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  expect: {
    toHaveScreenshot: { maxDiffPixels: 100 },
  },
});
```

#### stylePath

You can apply a custom stylesheet to your page while taking screenshot. This allows filtering out dynamic or volatile elements, hence improving the screenshot determinism.

```css title="screenshot.css"
iframe {
  visibility: hidden;
}
```

```js title="example.spec.ts"
import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveScreenshot({ stylePath: path.join(__dirname, 'screenshot.css') });
});
```

If you'd like to share the default value among all the tests in the project, you can specify it in the playwright config, either globally or per project:

```js title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      stylePath: './screenshot.css'
    },
  },
});
```

### Non-image snapshots

Apart from screenshots, you can use `expect(value).toMatchSnapshot(snapshotName)` to compare text or arbitrary binary data. Playwright Test auto-detects the content type and uses the appropriate comparison algorithm.

Here we compare text content against the reference.

```js title="example.spec.ts"
import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('https://playwright.dev');
  expect(await page.textContent('.hero__title')).toMatchSnapshot('hero.txt');
});
```

Snapshots are stored next to the test file, in a separate directory. For example, `my.spec.ts` file will produce and store snapshots in the `my.spec.ts-snapshots` directory. **You should commit this directory to your version control** (e.g. `git`), and review any changes to it.

---

## API: async method PageAssertions.toHaveScreenshot() (langs: js only: screenshot assertions only work with the Playwright test runner)
- since: v1.23

Two overloads:
1. `toHaveScreenshot(name, options)`: explicit snapshot name.
2. `toHaveScreenshot(options)`: auto-generated snapshot name.

This function will wait until two consecutive page screenshots yield the same result, and then compare the last screenshot with the expectation.

**Usage**

```js
await expect(page).toHaveScreenshot('image.png');

// Store the snapshot in the WebP format.
await expect(page).toHaveScreenshot('image.webp');
```

```js
await expect(page).toHaveScreenshot();
```

The snapshot is stored in the PNG format by default. To store it in the WebP format instead, pass a snapshot name with the `.webp` extension.

### Parameter: name
- `name` <string|Array<string>>

Snapshot name. Must have a `.png` or `.webp` extension, the screenshot is captured in the corresponding format. Both formats are lossless.

### Options (full table)

- `timeout` <float>: assertion timeout (JS assertions timeout macro).
- `signal` <AbortSignal> (since v1.62)
- `animations` <ScreenshotAnimations<"disabled"|"allow">>: **Note: for `toHaveScreenshot()`, this defaults to `"disabled"`** (unlike `page.screenshot()`/`locator.screenshot()`, which default `animations` to `"allow"`). When set to `"disabled"`, stops CSS animations, CSS transitions and Web Animations: finite animations are fast-forwarded to completion (firing `transitionend`), infinite animations are canceled to initial state and then played over after the screenshot.
- `caret` <ScreenshotCaret<"hide"|"initial">>: defaults to `"hide"`. Same as `page.screenshot()`.
- `clip` <Object>: `{x, y, width, height}`, same as `page.screenshot()`.
- `fullPage` <boolean>: defaults to `false`, same as `page.screenshot()`.
- `mask` <Array<Locator>>: same as `page.screenshot()`; masked elements overlaid with pink `#FF00FF` box (or `maskColor`).
- `maskColor` <string> (since v1.35): same as `page.screenshot()`, default `#FF00FF`.
- `stylePath` <string|Array<string>> (since v1.41): file name(s) containing the stylesheet to apply while making the screenshot; used to hide dynamic/volatile elements for determinism. Pierces Shadow DOM, applies to inner frames.
- `omitBackground` <boolean>: same as `page.screenshot()`, defaults to `false`, not applicable to jpeg.
- `scale` <ScreenshotScale<"css"|"device">>: **Note: for `toHaveScreenshot()`, this defaults to `"css"`** (unlike plain `page.screenshot()`, which defaults `scale` to `"device"`).
- `maxDiffPixels` <int>: An acceptable amount of pixels that could be different. Default is configurable with `TestConfig.expect`. Unset by default.
- `maxDiffPixelRatio` <float>: An acceptable ratio of pixels that are different to the total amount of pixels, between `0` and `1`. Default is configurable with `TestConfig.expect`. Unset by default.
- `threshold` <float>: An acceptable perceived color difference in the YIQ color space between the same pixel in compared images, between zero (strict) and one (lax). Default is configurable with `TestConfig.expect`. **Defaults to `0.2`.**

### Snapshot naming (consolidated from guide + API)

- Auto-generated name pattern: `<test-name>-<index>-<project-or-browser-name>-<platform>.png` (or `.webp` if that extension was requested), e.g. `example-test-1-chromium-darwin.png`.
- Explicit name: first positional argument to `toHaveScreenshot('landing.png')`, or an array of path segments `toHaveScreenshot(['relative', 'path', 'to', 'snapshot.png'])`: the resolved path must stay within the per-test-file snapshots directory (e.g. `a.spec.js-snapshots`), or it throws.
- Snapshot storage directory: sibling to the test file, named `<test-file-name>-snapshots` (e.g. `example.spec.ts` → `example.spec.ts-snapshots/`). Commit this directory to version control.
- The full name/path template is configurable via `TestConfig.snapshotPathTemplate` in the Playwright config.
- Uses the `pixelmatch` library under the hood for pixel diffing, tunable via `threshold`, `maxDiffPixels`, `maxDiffPixelRatio`.
- Update baselines with `npx playwright test --update-snapshots`.
