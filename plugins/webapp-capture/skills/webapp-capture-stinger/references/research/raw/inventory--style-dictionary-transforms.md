# Built-in transforms - Style Dictionary
- URL: https://styledictionary.com/reference/hooks/transforms/predefined/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (current major version docs, v4/v5)

## Overview

Style Dictionary provides 60+ predefined transforms organized by category. From version 4 onwards, transforms match tokens using the `token.type` property rather than the legacy CTI (Category/Type/Item) structure.

## Transform categories

### Attribute transforms
- **attribute/cti**: adds category, type, item, subitem, and state based on token location.
- **attribute/color**: extracts hex, hsl, hsv, and rgb color properties.

### Name/formatting transforms
- **name/human**: produces human-readable format ("button primary").
- **name/camel**: creates camelCase naming (with optional prefix support).
- **name/kebab**: generates kebab-case identifiers.
- **name/snake**: produces snake_case format.
- **name/constant**: creates CONSTANT_CASE naming.
- **name/pascal**: generates PascalCase identifiers.

### Color transforms
Converts color tokens to various formats:
- **color/rgb**, **color/hsl**, **color/hsl-4**: CSS color functions.
- **color/hex**, **color/hex8**: hexadecimal representations.
- **color/hex8android**: Android format (alpha channel first).
- **color/UIColor**, **color/UIColorSwift**, **color/ColorSwiftUI**: iOS/Swift formats.
- **color/composeColor**: Jetpack Compose Color class.
- **color/sketch**: Sketch-compatible object format.
- **color/hex8flutter**: Flutter Color objects.

### Size transforms
Platform-specific sizing conversions:
- **size/px**, **size/rem**: basic web units.
- **size/remToPx**, **size/pxToRem**: web unit conversions.
- **size/sp**, **size/dp**: Android scalable/density pixels.
- **size/remToSp**, **size/remToDp**: web-to-Android conversions.
- **size/remToFloat**, **size/remToPt**: scaling with configurable `basePxFontSize`.
- **size/compose/** variants: Jetpack Compose extensions (`.sp`, `.dp`, `.em`).
- **size/swift/remToCGFloat**: Swift CGFloat initialization.
- **size/flutter/remToDouble**: Flutter point conversions.

### DTCG-specific object transforms
Handles Design Token Community Group formatted composite tokens:
- **fontFamily/css**: converts font family arrays to CSS strings with proper quoting.
- **cubicBezier/css**: transforms to a `cubic-bezier()` function.
- **border/css/shorthand**: CSS border shorthand notation.
- **typography/css/shorthand**: CSS font shorthand (e.g. `italic 400 1.2rem/1.5 'Font'`).
- **transition/css/shorthand**: CSS transition shorthand.
- **shadow/css/shorthand**: multiple shadow support with optional color conversion.
- **strokeStyle/css/shorthand**: stroke pattern output.

### Content transforms
- **content/quote**: single-quoted strings.
- **content/objC/literal**: Objective-C string literals (`@"string"`).
- **content/swift/literal**: Swift string literals.
- **content/flutter/literal**: Flutter string literals.

### Asset transforms
- **asset/url**: wraps in CSS `url()` function.
- **asset/base64**: base64-encoded asset data.
- **asset/path**: local file path reference.
- **asset/objC/literal**, **asset/swift/literal**, **asset/flutter/literal**: language-specific formats.

### Miscellaneous
- **html/icon**: HTML entity transformation for CSS.
- **time/seconds**: milliseconds to decimal seconds conversion.

All transforms support optional platform-level configuration, particularly `basePxFontSize` for scaling operations (default: 16).
