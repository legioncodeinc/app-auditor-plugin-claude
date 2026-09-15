# Locators - Shadow DOM | Playwright

- URL: https://playwright.dev/docs/locators
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content

## Shadow DOM Locator Behavior (verbatim)

"All locators in Playwright by default work with elements in Shadow DOM. The exceptions are:

- Locating by XPath does not pierce shadow roots.
- Closed-mode shadow roots are not supported."

## Summary

Playwright's locators (including CSS-based locators like `getByRole`, `getByText`, `locator()`) automatically traverse (pierce) open Shadow DOM boundaries by default, with two key exceptions:

1. **XPath-based locators cannot pierce shadow roots.**
2. **Closed-mode shadow roots are unsupported** — a closed shadow root is invisible to scripts (and to Playwright); it cannot be pierced. This aligns with the standard DOM behavior where `element.shadowRoot` returns `null` for closed-mode roots (see MDN "Using shadow DOM").

## Relevance to capture-tool design

A capture tool using Playwright locators can rely on default locator piercing to find and screenshot elements inside open shadow roots (common in web-component-based design systems) without extra JS injection, but must account for closed shadow roots and XPath-based locator strategies as blind spots when building a component inventory.
