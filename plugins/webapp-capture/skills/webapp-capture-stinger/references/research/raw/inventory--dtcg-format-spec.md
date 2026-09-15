# Design Tokens Format Module 2025.10
- URL: https://www.designtokens.org/tr/2025.10/format/
- Fetched: 2026-09-15
- Source type: spec
- Last updated (if shown): 28 October 2025 (Final Community Group Report, considered stable)

## Document metadata

- **Title:** Design Tokens Format Module 2025.10
- **Status:** Final Community Group Report (28 October 2025)
- **Publication URL:** https://www.designtokens.org/TR/2025.10/format/
- **Abstract:** This specification defines a technical file format enabling the exchange of design tokens between tools, using JSON as the interchange medium.
- **Classification:** Candidate Recommendation, intended for implementation after extensive consensus-building. The specification is considered stable; future updates will come through superseding specifications.
- **Editors:** Louis Chenais, Kathleen McMahon, Drew Powers, Matthew Strom-Awn, Donna Vitan
- **Authors:** Daniel Banks, Mike Kamminga, Ayesha Mazrana (Mazumdar), James Nash, Adekunle Oduye, Kevin Powell
- **Published by:** Design Tokens Community Group under the W3C Community Final Specification Agreement

Note: the "living draft" copy of this document lives at https://www.designtokens.org/tr/drafts/format/ and carries the warning "This is a preview draft of in progress changes. Do not refer to this document directly, and do not implement anything in this document." The archived content below is from the 2025.10 stable release, not the draft.

## Core token structure

A design token is "information associated with a human readable name, at minimum a name/value pair." All tokens require:

1. **Token Name** - the key identifier (case-sensitive JSON string)
2. **`$value`** - the required property containing the actual token data. "An object with a `$value` property is a token."

### `$value` (required)
Mandatory for all tokens; content varies by token type.

### `$type` (conditional)
Determines how the value should be interpreted. "If the `$type` property is not set on a token, then the token's type _MUST_ be determined" through this resolution order:

1. Token's explicit `$type` property
2. Resolved group's `$type` property (if applicable)
3. Parent group's `$type` property (walking hierarchy)
4. Token becomes invalid if no type is determinable

"Tools _MUST NOT_ attempt to guess the type of a token by inspecting" its value.

### `$description` (optional)
A plain JSON string explaining the token's purpose. Tools may use descriptions in style guides, IDEs, design tools, or as source code comments.

### `$deprecated` (optional)
Marks tokens as deprecated:

| Value | Meaning |
|-------|---------|
| `true` | Deprecated (no explanation) |
| `false` | Not deprecated (overrides defaults) |
| `"string"` | Deprecated with explanation provided |

Tools may augment deprecated strings containing token aliases by resolving them to documentation links.

### `$extensions` (optional)
Vendor-specific metadata object. "each tool _MUST_ use a vendor-specific key whose value _MAY_ be any valid JSON data." Reverse domain notation (e.g. `"org.example.tool-a"`) is recommended.

"Tools that process design token files _MUST_ preserve any extension data they do not themselves understand."

### Character restrictions
Token and group names must not:
- begin with `$` (reserved for properties)
- contain `{`, `}`, or `.`

These restrictions enable safe use of reference syntax.

## Complete type system

### Atomic types

**Color** - represents UI colors. Full definition lives in the separate Color module (see `inventory--dtcg-color-module.md`). Values follow a color object structure with `colorSpace`, `components`, and an optional `hex` fallback.

**Dimension** - measures distance in a single dimension.

| Property | Type | Required | Details |
|----------|------|----------|---------|
| `value` | number | Yes | Integer or floating-point |
| `unit` | string | Yes | Only `"px"` or `"rem"` permitted |

Example: `{"value": 16, "unit": "px"}`

Units: **px** = idealized viewport pixel (equivalent to Android `dp`, iOS `pt`); **rem** = multiple of system default font size (equivalent to Android `16sp`).

