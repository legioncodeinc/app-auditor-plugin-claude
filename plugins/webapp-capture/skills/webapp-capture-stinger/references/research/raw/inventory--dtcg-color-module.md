# Design Tokens Color Module 2025.10
- URL: https://www.designtokens.org/tr/2025.10/color/
- Fetched: 2026-09-15
- Source type: spec
- Last updated (if shown): 28 October 2025 (Final Community Group Report, considered stable)

## Document identity

- **Title:** Design Tokens Color Module 2025.10
- **Status:** Final Community Group Report (published 28 October 2025)
- **Publication URL:** https://www.designtokens.org/TR/2025.10/color/
- **Editors:** Ayesha Mazrana, Kathleen McMahon, Adekunle Oduye, Matthew Strom-Awn
- **Abstract:** "the technical specification for design token color values and opacity."
- **Stability:** Explicitly "considered stable"; future updates come through superseding specifications.

This module is part of the same 2025.10 release as the Format module (`inventory--dtcg-format-spec.md`) and the Resolver module. It defines the `color` token type referenced there.

## Color token structure

### `$value` object requirements

**Required:**
- `colorSpace`: a string naming the color space (e.g. `"srgb"`, `"oklch"`)
- `components`: an array of color values, where each element must be either a number or the string `'none'`

**Optional:**
- `alpha`: a number between 0 and 1 (defaults to 1 if omitted). "0 is fully transparent and 1 is fully opaque."
- `hex`: a 6-digit CSS hex fallback value. "MUST be formatted in 6 digit CSS hex color notation."

"The `$type` property MUST be set to the string `color`."

Each `components` element "MUST be either: A number" or the `'none'` keyword. "The `none` keyword MAY be used in the `components` array to indicate that a component is not applicable."

## Supported color spaces

| Space | Key | Component structure |
|-------|-----|----------------------|
| sRGB | `"srgb"` | [Red, Green, Blue] [0-1] |
| sRGB linear | `"srgb-linear"` | [Red, Green, Blue] [0-1] |
| HSL | `"hsl"` | [Hue, Saturation, Lightness] |
| HWB | `"hwb"` | [Hue, Whiteness, Blackness] |
| CIELAB | `"lab"` | [Lightness, A, B] |
| LCH | `"lch"` | [Lightness, Chroma, Hue] |
| OKLAB | `"oklab"` | [Lightness, A, B] |
| OKLCH | `"oklch"` | [Lightness, Chroma, Hue] |
| Display P3 | `"display-p3"` | [Red, Green, Blue] [0-1] |
| A98 RGB | `"a98-rgb"` | [Red, Green, Blue] [0-1] |
| ProPhoto RGB | `"prophoto-rgb"` | [Red, Green, Blue] [0-1] |
| Rec 2020 | `"rec2020"` | [Red, Green, Blue] [0-1] |
| XYZ-D65 | `"xyz-d65"` | [X, Y, Z] [0-1] |
| XYZ-D50 | `"xyz-d50"` | [X, Y, Z] [0-1] |

## Normative statements

- Employs RFC 2119 language throughout.
- `colorSpace` and `components` are both required.
- The specification references CSS Color Module Level 4 as its normative baseline for color science concepts.
