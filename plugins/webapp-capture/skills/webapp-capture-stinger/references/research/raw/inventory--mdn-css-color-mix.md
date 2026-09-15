# color-mix() - CSS: Cascading Style Sheets - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix
- Fetched: 2026-09-15
- Source type: official docs (references CSS Color Module Level 5 spec)
- Last updated (if shown): September 6, 2026

## Overview

The `color-mix()` functional notation mixes one or more `<color>` values in a given colorspace by specified amounts, returning the blended result. Widely available since May 2023.

## Syntax

```css
/* Polar color space */
color-mix(in hsl, hsl(200 50 80), coral)
color-mix(in hsl, hsl(200 50 80) 20%, coral 80%)

/* Rectangular color space */
color-mix(in srgb, plum, #123456)
color-mix(in lab, plum 60%, #123456 50%)

/* With hue interpolation method */
color-mix(in lch increasing hue, hsl(200deg 50% 80%), coral)
color-mix(in lch longer hue, hsl(200deg 50% 80%) 44%, coral 16%)

/* With a color argument list */
color-mix(in oklab, teal)
color-mix(in oklab, teal 20%, olive 30%, blue 50%)
color-mix(in oklab, teal, olive, blue, purple)
```

## Parameters

### `<color-interpolation-method>` (optional)
Syntax: `in <color-space> [<hue-interpolation-method>]?`

Rectangular color spaces: `srgb`, `srgb-linear`, `display-p3`, `display-p3-linear`, `a98-rgb`, `prophoto-rgb`, `rec2020`, `lab`, `oklab`, `xyz`, `xyz-d50`, `xyz-d65`.

Polar color spaces: `hsl`, `hwb`, `lch`, `oklch` - with optional hue interpolation: `shorter hue` (default), `longer hue`, `increasing hue`, `decreasing hue`.

Default: `oklab` with `shorter hue`.

### `<color>`
Any valid `<color>` value (named colors, hex, `rgb()`, `hsl()`, etc.)

### `<percentage>` (optional)
Value between `0%` and `100%` specifying the amount of the corresponding color to mix.

## Percentage normalization

When two colors are mixed:

1. Both omitted: `p1 = p2 = 50%`.
2. One omitted: the other is subtracted from 100%.
3. Sum != 100%: both percentages are normalized: `p1' = p1 / (p1 + p2)`, `p2' = p2 / (p1 + p2)`.
4. Sum < 100%: an alpha multiplier of `(p1 + p2)` is applied to the result (equivalent to mixing with transparent).
5. Both = 0%: invalid function.

## Formal syntax

```
<color-mix()> = color-mix( <color-interpolation-method>?, , [<color> && <percentage [0,100]>?]# )

<color-interpolation-method> = in [ <rectangular-color-space> | <polar-color-space> <hue-interpolation-method>? | <custom-color-space> ]

<hue-interpolation-method> = [ shorter | longer | increasing | decreasing ] hue
```

## Color space selection guide

- Linear light intensity mixing: `xyz`, `srgb-linear`.
- Perceptually uniform (gradients): `oklab`, `lab`.
- Maximum chroma (avoid graying): `oklch`, `lch`.
- Avoid: `srgb` (neither linear nor perceptually uniform).

## Examples

### Mixing two colors with percentages
```css
li:nth-child(1) { background-color: color-mix(in oklab, #a71e14 0%, white); }
li:nth-child(2) { background-color: color-mix(in oklab, #a71e14 25%, white); }
li:nth-child(3) { background-color: color-mix(in oklab, #a71e14 50%, white); }
li:nth-child(4) { background-color: color-mix(in oklab, #a71e14 75%, white); }
li:nth-child(5) { background-color: color-mix(in oklab, #a71e14 100%, white); }
li:nth-child(6) { background-color: color-mix(in oklab, #a71e14, white); /* defaults to 50/50 */ }
```

### Mixing multiple colors
```css
li:nth-child(1) { background-color: color-mix(in oklab, teal); }
li:nth-child(2) { background-color: color-mix(in oklab, teal 20%, olive 30%, blue 50%); }
li:nth-child(3) { background-color: color-mix(in oklab, teal, olive, blue, purple); /* 25% each */ }
```

### Adding transparency
```css
:root { --base: red; }

li:nth-child(1) { background-color: color-mix(in srgb, var(--base) 0%, transparent); }
li:nth-child(2) { background-color: color-mix(in srgb, var(--base) 25%, transparent); }
li:nth-child(3) { background-color: color-mix(in srgb, var(--base) 50%, transparent); }
li:nth-child(6) { background-color: color-mix(in srgb, var(--base), transparent); /* 50% opacity */ }
```

### Hue interpolation methods
```css
/* Shorter path around color wheel (default, 20deg increments) */
color-mix(in lch shorter hue, red 100%, blue 0%)

/* Longer path around color wheel (52deg increments) */
color-mix(in lch longer hue, red 100%, blue 0%)

/* Always increase hue (40deg increments) */
color-mix(in lch increasing hue, yellow 100%, blue 0%)

/* Always decrease hue (32deg decrements) */
color-mix(in lch decreasing hue, yellow 100%, blue 0%)
```

### Default behavior
These three declarations are equivalent:
```css
background-color: color-mix(red, blue);
background-color: color-mix(in oklab, red, blue);
background-color: color-mix(in oklab shorter hue, red, blue);
```

## Browser compatibility

Widely available across major browsers since May 2023. Some advanced features (like color lists) may have varying support levels.

## Specifications

CSS Color Module Level 5: https://drafts.csswg.org/css-color-5/#color-mix
