# Colors - Tailwind CSS
- URL: https://tailwindcss.com/docs/colors
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (Tailwind CSS v4 docs)

## Overview

Tailwind CSS includes a large default color palette with 11 steps per color (50 being lightest, 950 being darkest). Colors are expressed in OKLCH format and exposed as CSS variables in the `--color-*` namespace.

## Default color palette

26 color families:
- Reds/Pinks: red, orange, amber, yellow, pink, rose
- Greens: lime, green, emerald, teal
- Blues/Purples: cyan, sky, blue, indigo, violet, purple
- Neutrals: slate, gray, zinc, neutral, stone
- Additional: mauve, mist, olive, taupe, fuchsia
- Core: black, white

Each color has 11 shades (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950).

## OKLCH color values

All colors use OKLCH format. Example for the `sky` color:

```css
--color-sky-50: oklch(97.7% 0.013 236.62);
--color-sky-100: oklch(95.1% 0.026 236.824);
--color-sky-200: oklch(90.1% 0.058 230.902);
--color-sky-300: oklch(82.8% 0.111 230.318);
--color-sky-400: oklch(74.6% 0.16 232.661);
--color-sky-500: oklch(68.5% 0.169 237.323);
--color-sky-600: oklch(58.8% 0.158 241.966);
--color-sky-700: oklch(50% 0.134 242.749);
--color-sky-800: oklch(44.3% 0.11 240.79);
--color-sky-900: oklch(39.1% 0.09 240.876);
--color-sky-950: oklch(29.3% 0.066 243.157);
```

Also shown for `red` and `blue`:
```css
@theme {
  --color-red-50: oklch(97.1% 0.013 17.38);
  --color-red-100: oklch(93.6% 0.032 17.717);
  /* ... continues through red-950 */

  --color-blue-50: oklch(97% 0.014 254.604);
  /* ... continues through blue-950 */

  /* Plus 24 other complete color families */

  --color-black: #000;
  --color-white: #fff;
}
```

## Using color utilities

| Utility | Description |
|---------|-------------|
| `bg-*` | Background color |
| `text-*` | Text color |
| `decoration-*` | Text decoration color |
| `border-*` | Border color |
| `outline-*` | Outline color |
| `shadow-*` | Box shadow color |
| `inset-shadow-*` | Inset box shadow color |
| `ring-*` | Ring shadow color |
| `inset-ring-*` | Inset ring shadow color |
| `accent-*` | Form control accent color |
| `caret-*` | Text input caret color |
| `scrollbar-thumb-*` | Scrollbar thumb color |
| `scrollbar-track-*` | Scrollbar track color |
| `fill-*` | SVG fill color |
| `stroke-*` | SVG stroke color |

### Example usage
```html
<div class="flex items-center gap-4 rounded-lg bg-white p-6 shadow-md outline outline-black/5 dark:bg-gray-800">
  <span class="inline-flex shrink-0 rounded-full border border-pink-300 bg-pink-100 p-2 dark:border-pink-300/10 dark:bg-pink-400/10">
    <svg class="size-6 stroke-pink-700 dark:stroke-pink-500"><!-- ... --></svg>
  </span>
  <div>
    <p class="text-gray-700 dark:text-gray-400">
      <span class="font-medium text-gray-950 dark:text-white">Tom Watson</span> mentioned you in
      <span class="font-medium text-gray-950 dark:text-white">Logo redesign</span>
    </p>
    <time class="mt-1 block text-gray-500" datetime="9:37">9:37am</time>
  </div>
</div>
```

## Adjusting opacity

Use the `/` syntax with opacity values (10-100):
```html
<div>
  <div class="bg-sky-500/10"></div>
  <div class="bg-sky-500/20"></div>
  <div class="bg-sky-500/30"></div>
  <div class="bg-sky-500/40"></div>
  <div class="bg-sky-500/50"></div>
  <div class="bg-sky-500/60"></div>
  <div class="bg-sky-500/70"></div>
  <div class="bg-sky-500/80"></div>
  <div class="bg-sky-500/90"></div>
  <div class="bg-sky-500/100"></div>
</div>
```

Supports arbitrary values and CSS variables:
```html
<div class="bg-pink-500/[71.37%]"><!-- ... --></div>
<div class="bg-cyan-400/(--my-alpha-value)"><!-- ... --></div>
```

## Dark mode

Use the `dark` variant for dark mode colors:
```html
<div class="bg-white dark:bg-gray-800 rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
  <div>
    <span class="inline-flex items-center justify-center rounded-md bg-indigo-500 p-2 shadow-lg">
      <svg class="h-6 w-6 stroke-white" ...><!-- ... --></svg>
    </span>
  </div>
  <h3 class="text-gray-900 dark:text-white mt-5 text-base font-medium tracking-tight">Writes upside-down</h3>
  <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm">
    The Zero Gravity Pen can be used to write in any orientation, including upside-down. It even works in outer space.
  </p>
</div>
```

## Referencing colors in CSS

Colors are exposed as CSS variables in the `--color-*` namespace:
```css
@import "tailwindcss";

@layer components {
  .typography {
    color: var(--color-gray-950);
    a {
      color: var(--color-blue-500);
      &:hover {
        color: var(--color-blue-800);
      }
    }
  }
}
```

### Using as arbitrary values
```html
<div class="bg-[light-dark(var(--color-white),var(--color-gray-950))]">
  <!-- ... -->
</div>
```

### The `--alpha()` function
```css
@import "tailwindcss";

@layer components {
  .DocSearch-Hit--Result {
    background-color: --alpha(var(--color-gray-950) / 10%);
  }
}
```

## Customizing colors

### Adding custom colors
```css
@import "tailwindcss";

@theme {
  --color-midnight: #121063;
  --color-tahiti: #3ab7bf;
  --color-bermuda: #78dcca;
}
```
Enables `bg-midnight`, `text-tahiti`, `fill-bermuda`.

### Overriding default colors
```css
@import "tailwindcss";

@theme {
  --color-gray-50: oklch(0.984 0.003 247.858);
  --color-gray-100: oklch(0.968 0.007 247.896);
  --color-gray-200: oklch(0.929 0.013 255.508);
  --color-gray-300: oklch(0.869 0.022 252.894);
  --color-gray-400: oklch(0.704 0.04 256.788);
  --color-gray-500: oklch(0.554 0.046 257.417);
  --color-gray-600: oklch(0.446 0.043 257.281);
  --color-gray-700: oklch(0.372 0.044 257.287);
  --color-gray-800: oklch(0.279 0.041 260.031);
  --color-gray-900: oklch(0.208 0.042 265.755);
  --color-gray-950: oklch(0.129 0.042 264.695);
}
```

### Disabling default colors
```css
@import "tailwindcss";

@theme {
  --color-lime-*: initial;
  --color-fuchsia-*: initial;
}
```

### Creating a custom palette
```css
@import "tailwindcss";

@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-purple: #3f3cbb;
  --color-midnight: #121063;
  --color-tahiti: #3ab7bf;
  --color-bermuda: #78dcca;
}
```

### Referencing other variables
```css
@import "tailwindcss";

:root {
  --acme-canvas-color: oklch(0.967 0.003 264.542);
}

[data-theme="dark"] {
  --acme-canvas-color: oklch(0.21 0.034 264.665);
}

@theme inline {
  --color-canvas: var(--acme-canvas-color);
}
```
