# lab() - CSS: Cascading Style Sheets - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/lab
- Fetched: 2026-09-15
- Source type: official docs (references CSS Color Module Level 4/5 spec)
- Last updated (if shown): August 27, 2026

## Overview

The `lab()` functional notation expresses a given color in the CIE L*a*b* color space. Lab represents the entire range of colors that humans can see by specifying the color's lightness, a red/green axis value, a blue/yellow axis value, and an optional alpha transparency value.

Status: Widely available since May 2023 (Baseline feature).

## Syntax

### Absolute values
```css
lab(L a b [ / A])
lab(29.2345% 39.3825 20.0664);
lab(52.2345% 40.1645 59.9971);
lab(52.2345% 40.1645 59.9971 / .5);
```

### Relative values
```css
lab(from <color> L a b [ / A])
lab(from green l a b / 0.5)
lab(from #123456 calc(l + 10) a b)
lab(from hsl(180 100% 50%) calc(l - 10) a b)
```

## Parameter definitions

### Absolute syntax: `lab(L a b [ / A])`

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| **L** (Lightness) | `<number>` \| `<percentage>` \| `none` | 0-100 / 0%-100% | Specifies the color's lightness. 0 = black, 100 = white |
| **a** (Red/Green) | `<number>` \| `<percentage>` \| `none` | -125 to 125 / -100% to 100% | Distance along the a-axis. Negative = green, positive = red. In practice, values cannot exceed +-160 |
| **b** (Blue/Yellow) | `<number>` \| `<percentage>` \| `none` | -125 to 125 / -100% to 100% | Distance along the b-axis. Negative = blue, positive = yellow. In practice, values cannot exceed +-160 |
| **A** (Alpha) | `<alpha-value>` \| `none` | 0-1 (Optional) | Alpha channel. 0 = fully transparent, 1 = fully opaque. Defaults to 100% if omitted |

### Relative syntax: `lab(from <color> L a b [ / A])`

Channel values resolve as: **l**: `<number>` between 0-100; **a** and **b**: `<number>` between -125 to 125; **alpha**: `<number>` between 0-1.

## Formal syntax

```
<lab()> = lab( [from <color>]? [<percentage> | <number> | none] [<percentage> | <number> | none] [<percentage> | <number> | none] [/ [<alpha-value> | none]]? )
```

## Usage examples

### Adjusting lightness
```css
[data-color="red-dark"] {
  background-color: lab(5 125 71);      /* Very dark red */
}
[data-color="red"] {
  background-color: lab(40 125 71);     /* Medium red */
}
[data-color="red-light"] {
  background-color: lab(95 125 71);     /* Very light red */
}
```

### Adjusting color axes
```css
[data-color="red-yellow"] {
  background-color: lab(50 125 125);    /* Red-yellow */
}
[data-color="red-blue"] {
  background-color: lab(50 125 -125);   /* Red-blue */
}
[data-color="green-yellow"] {
  background-color: lab(50 -125 125);   /* Green-yellow */
}
```

### Linear gradients
```css
[data-color="red-to-green-yellow"] {
  background-image: linear-gradient(to right, lab(50 125 125), lab(50 -125 125));
}
```

### Adjusting opacity
```css
[data-color="red"] {
  background-color: lab(80 125 125);        /* Fully opaque */
}
[data-color="red-alpha"] {
  background-color: lab(80 125 125 / 0.4);  /* 40% opaque */
}
```

### Relative colors with calc()
```css
:root {
  --base-color: orange;
}

#one {
  background-color: lab(from var(--base-color) calc(l + 15) a b);  /* Lighten by 15 */
}
#two {
  background-color: var(--base-color);
}
#three {
  background-color: lab(from var(--base-color) calc(l - 15) a b);  /* Darken by 15 */
}
```

## Key notes

1. Percentage-to-number mapping: for **L**, 100% = 100; for **a** and **b**, 100% = 125, -100% = -125.
2. Missing color components: `none` defaults to 0% in absolute mode; for relative colors, `none` uses the origin color's value.
3. Theoretical vs. practical bounds: a/b values are theoretically unbounded but practically cannot exceed +-160.
4. Alpha channel: if not specified in relative colors, defaults to the origin color's alpha value.

## Specifications

- CSS Color Module Level 5: Relative Lab colors - https://drafts.csswg.org/css-color-5/#relative-Lab
- CSS Color Module Level 4: Lab colors - https://drafts.csswg.org/css-color/#lab-colors