**Font Family** - single string or ordered array of strings, e.g. `"Comic Sans MS"` or `["Helvetica", "Arial", "sans-serif"]`.

**Font Weight** - numeric [1, 1000] or predefined string aliases:

| Numeric | String Aliases |
|---------|----------------|
| 100 | thin, hairline |
| 200 | extra-light, ultra-light |
| 300 | light |
| 400 | normal, regular, book |
| 500 | medium |
| 600 | semi-bold, demi-bold |
| 700 | bold |
| 800 | extra-bold, ultra-bold |
| 900 | black, heavy |
| 950 | extra-black, ultra-black |

"Number values outside of the [1, 1000] range and any other string values...are invalid and _MUST_ be rejected."

**Duration** - animation/timing length.

| Property | Type | Required | Details |
|----------|------|----------|---------|
| `value` | number | Yes | Integer or floating-point |
| `unit` | string | Yes | Only `"ms"` or `"s"` permitted |

**Cubic Bezier** - animation progression curve as an array of four numbers `[P1x, P1y, P2x, P2y]`. Y coordinates: any real number. X coordinates: restricted to [0, 1].

**Number** - unitless numeric value (positive, negative, fractional). Used for gradient stop positions and unitless line heights.

### Composite types
Composite types combine multiple values following predefined structures. Sub-values may be explicit values or references to tokens of the appropriate type.

**Shadow** - drop shadow styling:

| Property | Type | Accepts |
|----------|------|---------|
| `color` | color | Color value or color token reference |
| `offsetX` | dimension | Dimension value or reference |
| `offsetY` | dimension | Dimension value or reference |
| `blur` | dimension | Dimension value or reference |
| `spread` | dimension | Dimension value or reference |

May be a single shadow object or an array of shadow objects/references (no flattening occurs).

**Border** - border styling:

| Property | Type | Accepts |
|----------|------|---------|
| `color` | color | Color value or reference |
| `width` | dimension | Dimension value or reference |
| `style` | strokeStyle | Stroke style value or reference |

**Stroke Style** - line/border styling. Either:
- A predefined string: `solid`, `dashed`, `dotted`, `double`, `groove`, `ridge`, `outset`, `inset` (meanings align with CSS `border-style`)
- An object: `{ dashArray: [dimension values/references, alternating dashes/gaps], lineCap: "round" | "butt" | "square" }`

**Transition** - state-change animation:

| Property | Type | Accepts |
|----------|------|---------|
| `duration` | duration | Duration value or reference |
| `delay` | duration | Duration value or reference |
| `timingFunction` | cubicBezier | Cubic Bezier value or reference |

**Typography** - complete text styling (full definition in spec section 9.8; combines font family, size, weight, line height, etc.).

**Gradient** - color gradients (full definition in spec section 9.7).

## Groups and hierarchical organization

A group is a JSON object that does NOT contain a `$value` property. Groups provide arbitrary hierarchical organization and may contain child tokens, nested groups, and group properties.

"If an object contains both `$value` and child tokens/groups, this creates an invalid structure where the object cannot be both a token and a group simultaneously. Tools _MUST_ report this as an error."

### Root tokens
Groups may include a root token using the reserved name `$root`:

```json
{
  "color": {
    "accent": {
      "$root": {
        "$type": "color",
        "$value": { "colorSpace": "srgb", "components": [0.867, 0, 0] }
      }
    }
  }
}
```

Referenced as `{color.accent.$root}`.

### Group properties

| Property | Required | Purpose |
|----------|----------|---------|
| `$description` | No | Plain text describing group purpose |
| `$type` | No | Default type for child tokens (inherited unless overridden) |
| `$extends` | No | Inherits tokens/properties from another group |
| `$deprecated` | No | Marks group and children as deprecated |
| `$extensions` | No | Vendor-specific metadata |

### Type inheritance
When a group has `$type` defined, all child tokens inherit that type unless they explicitly declare their own `$type`.

