# oklab() - CSS: Cascading Style Sheets - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklab
- Fetched: 2026-09-15
- Source type: official docs (references CSS Color Module Level 4/5 spec)
- Last updated (if shown): August 27, 2026

## Overview

The `oklab()` functional notation expresses a color in the Oklab color space, which attempts to mimic how color is perceived by the human eye. It is a perceptual color space useful for: converting images to grayscale without changing lightness, modifying color saturation while preserving hue and lightness perception, and creating smooth, uniform color gradients.

Baseline support: Widely available since May 2023.

## Syntax

### Absolute values
```css
oklab(40.1% 0.1143 0.045);
oklab(59.69% 0.1007 0.1191);
oklab(59.69% 0.1007 0.1191 / 0.5);
```

### Relative values
```css
oklab(from green l a b / 0.5)
oklab(from #123456 calc(l + 0.1) a b / calc(alpha * 0.9))
oklab(from hsl(180 100% 50%) calc(l - 0.1) a b)
```

## Parameter definitions

### Absolute syntax: `oklab(L a b [ / A])`

| Parameter | Range | Description |
|-----------|-------|-------------|
| **L** | 0-1 or 0%-100% | Perceived lightness. `0` = black, `1` = white |
| **a** | -0.4 to 0.4 or -100% to 100% | Distance along a-axis: negative = green, positive = red |
| **b** | -0.4 to 0.4 or -100% to 100% | Distance along b-axis: negative = blue, positive = yellow |
| **A** (optional) | 0-1 or 0%-100% | Alpha channel (opacity). Defaults to 100% if omitted |

Note: the `a` and `b` values are theoretically unbounded but practically cannot exceed +-0.5.

### Relative syntax: `oklab(from <color> L a b [ / A])`

- `from <color>`: origin color (any valid `<color>` syntax, including other relative colors)
- Channel values: can use absolute values, `none`, or `calc()` expressions
- Default alpha: if output alpha isn't specified, it inherits from the origin color

## Formal syntax

```
<oklab()> = oklab( [from <color>]? [<percentage> | <number> | none] [<percentage> | <number> | none] [<percentage> | <number> | none] [/ [<alpha-value> | none]]? )

<alpha-value> = <number> | <percentage>
```

## Examples

### Adjusting lightness
```css
[data-color="red-dark"] {
  background-color: oklab(0.05 0.4 0.4);
}
[data-color="red"] {
  background-color: oklab(0.5 0.4 0.4);
}
[data-color="red-light"] {
  background-color: oklab(0.95 0.4 0.4);
}
```

### Adjusting opacity
```css
[data-color="red"] {
  background-color: oklab(0.628 0.225 0.126);
}
[data-color="red-alpha"] {
  background-color: oklab(0.628 0.225 0.126 / 0.4);
}
```

### Linear gradients
```css
[data-color="red-to-green-yellow"] {
  background-image: linear-gradient(to right, oklab(50% 0.4 0.4), oklab(50% -0.4 0.4));
}
[data-color="yellow-to-blue-zero"] {
  background-image: linear-gradient(to right, oklab(50% 0 0.4), oklab(50% 0 -0.4));
}
```

### Using relative colors
```css
:root {
  --base-color: orange;
}

#one {
  background-color: oklab(from var(--base-color) calc(l + 0.15) a b);
}

#two {
  background-color: var(--base-color);
}

#three {
  background-color: oklab(from var(--base-color) calc(l - 0.15) a b);
}
```

## Key characteristics

- Cartesian coordinate system with a- and b-axes (use `oklch()` for polar hue/chroma).
- Wide color gamut: represents more colors than RGB, including P3 colors.
- Perceptually uniform: changes in color values correspond to perceived changes.
- Missing components: the `none` keyword can specify missing channels.

## Related functions

- `lab()` - similar perceptual color space
- `oklch()` - polar coordinate version of oklab
- Using relative colors (MDN guide)

## Specifications

CSS Color Module Level 4 and Level 5.
