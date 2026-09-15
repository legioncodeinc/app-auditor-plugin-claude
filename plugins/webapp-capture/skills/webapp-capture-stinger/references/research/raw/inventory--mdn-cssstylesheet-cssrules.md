# CSSStyleSheet: cssRules property - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/cssRules
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): April 7, 2023 (cssRules page); December 19, 2025 (CSSStyleSheet interface page, cited below for the cross-origin note)

## Overview

The `cssRules` property is a read-only property of the `CSSStyleSheet` interface that returns a live `CSSRuleList` containing every CSS rule that comprises the stylesheet.

## Return value

A live-updating `CSSRuleList` where each entry is a `CSSRule` object describing a single rule in the stylesheet. The list updates in real time as the stylesheet changes.

## Key characteristics

- Read-only: cannot be set directly.
- Live-updating: reflects changes to the stylesheet immediately.
- Baseline: widely available since July 2015 across all major browsers.

## Usage examples

### Access rules by index
```javascript
const ruleList = document.styleSheets[0].cssRules;

for (let i = 0; i < ruleList.length; i++) {
  processRule(ruleList[i]);
}
```

### Using for...of
```javascript
const ruleList = document.styleSheets[0].cssRules;

for (const rule of ruleList) {
  processRule(rule);
}
```

Important limitation: `CSSRuleList` is not a proper array, so `forEach()` cannot be used directly on it without conversion (e.g. `Array.from(ruleList)`).

## Cross-origin stylesheet access restrictions

From the `CSSStyleSheet` interface overview page (parent of `cssRules`):

> Note: In some browsers, if a stylesheet is loaded from a different domain, accessing `cssRules` results in a `SecurityError`.

When attempting to programmatically access the rules of a stylesheet loaded from a different origin/domain (e.g. a cross-origin `<link rel="stylesheet">` without appropriate CORS headers), browsers throw a `SecurityError` exception to prevent unauthorized access to cross-origin styling information. This applies to `cssRules` and equally to the legacy `rules` property, which is functionally identical. This is a browser security measure to protect user privacy and prevent information leakage across domain boundaries. Practical implication for style/token extraction tooling: catching and handling `SecurityError` (or filtering `document.styleSheets` entries whose `cssRules` access throws) is required when iterating all stylesheets on a page that may include cross-origin CSS.

## Specifications

CSS Object Model (CSSOM), `dom-cssstylesheet-cssrules`: https://drafts.csswg.org/cssom/#dom-cssstylesheet-cssrules
