# Window.getComputedStyle() - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): May 11, 2026

## Syntax

```javascript
getComputedStyle(element)
getComputedStyle(element, pseudoElt)
```

## Parameters

- **`element`** (required): The `Element` for which to get the computed style.
- **`pseudoElt`** (optional): A string specifying the pseudo-element to match (e.g. `::after`, `::before`). Omitted or `null` for real elements.

## Return value

A **live** `CSSStyleProperties` object containing the resolved values of all CSS properties of an element. The object updates automatically when the element's styles change.

Note: earlier specifications returned a `CSSStyleDeclaration` (which `CSSStyleProperties` derives from).

## Exceptions

- **`TypeError`**: thrown if the passed object is not an `Element`, or if `pseudoElt` is not a valid pseudo-element selector (or is `::part()` or `::slotted()`).

## Description

The method returns a **live, read-only** `CSSStyleProperties` object containing resolved CSS property values after applying active stylesheets and resolving any computations those values contain.

Key characteristics:
- **Read-only**: cannot be used to set styles directly
- **Live**: updates automatically when element styles change via other APIs
- **Comprehensive**: includes all CSS properties supported by the browser (both shorthand and longhand)
- **Property access**: properties available in both dash-named (`border-top-color`) and camelCase (`borderTopColor`) formats

### Shorthand expansion
Shorthand properties are expanded to their longhand equivalents. For example, `"border-top: 1px solid black"` provides `border-top`/`borderTop`, `border-top-color`/`borderTopColor`, `border-top-style`/`borderTopStyle`, `border-top-width`/`borderTopWidth`.

### Color values
- sRGB colors with alpha = 1: serialized as `rgb(255, 0, 0)`
- Other colors: serialized as `rgba(255, 0, 0, 0.5)`
- Other color spaces: `lab()`, `lch()`, `oklab()`, `oklch()`, `color()`

### Security note
Browsers may deliberately return inaccurate values for visited links to prevent CSS history leaks.

## Examples

### Retrieving resolved styles

```html
<p>Hello</p>
```

```css
p {
  width: 400px;
  margin: 0 auto;
  padding: 20px;
  font: 2rem/2 sans-serif;
  text-align: center;
  background: purple;
  color: white;
}
```

```javascript
const para = document.querySelector("p");
const compStyles = window.getComputedStyle(para);
para.textContent =
  `My computed font-size is ${compStyles.getPropertyValue("font-size")},\n` +
  `and my computed line-height is ${compStyles.getPropertyValue("line-height")}.`;
```

### Using with pseudo-elements

```html
<h3>Generated content</h3>
```

```css
h3::after {
  content: " rocks!";
}
```

```javascript
const h3 = document.querySelector("h3");
const result = getComputedStyle(h3, "::after").content;
console.log("the generated content is: ", result); // returns ' rocks!'
```

## Specifications

CSS Object Model (CSSOM), `dom-window-getcomputedstyle`: https://drafts.csswg.org/cssom/#dom-window-getcomputedstyle

## Browser compatibility

Baseline: Widely available, across browsers since July 2015.

## See also

- `window.getDefaultComputedStyle()`
- `CSSStyleDeclaration.getPropertyValue()`
- `Element.computedStyleMap()`
- Resolved value (CSS cascade processing docs)
