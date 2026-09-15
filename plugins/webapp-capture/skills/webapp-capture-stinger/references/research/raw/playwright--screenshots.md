# Screenshots (guide) + page.screenshot() / locator.screenshot() API reference
- URL: https://playwright.dev/docs/screenshots and https://playwright.dev/docs/api/class-page#page-screenshot and https://playwright.dev/docs/api/class-locator#locator-screenshot
- Fetched: 2026-09-15
- Source type: official docs (guide page + API reference, sourced from microsoft/playwright docs/src markdown on the `main` branch)
- Last updated (if shown): unknown (no per-page date shown on playwright.dev; content reflects the current `main` branch of microsoft/playwright as of fetch date)

Note: playwright.dev API reference pages are generated from the markdown source files in `microsoft/playwright/docs/src/api/*.md`, using macro includes (`%%-name-%%`) resolved against `microsoft/playwright/docs/src/api/params.md`. Because the live playwright.dev HTML page for `class-page` / `class-locator` is extremely large (auto-fetch truncated it), this archive was built by reading the markdown source directly and resolving the macros, which is faithful to the same rendered content.

---

## GUIDE: Screenshots (https://playwright.dev/docs/screenshots)

### Introduction

Here is a quick way to capture a screenshot and save it into a file:

```js
await page.screenshot({ path: 'screenshot.png' });
```

```python async
await page.screenshot(path="screenshot.png")
```

```python sync
page.screenshot(path="screenshot.png")
```

```java
page.screenshot(new Page.ScreenshotOptions()
      .setPath(Paths.get("screenshot.png")));
```

```csharp
await Page.ScreenshotAsync(new()
{
    Path = "screenshot.png",
});
```

