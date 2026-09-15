# Understanding SC 1.4.11: Non-text Contrast — WCAG 2.2
- URL: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- Fetched: 2026-09-15
- Source type: spec (W3C official Understanding document)
- Last updated (if shown): unknown (W3C WAI living document for WCAG 2.2)

## Success criterion text

"The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s): User Interface Components — Visual information required to identify user interface components and states, except for inactive components or where the appearance of the component is determined by the user agent and not modified by the author; Graphical Objects — Parts of graphics required to understand the content, except when a particular presentation of graphics is essential to the information being conveyed."

## Intent

To "ensure that user interface components (i.e., controls) and meaningful graphics are distinguishable by people with moderately low vision." This mirrors the contrast requirement for large text, recognizing that low-contrast controls and graphics are easily missed by people with visual impairments even though the controls/graphics themselves aren't text.

## The 3:1 threshold

Computed values should not be rounded (e.g., a measured 2.999:1 would not meet the 3:1 threshold).

## What it applies to

**User Interface Components:**
- Visual information needed to identify controls and their states (e.g., the boundary of a text input, the visible affordance of a button).
- Excludes inactive/disabled components.
- Does not apply to a state change that is conveyed purely by a color change between two states that are never visible adjacent to each other simultaneously.

**Graphical Objects:**
- Parts of graphics required to understand the content (icons, chart lines, form-field boundaries, etc.).
- Exempted when the specific presentation is "essential" to the information being conveyed and cannot be altered without losing meaning — e.g., logos, flags, sensory photographs, medical diagnostic images/diagrams.

## Key exceptions

1. Inactive components are exempt.
2. Essential presentations (logos, flags, sensory photographs, medical diagrams) that cannot be altered without losing meaning.
3. Graphics that already have an accessible text alternative conveying the equivalent information don't require the graphic itself to meet contrast.

## Additional notes

- Focus indicators must maintain 3:1 contrast against adjacent background(s).
- Hover states don't require the 3:1 contrast unless the hover-state visual change is essential to identifying that hover occurred.
- Borders that indicate a control's hit area aren't separately required to meet 3:1 when visible content (text/icon) inside the control already identifies it.

## Notes for webapp-capture-stinger

1.4.3 (text) and 1.4.11 (non-text: UI components and graphical objects) together define the two WCAG contrast checks relevant to an automated UI-inconsistency audit: text-vs-background contrast (4.5:1 / 3:1 large text) and control/icon-vs-adjacent-color contrast (3:1 flat). Both use the same relative-luminance contrast-ratio formula from 1.4.3's Understanding doc.
