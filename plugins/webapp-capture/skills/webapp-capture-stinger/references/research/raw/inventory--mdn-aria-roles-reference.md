# ARIA roles reference - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): August 14, 2025

## Overview

ARIA roles provide semantic meaning to content, allowing screen readers and assistive technologies to present and support interaction with objects consistently with user expectations. They can describe elements that don't natively exist in HTML or lack full browser support.

## ARIA role categories

### 1. Document structure roles
Used to provide structural descriptions for content sections. Most should no longer be used as semantic HTML equivalents now exist.

**Roles without HTML equivalents (still useful):**
- `toolbar` - collection of commonly used function buttons
- `tooltip` - contextual text bubble on hover/focus
- `feed` - dynamic scrollable list of articles
- `math` - mathematical expression content
- `presentation` / `none` - remove implicit ARIA semantics
- `note` - parenthetic or ancillary section

**Roles to avoid (HTML alternatives exist):**
`application`, `article`, `cell`, `columnheader`, `definition`, `directory`, `document`, `figure`, `group`, `heading`, `img`, `list`, `listitem`, `meter`, `row`, `rowgroup`, `rowheader`, `separator`, `table`, `term`

**Rarely useful:**
`associationlist`, `associationlistitemkey`, `associationlistitemvalue`, `blockquote`, `caption`, `code`, `deletion`, `emphasis`, `insertion`, `paragraph`, `strong`, `subscript`, `superscript`, `time`

### 2. Widget roles
Used to define common interactive patterns. Typically require JavaScript for interaction.

**Standard widget roles:**
- `scrollbar` - controls scrolling
- `searchbox` - text input for search criteria
- `separator` - divider (when focusable)
- `slider` - user selects value from range
- `spinbutton` - discrete value selection
- `switch` - on/off toggle
- `tab` - interactive element in tablist
- `tabpanel` - container for tab content
- `treeitem` - item in tree structure

**Avoid using (native HTML alternatives):**
`button`, `checkbox`, `gridcell`, `link`, `menuitem`, `menuitemcheckbox`, `menuitemradio`, `option`, `progressbar`, `radio`, `textbox`

**Composite widget roles:**
- `combobox` - input/button controlling popup element
- `menu` - list of choices
- `menubar` - horizontal menu presentation
- `tablist` - container for tabs
- `tree` - hierarchical selection widget
- `treegrid` - grid with expandable rows

**Avoid using (composite):**
`grid`, `listbox`, `radiogroup`

### 3. Landmark roles
Identify organization and structure of web pages. Screen readers use these for keyboard navigation. Use sparingly to avoid "noise."

- `banner` - global site header (document `<header>`)
- `complementary` - supporting section (`<aside>`)
- `contentinfo` - footer (document `<footer>`)
- `form` - group of form elements (`<form>`)
- `main` - primary content area (`<main>`)
- `navigation` - major navigation groups (`<nav>`)
- `region` - significant document area (`<section>`)
- `search` - search functionality (`<search>`)

### 4. Live region roles
Define elements with dynamically changing content. Help assistive technologies announce updates:

- `alert` - important, time-sensitive information
- `log` - log of new information added in meaningful order
- `marquee` - non-essential, frequently changing information
- `status` - advisory information for users
- `timer` - numerical counter of elapsed/remaining time

### 5. Window roles
Define sub-windows within the main document window (e.g. modal dialogs):

- `alertdialog` - modal alert requiring user response
- `dialog` - application dialog or window (modal or non-modal)

### 6. Abstract roles
DO NOT USE IN MARKUP, only for browser organization. Developers should avoid these:

`command`, `composite`, `input`, `landmark`, `range`, `roletype`, `section`, `sectionhead`, `select`, `structure`, `widget`, `window`

## Key guidelines

Best practices:
- Prefer semantic HTML elements when available.
- Use ARIA to enhance, not replace, native elements.
- Ensure roles have associated required states/properties.
- Verify role creates accurate accessibility tree.

Common mistakes:
- Adding `role="tabpanel"` without nested tabs creates false semantics.
- Using abstract roles in content.
- Over-using landmark roles creates screen reader "noise."
- Using ARIA roles without proper keyboard handling.

## Example usage

```html
<!-- Good: Using semantic HTML -->
<button>Click me</button>

<!-- Acceptable: ARIA when necessary -->
<div role="button" tabindex="0">Custom button</div>

<!-- Bad: Unnecessary ARIA -->
<div role="list">
  <div role="listitem">Item 1</div> <!-- Use <ul>/<li> instead -->
</div>
```

For complete role documentation, individual role pages (linked from this index) include required ARIA states, properties, and implementation examples.
