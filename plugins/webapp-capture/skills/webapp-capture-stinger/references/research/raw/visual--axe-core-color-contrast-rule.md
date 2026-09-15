# Elements must have sufficient color contrast (color-contrast) — axe-core / Deque University
- URL: https://dequeuniversity.com/rules/axe/4.10/color-contrast (rule descriptions index: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- Fetched: 2026-09-15
- Source type: official docs (Deque University axe rule reference)
- Last updated (if shown): versioned to axe-core 4.10; unknown exact publish date

## Rule description

"All text elements must have sufficient contrast between text in the foreground and background colors" per WCAG 2 AA standards. The rule checks all text elements to ensure the contrast between foreground text and background colors meets the WCAG 2 AA contrast ratio thresholds — 4.5:1 for small text or 3:1 for large text, even when the text is part of an image.

## Scope and limitations

The rule will **not** report on text elements that:
- Have a background-image (can't reliably compute effective background color/luminance).
- Are obscured by other elements.
- Are images of text (not evaluated by the DOM/CSS-based algorithm).

It accounts for color transparency and opacity in backgrounds but has documented difficulty detecting foreground opacity accurately when gradients, pseudo-elements, borders, or overlapping elements are involved. Child elements of disabled buttons are ignored to avoid false positives (inactive UI components are not required to meet contrast per WCAG 1.4.3/1.4.11).

## Why it matters

- **Low vision**: people with low vision struggle when text luminance is too similar to the background, making details hard to distinguish.
- **Color blindness**: roughly 8% of men and 0.4% of women in the US cannot perceive the full color spectrum, so contrast (not hue alone) must carry the distinction.
- **Prevalence**: nearly three times more people experience low vision than total blindness — making this one of the highest-impact automated accessibility checks.

## How to fix

Ensure contrast ratios meet:
- **Small text**: minimum 4.5:1.
- **Large text** (18pt / 24 CSS px, or 14pt bold / 19 CSS px): minimum 3:1.

Recommended tooling: axe DevTools browser extension, or the axe-core library directly, to analyze and validate contrast ratios programmatically.

## Disabilities affected

- Low vision
- Colorblindness

## WCAG success criteria mapped

**1.4.3 Contrast (Minimum)** — required at WCAG 2.0 AA, 2.1 AA, and 2.2 AA.

## Version note

axe-core 3.5 significantly improved the color-contrast rule's speed and accuracy, "completely changing how the functionality works" versus earlier versions — worth pinning to a recent axe-core version rather than an old cached copy when embedding this check in a capture/audit pipeline.
