# Understanding SC 1.4.3: Contrast (Minimum) — WCAG 2.2
- URL: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Fetched: 2026-09-15
- Source type: spec (W3C official Understanding document)
- Last updated (if shown): unknown (W3C WAI living document for WCAG 2.2)

## Success criterion text

"The visual presentation of text and images of text has a contrast ratio of at least 4.5:1," with exceptions for:
- Large text — 3:1 ratio.
- Incidental text (e.g., text that is part of an inactive UI component, pure decoration, not visible to anyone, or part of a picture that contains significant other visual content).
- Logotypes (text that is part of a logo or brand name has no minimum contrast requirement).

## Intent

Ensures sufficient contrast so people with moderately low vision or impaired contrast perception can read text without needing assistive technology (e.g. a screen magnifier). Contrast is calculated using relative luminance rather than raw color, because this approach also accommodates color vision deficiencies (the ratio is defined independent of hue).

## Contrast ratio formula

Contrast ratio = **(L1 + 0.05) / (L2 + 0.05)**, where:
- L1 = relative luminance of the lighter of the two colors.
- L2 = relative luminance of the darker of the two colors.

## Thresholds

- **Standard/normal text**: 4.5:1 minimum. This ratio was chosen to compensate for the loss in contrast sensitivity usually experienced by users with vision equivalent to approximately 20/40 vision (a level of vision loss that is common with aging).
- **Large text**: 3:1 minimum, because larger text is more legible at lower contrast.

## Large text definition

Text qualifies as "large scale" at "at least 18 point or 14 point bold, or a font size that would yield equivalent size for Chinese, Japanese, and Korean (CJK) fonts."

## Exceptions

- Logotypes — text that is part of a logo or brand name has no contrast requirement.
- Pure decoration — text that isn't intended to be read (e.g. randomly decorative words).
- Incidental text — such as street signs incidentally captured within a photograph.
- Inactive user interface components.
- Text within pictures that contain significant other visual content.

## Referenced resources

The Understanding document references contrast-checking tools including Adobe Color Contrast Analyzer and TPGI's Colour Contrast Analyser, plus academic sources on color vision deficiency and contrast sensitivity that informed the threshold choices.
