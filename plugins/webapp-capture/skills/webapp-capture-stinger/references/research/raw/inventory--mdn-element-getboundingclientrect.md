# Element.getBoundingClientRect() - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): October 30, 2025

## Overview

`Element.getBoundingClientRect()` returns a `DOMRect` object providing information about the size of an element and its position relative to the viewport.

Status: Baseline, widely available since July 2015.

## Syntax

```javascript
getBoundingClientRect()
```

No parameters.

## Return value

Returns a `DOMRect` object with the following properties:

| Property | Description |
|----------|-------------|
| `x` | Left position relative to viewport |
| `y` | Top position relative to viewport |
| `left` | Same as `x` |
| `top` | Same as `y` |
| `right` | Right edge position relative to viewport |
| `bottom` | Bottom edge position relative to viewport |
| `width` | Element width (includes padding and border) |
| `height` | Element height (includes padding and border) |

### Key notes on return value

- The rectangle is the smallest rectangle containing the entire element, including padding and border-width.
- `width`/`height` include padding and border-width (equivalent to CSS `width`/`height` + `padding` + `border-width`).
- With `box-sizing: border-box`, `width`/`height` equal the element's CSS `width`/`height` directly.
- All coordinates except `width`/`height` are relative to the top-left of the viewport.
- Empty border-boxes are ignored; if all boxes are empty, returns a rectangle with `width: 0`, `height: 0`.

## Viewport-relative coordinates and scrolling

Important: the returned coordinates are relative to the viewport, not the document.

- Values change when the page is scrolled since they're viewport-relative.
- The scroll position of the viewport (or any scrollable element) is taken into account.
- To get document-relative coordinates, add the scroll position:

```javascript
const rect = element.getBoundingClientRect();
const absoluteTop = rect.top + window.scrollY;
const absoluteLeft = rect.left + window.scrollX;
```

## Examples

### Basic example
```javascript
let elem = document.querySelector("div");
let rect = elem.getBoundingClientRect();

console.log(rect.x);      // left position
console.log(rect.y);      // top position
console.log(rect.width);  // width with padding + border
console.log(rect.height); // height with padding + border
```

### HTML example
```html
<div></div>
```

```css
div {
  width: 400px;
  height: 200px;
  padding: 20px;
  margin: 50px auto;
  background: purple;
}
```

```javascript
let elem = document.querySelector("div");
let rect = elem.getBoundingClientRect();
for (const key in rect) {
  if (typeof rect[key] !== "function") {
    console.log(`${key} : ${rect[key]}`);
  }
}
```

Note: `width`/`height` equal 400+40 = 440 and 200+40 = 240 respectively (content + padding).

### Scrolling example
```javascript
function update() {
  const elem = document.getElementById("example");
  const rect = elem.getBoundingClientRect();

  console.log(`top: ${rect.top}`);    // Changes as you scroll
  console.log(`left: ${rect.left}`);  // Changes as you scroll
}

document.addEventListener("scroll", update);
```

## Specification

CSSOM View Module, `Element.getBoundingClientRect()`: https://drafts.csswg.org/cssom-view/#dom-element-getboundingclientrect
