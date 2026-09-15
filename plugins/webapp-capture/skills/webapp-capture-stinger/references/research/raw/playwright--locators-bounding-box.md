# Locators / ElementHandle: boundingBox() and scrollIntoViewIfNeeded() API reference + Scrolling guide
- URL: https://playwright.dev/docs/api/class-locator#locator-bounding-box and https://playwright.dev/docs/api/class-locator#locator-scroll-into-view-if-needed and https://playwright.dev/docs/input#scrolling
- Fetched: 2026-09-15
- Source type: official docs (API reference + guide, sourced from microsoft/playwright docs/src/api/class-locator.md, docs/src/api/class-elementhandle.md, docs/src/input.md on the `main` branch)
- Last updated (if shown): unknown

## GUIDE: Scrolling (from Input guide)

Most of the time, Playwright will automatically scroll for you before doing any actions. Therefore, you do not need to scroll explicitly.

```js
// Scrolls automatically so that button is visible
await page.getByRole('button').click();
```

However, in rare cases you might need to manually scroll. For example, you might want to force an "infinite list" to load more elements, or position the page for a specific screenshot. In such a case, the most reliable way is to find an element that you want to make visible at the bottom, and scroll it into view.

```js
// Scroll the footer into view, forcing an "infinite list" to load more content
await page.getByText('Footer text').scrollIntoViewIfNeeded();
```

```java
// Scroll the footer into view, forcing an "infinite list" to load more content
page.getByText("Footer text").scrollIntoViewIfNeeded();
```

```python async
# Scroll the footer into view, forcing an "infinite list" to load more content
await page.get_by_text("Footer text").scroll_into_view_if_needed()
```

```csharp
// Scroll the footer into view, forcing an "infinite list" to load more content
await page.GetByText("Footer text").ScrollIntoViewIfNeededAsync();
```

If you would like to control the scrolling more precisely, use `Mouse.wheel()` or `Locator.evaluate()`:

```js
// Position the mouse and scroll with the mouse wheel
await page.getByTestId('scrolling-container').hover();
await page.mouse.wheel(0, 10);

// Alternatively, programmatically scroll a specific element
await page.getByTestId('scrolling-container').evaluate(e => e.scrollTop += 100);
```

```python async
# Position the mouse and scroll with the mouse wheel
await page.get_by_test_id("scrolling-container").hover()
await page.mouse.wheel(0, 10)

# Alternatively, programmatically scroll a specific element
await page.get_by_test_id("scrolling-container").evaluate("e => e.scrollTop += 100")
```

---

## API: async method Locator.boundingBox()
- since: v1.14
- returns: `<null|Object>`
  - `x` <float> the x coordinate of the element in pixels.
  - `y` <float> the y coordinate of the element in pixels.
  - `width` <float> the width of the element in pixels.
  - `height` <float> the height of the element in pixels.

This method returns the bounding box of the element matching the locator, or `null` if the element is not visible. The bounding box is calculated relative to the main frame viewport: which is usually the same as the browser window.

**Details**

Scrolling affects the returned bounding box, similarly to `Element.getBoundingClientRect`. That means `x` and/or `y` may be negative.

Elements from child frames return the bounding box relative to the main frame, unlike `Element.getBoundingClientRect`.

Assuming the page is static, it is safe to use bounding box coordinates to perform input. For example, the following snippet should click the center of the element.

**Usage**

```js
const box = await page.getByRole('button').boundingBox();
await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
```

**Options:** `timeout` <float>, `signal` <AbortSignal> (JS).

---

## API: async method Locator.scrollIntoViewIfNeeded()
- since: v1.14

This method waits for actionability checks, then tries to scroll element into view, unless it is completely visible as defined by IntersectionObserver's `ratio`.

See "Scrolling" (above) for alternative ways to scroll.

**Options:**
- `timeout` <float>: JS: defaults to `0` (no timeout), configurable via `actionTimeout`; Python/Java/C#: defaults to `30000` ms, pass `0` to disable.
- `signal` <AbortSignal> (JS)

---

## API: async method ElementHandle.boundingBox()
- since: v1.8
- returns: `<null|Object>`: same shape as `Locator.boundingBox()`: `x`, `y`, `width`, `height` (float, pixels).

This method returns the bounding box of the element, or `null` if the element is not visible. The bounding box is calculated relative to the main frame viewport: which is usually the same as the browser window.

**Details**

Scrolling affects the returned bounding box, similarly to `Element.getBoundingClientRect`. That means `x` and/or `y` may be negative.

Elements from child frames return the bounding box relative to the main frame, unlike `Element.getBoundingClientRect`.

Assuming the page is static, it is safe to use bounding box coordinates to perform input. For example, the following snippet should click the center of the element.

**Usage**

```js
const box = await elementHandle.boundingBox();
await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
```

```python async
box = await element_handle.bounding_box()
await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
```

---

## API: async method ElementHandle.scrollIntoViewIfNeeded()
- since: v1.8
- **Discouraged**: Use locator-based `Locator.scrollIntoViewIfNeeded()` instead.

This method waits for actionability checks, then tries to scroll element into view, unless it is completely visible as defined by IntersectionObserver's `ratio`.

Throws when `elementHandle` does not point to an element connected to a Document or a ShadowRoot.

See "Scrolling" (above) for alternative ways to scroll.

**Options:** `timeout` <float> (same semantics as Locator variant above), `signal` <AbortSignal> (JS).

---

## Summary: Locator vs ElementHandle for these two methods

| Method | Locator (recommended) | ElementHandle (discouraged) |
|---|---|---|
| Bounding box | `locator.boundingBox()`: re-resolves the element each call, safe against DOM re-renders | `elementHandle.boundingBox()`: pinned to one specific DOM node handle; can go stale if the node is removed/replaced |
| Scroll into view | `locator.scrollIntoViewIfNeeded()` | `elementHandle.scrollIntoViewIfNeeded()`: explicitly marked "discouraged" in favor of the locator-based method, since element handles do not auto re-resolve and Playwright's own docs steer all new code toward Locators |

Both return `null`/throw under similar conditions (element not visible → `boundingBox()` returns `null`; element not connected to the DOM → `scrollIntoViewIfNeeded()` throws for ElementHandle). For any new capture-tooling code (e.g. scrolling an element into view before a `page.screenshot()` or `locator.screenshot()` call, or computing precise mouse-click coordinates for a masked/clipped screenshot), prefer the `Locator` APIs.
