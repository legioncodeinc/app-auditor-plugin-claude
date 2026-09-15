# Design Tokens Community Group - Style Dictionary
- URL: https://styledictionary.com/info/dtcg/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (current major version docs, v4/v5)

## What is DTCG?

The Design Tokens W3C Community Group (DTCG) establishes standards for sharing design system tokens across tools and platforms. Style Dictionary provides "first-class support for the DTCG format" as of version 4.

The DTCG specification defines a standardized format for design tokens to ensure "cross-tool and cross-platform interoperability."

## Format differences: legacy vs. DTCG

**Legacy Style Dictionary format (v3):**
- Uses `value`, `type`, and `description` properties.
- Type information stored at the token group level.

**DTCG format:**
- Replaces property keys with dollar-sign-prefixed equivalents: `$value`, `$type`, `$description`.
- Moves `$type` from the highest common ancestor token group to individual tokens.

Note: in Style Dictionary v4 you can use either format, but pick one, as they cannot be combined inside a single Style Dictionary instance. The `usesDtcg` config option controls whether platform output treats tokens as `$value`/`$type` (DTCG) or `value`/`type` (legacy).

## Conversion tool

Style Dictionary offers an automated converter for migrating from v3 JSON format to DTCG, which:
- Converts legacy property names to DTCG equivalents.
- Distributes type information to individual tokens.
- Does NOT refactor type values (e.g. does not convert a legacy "size" type value to a DTCG "dimension" type value).

## CSS auto-conversion for DTCG color objects

When using the DTCG color object definition for the `color` property (i.e. `{ colorSpace, components, alpha, hex }`), Style Dictionary auto-converts it to a CSS-compatible string if available in the color space in which it is defined.

## Version support caveat

"The latest format 2025.10 does not have full support yet in Style Dictionary. This is a work in progress in v5."