### Group extension (`$extends`)
Follows JSON Schema `$ref` semantics: `"$extends": "{group}"`.

Resolution: locate target group via reference, copy inherited tokens/properties, apply local overrides at same paths, add new local tokens/properties. Same path = local version wins (complete replacement, not property-merge). Different paths coexist.

"Groups _MUST NOT_ create circular inheritance chains." Tools must detect and error on cycles like `a -> b -> c -> a`.

Example:
```json
{
  "button-primary": {
    "$extends": "{button}",
    "background": {"$value": "#cc0066"}
  }
}
```

## Reference syntax and aliases

Two reference mechanisms exist.

### Curly brace syntax (primary token references)
Format: `{group.token}` or nested `{group.subgroup.token}`.

- Targets complete token values only; always resolves to `$value`
- Cannot access individual properties or array elements

```json
{
  "colors": {
    "blue": {
      "$value": {"colorSpace": "srgb", "components": [0, 0.4, 0.8]},
      "$type": "color"
    }
  },
  "semantic": {
    "primary": { "$value": "{colors.blue}", "$type": "color" }
  }
}
```

### JSON Pointer syntax (advanced references, RFC 6901)
Format: `"$ref": "#/path/to/target"`.

"Tools implementing this specification _MUST_ support JSON Pointer syntax."

- Accesses any document location; requires explicit full path
- Enables property-level references within composite tokens
- Supports array indexing
- Root: `#/`; object properties separated by `/`; array indices numeric (e.g. `#/color/$value/components/0`)
- Special characters escaped per RFC 6901 (`~` -> `~0`, `/` -> `~1`)

Equivalence table:

| Target | Curly Brace | JSON Pointer |
|--------|-------------|---------------|
| Complete token value | `{colors.blue}` | `#/colors/blue/$value` |
| Color hex property | Not supported | `#/colors/blue/$value/hex` |
| First component | Not supported | `#/colors/blue/$value/components/0` |
| Token type | Not supported | `#/colors/blue/$type` |

Property-level reference example:
```json
{
  "base": {
    "blue": {
      "$value": {
        "colorSpace": "srgb",
        "components": [0.2, 0.4, 0.9],
        "hex": "#3366e6"
      },
      "$type": "color"
    }
  },
  "semantic": {
    "primary": {
      "$value": {
        "colorSpace": "srgb",
        "components": [
          {"$ref": "#/base/blue/$value/components/0"},
          {"$ref": "#/base/blue/$value/components/1"},
          0.7
        ],
        "hex": "#3366b3"
      },
      "$type": "color"
    }
  }
}
```

### Chained references
Aliases may reference other aliases; tools follow chains until reaching an explicit value. Example chain: `{semantic.link}` -> `{semantic.brand}` -> `{base.primary}`.

### Circular reference detection
"References _MUST NOT_ be circular." Tools must detect and report this as an error affecting all tokens in the circular chain.

## File format specifications

- **Media type:** `application/design-tokens+json` (recommended). "Since every design token file is a valid JSON file, they _MAY_ be served using the JSON media type: `application/json`." Tools "_MUST_ support both media types."
- **File extensions:** `.tokens` (succinct) or `.tokens.json` (verbose, for JSON-editor compatibility). "Tools that can save design token files _SHOULD_ append one of the recommended file extensions to the filename when saving."
- **Format:** JSON per RFC 8259, chosen for broad standard-library support, human readability/hand-editability, and version-control friendliness.

## Reserved keywords

All properties defined by this format are prefixed with `$`: `$value`, `$type`, `$description`, `$extensions`, `$deprecated`, `$root`, `$extends`, `$ref`. "This convention will also be used for any new properties introduced by future versions of this spec."

## Conformance language
RFC 2119 keywords used throughout: MUST/MUST NOT (absolute requirement), SHOULD/SHOULD NOT (strong recommendation), MAY (optional feature).
