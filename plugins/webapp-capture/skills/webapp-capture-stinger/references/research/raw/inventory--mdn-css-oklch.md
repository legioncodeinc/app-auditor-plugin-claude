# oklch() - CSS: Cascading Style Sheets - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch
- Fetched: 2026-09-15
- Source type: official docs (references CSS Color Module Level 4/5 spec)
- Last updated (if shown): August 27, 2026

## Overview

The `oklch()` functional notation expresses a given color in the Oklab color space. It is the cylindrical form of `oklab()`, using the same `L` axis, but with polar Chroma (`C`) and Hue (`h`) coordinates.

Status: Baseline, widely available across browsers since May 2023.

## Syntax

### Absolute values
```css
oklch(40.1% 0.123 21.57)
oklch(59.69% 0.156 49.77)
oklch(59.69% 0.156 49.77 / .5)
```

### Relative values
```css
oklch(from green l c h / 0.5)
oklch(from #123456 calc(l + 0.1) c h)
oklch(from hsl(180 100% 50%) calc(l - 0.1) c h)
oklch(from var(--color) l c h / calc(alpha - 0.1))
```

## Parameter definitions

### Absolute syntax: `oklch(L C H [ / A])`

| Parameter | Description |
|-----------|-------------|
| **L** (Lightness) | `<number>` (0-1) or `<percentage>` (0%-100%), or `none`. Perceived lightness/"brightness". `0` = black, `1` = white. |
| **C** (Chroma) | `<number>`, `<percentage>`, or `none`. Measures color intensity ("amount of color"). Minimum: `0`, maximum: typically `0.4` (unbounded theoretically). `0%` = `0`, `100%` = `0.4`. |
| **H** (Hue) | `<number>`, `<angle>`, or `none`. Hue angle in degrees. Default: `0deg`. Hue angles differ across color spaces (oklch, sRGB/hsl, CIELAB/lch). |
| **A** (Alpha) | `<alpha-value>` or `none` (optional). `0` = fully transparent, `1` = fully opaque. Defaults to `100%` if omitted. Preceded by `/`. |

Key note: `100%` does NOT equal `1` for chroma; instead, `100%` = `0.4`.

### Relative syntax: `oklch(from <color> L C H [ / A])`

The origin color is converted to OkLCh and provides channel values: `l` (0-1), `c` (0-0.4), `h` (0-360), `alpha` (0-1). These can be used in calculations:

```css
oklch(from hsl(0 100% 50%) calc(l + 0.2) calc(c + 0.1) calc(h - 20) / calc(alpha - 0.1))
```

## Formal syntax

```
<oklch()> = oklch( [from <color>]? [<percentage> | <number> | none] [<percentage> | <number> | none] [<hue> | none] [/ [<alpha-value> | none]]? )

<hue> = <number> | <angle>
<alpha-value> = <number> | <percentage>
```

## Examples

### Adjusting brightness (L value)
```css
[data-color="blue-dark"] {
  background-color: oklch(10% 0.4 240);
}
[data-color="blue"] {
  background-color: oklch(50% 0.4 240);
}
[data-color="blue-light"] {
  background-color: oklch(90% 0.4 240);
}
```

### Adjusting color intensity (C value)
```css
[data-color="blue"] {
  background-color: oklch(50% 0.4 240);      /* fully saturated */
}
[data-color="blue-chroma1"] {
  background-color: oklch(50% 0.2 240);      /* half saturation */
}
[data-color="blue-chroma3"] {
  background-color: oklch(50% 0.01 240);     /* nearly gray */
}
```

### Hue variations
```css
[data-color="0"] {
  background-color: oklch(50% 0.4 0deg);     /* red (magenta in oklch) */
}
[data-color="180"] {
  background-color: oklch(50% 0.4 180deg);   /* cyan */
}
[data-color="240"] {
  background-color: oklch(50% 0.4 240deg);   /* blue */
}
```

Important: in `oklch()`, `0deg` = magenta, `41deg` roughly equals red (differs from `hsl()`).

### Adjusting alpha
```css
[data-color="red"] {
  background-color: oklch(50% 0.5 20);       /* fully opaque */
}
[data-color="red-alpha"] {
  background-color: oklch(50% 0.5 20 / 0.4); /* 40% opaque */
}
```

### Using relative colors
```css
:root {
  --base-color: orange;
}

#one {
  background-color: oklch(from var(--base-color) calc(l + 0.15) c h);
  /* 15% lighter */
}

#two {
  background-color: var(--base-color);
  /* original */
}

#three {
  background-color: oklch(from var(--base-color) calc(l - 0.15) c h);
  /* 15% darker */
}
```

## Key differences from other color spaces

| Aspect | oklch() | hsl() | lch() |
|--------|---------|-------|-------|
| Color space | Oklab (cylindrical) | sRGB | CIELAB (cylindrical) |
| Red (0 degrees) | ~41 degrees | 0 degrees | ~41 degrees |
| Magenta (0 degrees) | 0 degrees | 300 degrees | ~305 degrees |
| Chroma range | 0-0.4 (practical) | N/A | Much larger |

## Specifications

- CSS Color Module Level 5 - Relative Oklch
- CSS Color Module Level 4 - Ok-lab

## Browser compatibility

Widely available across modern browsers since May 2023 (with some variations in full feature support).
