# CSSStyleDeclaration.getPropertyValue() - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration/getPropertyValue
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): June 3, 2025

## Overview

The `CSSStyleDeclaration.getPropertyValue()` method returns a string containing the value of a specified CSS property. Widely available across browsers since July 2015.

## Syntax

```js
getPropertyValue(property)
```

### Parameters
- **`property`** (string): the property name in hyphen case to be checked (e.g. `"margin"`, `"background-color"`). This includes custom property names such as `--my-custom-property`.

### Return value
- A string containing the property value.
- Returns an empty string if the property is not set.

## Key behavior

### Value canonicalization
The method returns dynamically computed values, not the original declaration. CSS values are canonicalized:

- Color values are normalized to `rgb(R, G, B)` or `rgba(R, G, B, A)` format.
- Shorthand properties (like `margin`) expand to their longhand components.
- If a shorthand property has mixed `!important` statuses or undeclared components, an empty string is returned.
- Serialization follows each data type's canonical representation.

## Examples

### Basic usage
```js
const declaration = document.styleSheets[0].cssRules[0].style;
const value = declaration.getPropertyValue("margin"); // "1px 2px"
```

### Color value normalization

CSS input:
```css
p#blueish {
  color: hsl(250 90 50);
}
```

JavaScript output:
```js
const declaration = document.styleSheets[0].cssRules[0].style;
const value = declaration.getPropertyValue("color");
// Returns: "rgb(51, 13, 242)" (normalized format)
```

Important: string comparison of styles requires accounting for this canonicalization, as the returned value may differ from the original declaration text.

## Custom properties

`getPropertyValue()` is the mechanism used to read CSS custom properties (`--variable-name`) off a `CSSStyleDeclaration` (including the object returned by `getComputedStyle()`), e.g. `getComputedStyle(el).getPropertyValue('--my-custom-property')`. Custom property values are returned as their serialized string (untyped, exactly as declared/resolved), following the same canonicalization rules as standard properties where applicable.

## Browser compatibility

Baseline: Widely available across all modern browsers.

## Specifications

CSS Object Model (CSSOM), `dom-cssstyledeclaration-getpropertyvalue`: https://drafts.csswg.org/cssom/#dom-cssstyledeclaration-getpropertyvalue