[Screenshots API](./api/class-page#page-screenshot) accepts many parameters for image format, clip area, quality, etc. Make sure to check them out.

### Full page screenshots

Full page screenshot is a screenshot of a full scrollable page, as if you had a very tall screen and the page could fit it entirely.

```js
await page.screenshot({ path: 'screenshot.png', fullPage: true });
```

```java
page.screenshot(new Page.ScreenshotOptions()
  .setPath(Paths.get("screenshot.png"))
  .setFullPage(true));
```

```python async
await page.screenshot(path="screenshot.png", full_page=True)
```

```python sync
page.screenshot(path="screenshot.png", full_page=True)
```

```csharp
await Page.ScreenshotAsync(new()
{
    Path = "screenshot.png",
    FullPage = true,
});
```

### Capture into buffer

Rather than writing into a file, you can get a buffer with the image and post-process it or pass it to a third party pixel diff facility.

```js
const buffer = await page.screenshot();
console.log(buffer.toString('base64'));
```

```java
byte[] buffer = page.screenshot();
System.out.println(Base64.getEncoder().encodeToString(buffer));
```

```python async
# Capture into Image
screenshot_bytes = await page.screenshot()
print(base64.b64encode(screenshot_bytes).decode())
```

```python sync
screenshot_bytes = page.screenshot()
print(base64.b64encode(screenshot_bytes).decode())
```

```csharp
var bytes = await page.ScreenshotAsync();
Console.WriteLine(Convert.ToBase64String(bytes));
```

### Element screenshot

Sometimes it is useful to take a screenshot of a single element.

```js
await page.locator('.header').screenshot({ path: 'screenshot.png' });
```

```java
page.locator(".header").screenshot(new Locator.ScreenshotOptions().setPath(Paths.get("screenshot.png")));
```

```python async
await page.locator(".header").screenshot(path="screenshot.png")
```

```python sync
page.locator(".header").screenshot(path="screenshot.png")
```

```csharp
await page.Locator(".header").ScreenshotAsync(new() { Path = "screenshot.png" });
```

---

## API: async method Page.screenshot()

- since: v1.8
- returns: `<Buffer>`: the buffer with the captured screenshot.

Options (JS signature: `page.screenshot(options)`):

### fullPage
- `fullPage` <boolean>

When true, takes a screenshot of the full scrollable page, instead of the currently visible viewport. Defaults to `false`.

### clip
- `clip` <Object>
  - `x` <float> x-coordinate of top-left corner of clip area
  - `y` <float> y-coordinate of top-left corner of clip area
  - `width` <float> width of clipping area
  - `height` <float> height of clipping area

An object which specifies clipping of the resulting image.

### animations
- `animations` <ScreenshotAnimations<"disabled"|"allow">>

When set to `"disabled"`, stops CSS animations, CSS transitions and Web Animations. Animations get different treatment depending on their duration:
- finite animations are fast-forwarded to completion, so they'll fire `transitionend` event.
- infinite animations are canceled to initial state, and then played over after the screenshot.

Defaults to `"allow"` that leaves animations untouched. (Note: on `locator.screenshot()` and `page.screenshot()` this same definition applies via the shared `screenshot-options-common-list`; some other screenshot-taking APIs, e.g. visual comparisons' `toHaveScreenshot`, default `animations` to `"disabled"` instead: see the Visual comparisons archive file.)

### caret
- `caret` <ScreenshotCaret<"hide"|"initial">>

When set to `"hide"`, screenshot will hide text caret. When set to `"initial"`, text caret behavior will not be changed. Defaults to `"hide"`.

### scale
- `scale` <ScreenshotScale<"css"|"device">>

When set to `"css"`, screenshot will have a single pixel per each css pixel on the page. For high-dpi devices, this will keep screenshots small. Using `"device"` option will produce a single pixel per each device pixel, so screenshots of high-dpi devices will be twice as large or even larger.

Defaults to `"device"`.

(Note: for `expect(locator).toHaveScreenshot()` / visual-comparisons snapshot assertions, `scale` instead defaults to `"css"`: see the Visual comparisons archive file, which uses the `screenshot-option-scale-default-css` macro variant.)

### mask
- `mask` <Array<Locator>>

Specify locators that should be masked when the screenshot is taken. Masked elements will be overlaid with a pink box `#FF00FF` (customized by `maskColor`) that completely covers its bounding box. The mask is also applied to invisible elements: see "Matching only visible elements" in the locators guide to disable that.

### maskColor
- since: v1.35
- `maskColor` <string>

Specify the color of the overlay box for masked elements, in CSS color format. Default color is pink `#FF00FF`.

### style
- since: v1.41
- `style` <string>

Text of the stylesheet to apply while making the screenshot. This is where you can hide dynamic elements, make elements invisible or change their properties to help you creating repeatable screenshots. This stylesheet pierces the Shadow DOM and applies to the inner frames.

(Related, not part of the common options list, but available on `page.screenshot()` and via `stylePath` on related APIs: `stylePath` <string|Array<string>>: File name containing the stylesheet to apply while making the screenshot. Same purpose as `style`, but from file(s). Pierces Shadow DOM and applies to inner frames.)

### omitBackground
- `omitBackground` <boolean>

Hides default white background and allows capturing screenshots with transparency. Not applicable to `jpeg` images. Defaults to `false`.

### quality
- `quality` <int>

The quality of the image, between 0-100. Not applicable to `png` images. For `jpeg` the default is `80`. For `webp`, a quality of `100` (the default) produces a lossless image, while lower values use lossy compression.

### path
- `path` <path>

The file path to save the image to. The screenshot type will be inferred from file extension. If `path` is a relative path, then it is resolved relative to the current working directory. If no path is provided, the image won't be saved to the disk.

### type
- `type` <ScreenshotType<"png"|"jpeg"|"webp">>

Specify screenshot type, defaults to `png`.

### timeout
- JS: `timeout` <float>: Maximum time in milliseconds. Defaults to `0`: no timeout. The default value can be changed via `actionTimeout` option in the config, or by using `browserContext.setDefaultTimeout()` or `page.setDefaultTimeout()`.
- Python/Java/C#: `timeout` <float>: Maximum time in milliseconds. Defaults to `30000` (30 seconds). Pass `0` to disable timeout. The default value can be changed by using `browserContext.setDefaultTimeout()` or `page.setDefaultTimeout()`.

### signal
- `signal` <AbortSignal> (JS): allows aborting via an AbortSignal.

---

## API: async method Locator.screenshot()

- since: v1.14
- returns: `<Buffer>`: the buffer with the captured screenshot.

Take a screenshot of the element matching the locator.

**Usage**

```js
await page.getByRole('link').screenshot();
```

```java
page.getByRole(AriaRole.LINK).screenshot();
```

```python async
await page.get_by_role("link").screenshot()
```

```python sync
page.get_by_role("link").screenshot()
```

```csharp
await page.GetByRole(AriaRole.Link).ScreenshotAsync();
```

Disable animations and save screenshot to a file:

```js
await page.getByRole('link').screenshot({ animations: 'disabled', path: 'link.png' });
```

```java
page.getByRole(AriaRole.LINK).screenshot(new Locator.ScreenshotOptions()
    .setAnimations(ScreenshotAnimations.DISABLED)
    .setPath(Paths.get("example.png")));
```

```python async
await page.get_by_role("link").screenshot(animations="disabled", path="link.png")
```

```python sync
page.get_by_role("link").screenshot(animations="disabled", path="link.png")
```

```csharp
await page.GetByRole(AriaRole.Link).ScreenshotAsync(new() {
  Animations = ScreenshotAnimations.Disabled,
  Path = "link.png"
});
```

**Details**

This method captures a screenshot of the page, clipped to the size and position of a particular element matching the locator. If the element is covered by other elements, it will not be actually visible on the screenshot. If the element is a scrollable container, only the currently scrolled content will be visible on the screenshot.

This method waits for the actionability checks, then scrolls element into view before taking a screenshot. If the element is detached from DOM, the method throws an error.

Returns the buffer with the captured screenshot.

**Options**: `locator.screenshot()` accepts the same common screenshot options list as `page.screenshot()`: `animations`, `omitBackground`, `quality`, `path`, `scale`, `caret`, `type`, `mask`: plus:
- `timeout` (same semantics as `page.screenshot()`'s timeout, since v1.14)
- `signal` <AbortSignal> (JS)
- `maskColor` <string> (since v1.34, same definition as `page.screenshot()`)
- `style` <string> (since v1.41, same definition as `page.screenshot()`)

Note: `locator.screenshot()` does not accept `fullPage` or `clip`: those are page-level concepts; the locator screenshot is inherently clipped to the element's bounding box.
