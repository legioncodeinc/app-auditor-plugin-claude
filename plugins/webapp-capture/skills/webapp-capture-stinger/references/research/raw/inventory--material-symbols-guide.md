# Material Symbols guide - Google Fonts (Google for Developers)
- URL: https://developers.google.com/fonts/docs/material_symbols
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): September 26, 2024

## Overview

"Material Symbols are our newest icons, consolidating over 2,500 glyphs in a single font file with a wide range of design variants." The collection offers three styles (Outlined, Rounded, Sharp) and four adjustable variable font axes for customization.

## Variable font axes

- **Fill**: allows modification between unfilled (0) and filled (1) states, useful for conveying state transitions through animation.
- **Weight (wght)**: ranges from thin (100) to bold (700), defining stroke weight and affecting overall symbol size.
- **Grade (GRAD)**: provides more granular thickness adjustments than weight, with minimal size impact. Values like -25 reduce glare; 200+ emphasize symbols. Can match text font grades for visual harmony.
- **Optical Size (opsz)**: ranges from 20dp to 48dp, automatically adjusting stroke weight proportionally as icon size changes.

## Implementation methods

**Web via Google Fonts**: a single HTML `<link>` loads the font with default settings (weight 400, optical size 48, grade 0, fill 0).

**Ligatures**: the preferred rendering method uses text names like `arrow_forward` as the element's text content instead of numeric character references; supported in most modern browsers. This is the ligature feature described elsewhere as: "This example uses a typographic feature called ligatures, which allows rendering of an icon glyph simply by using its textual name." Reference the icon using the ligature name (e.g. `search`) or its Unicode codepoint.

**Codepoints**: alternative approach using numeric character references for legacy browser support.

**Subsetting**: use the `&icon_names` query parameter with an alphabetically sorted, comma-separated list of icon names (which are the ligatures) to reduce font payload (e.g. from 295 KB to 1.7 KB).

**Self-hosting**: download fonts from the Git repository and declare via custom `@font-face` CSS rules.

## Additional platforms

Icons are also available in Vector Drawable format for Android and Apple Symbols format for iOS. Flutter support is planned.
