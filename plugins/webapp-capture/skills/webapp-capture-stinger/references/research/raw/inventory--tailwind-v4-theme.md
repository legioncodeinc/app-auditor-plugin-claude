# Theme variables - Tailwind CSS
- URL: https://tailwindcss.com/docs/theme
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (Tailwind CSS v4 docs)

## Overview

Theme variables are special CSS variables defined using the `@theme` directive that influence which utility classes exist in your Tailwind project. They store low-level design decisions called design tokens.

### What are theme variables?

Theme variables are CSS variables that:
- Instruct Tailwind to create new utility classes.
- Must be defined at the top level using the `@theme` directive (not nested under selectors or media queries).
- Generate both utility classes AND regular CSS variables for reference.

Example:
```css
@import "tailwindcss";

@theme {
  --color-mint-500: oklch(0.72 0.11 178);
}
```

This creates utilities like `bg-mint-500`, `text-mint-500`, and `fill-mint-500`, plus a CSS variable `var(--color-mint-500)` you can reference directly.

### Why `@theme` instead of `:root`?

Theme variables do more than regular CSS variables, they create utility classes. Use `@theme` for design tokens that map to utility classes, and `:root` for regular CSS variables that shouldn't have corresponding utilities.

## Theme variable namespaces

Theme variables are organized in namespaces. Each namespace maps to utility classes or variants:

| Namespace | Utility classes |
|-----------|-----------------|
| `--color-*` | Color utilities (`bg-red-500`, `text-sky-300`, etc.) |
| `--font-*` | Font family utilities (`font-sans`, `font-serif`) |
| `--text-*` | Font size utilities (`text-xl`) |
| `--font-weight-*` | Font weight utilities (`font-bold`) |
| `--tracking-*` | Letter spacing utilities (`tracking-wide`) |
| `--leading-*` | Line height utilities (`leading-tight`) |
| `--breakpoint-*` | Responsive variants (`sm:*`, `md:*`) |
| `--spacing-*` | Spacing/sizing utilities (`px-4`, `max-h-16`) |
| `--radius-*` | Border radius utilities (`rounded-sm`) |
| `--shadow-*` | Box shadow utilities (`shadow-md`) |
| `--blur-*` | Blur filter utilities (`blur-md`) |
| `--animate-*` | Animation utilities (`animate-spin`) |
| `--ease-*` | Timing functions (`ease-out`) |
| `--aspect-*` | Aspect ratios (`aspect-video`) |

## Relationship to utility classes

Most utility classes are driven by theme variables. For example, default font utilities exist because of these theme variables:

```css
@theme {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
```

Add a new font variable to create a new utility:
```css
@import "tailwindcss";

@theme {
  --font-poppins: Poppins, sans-serif;
}
```

```html
<h1 class="font-poppins">This headline will use Poppins.</h1>
```

## Relationship to variants

Some theme variables define variants rather than utilities:

```css
@import "tailwindcss";

@theme {
  --breakpoint-3xl: 120rem;
}
```

```html
<div class="3xl:grid-cols-6 grid grid-cols-2 md:grid-cols-4">
  <!-- ... -->
</div>
```

## Customizing your theme

### Extending the default theme
```css
@import "tailwindcss";

@theme {
  --font-script: Great Vibes, cursive;
}
```
```html
<p class="font-script">This will use the Great Vibes font family.</p>
```

### Overriding the default theme
```css
@import "tailwindcss";

@theme {
  --breakpoint-sm: 30rem;
}
```
Now `sm:*` triggers at 30rem instead of 40rem.

### Completely replace a namespace
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
This removes all default color utilities and only provides the custom ones.

### Using a complete custom theme
```css
@import "tailwindcss";

@theme {
  --*: initial;
  --spacing: 4px;
  --font-body: Inter, sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
  --color-driftwood: oklch(0.79 0.06 74.59);
  --color-tide: oklch(0.49 0.08 205.88);
  --color-dusk: oklch(0.82 0.15 72.09);
}
```

### Defining animation keyframes
```css
@import "tailwindcss";

@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;

  @keyframes fade-in-scale {
    0% {
      opacity: 0;
      transform: scale(0.95);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
}
```

### Referencing other variables
```css
@import "tailwindcss";

@theme inline {
  --font-sans: var(--font-inter);
}
```
This prevents CSS variable resolution issues by using the variable's value directly in utilities.

### Generating all CSS variables
```css
@import "tailwindcss";

@theme static {
  --color-primary: var(--color-red-500);
  --color-secondary: var(--color-blue-500);
}
```
By default, only used CSS variables are generated; `static` always generates all variables.

### Sharing across projects

`./packages/brand/theme.css`:
```css
@theme {
  --*: initial;
  --spacing: 4px;
  --font-body: Inter, sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
  --color-driftwood: oklch(0.79 0.06 74.59);
  --color-tide: oklch(0.49 0.08 205.88);
  --color-dusk: oklch(0.82 0.15 72.09);
}
```

`./packages/admin/app.css`:
```css
@import "tailwindcss";
@import "../brand/theme.css";
```
Works in monorepos or npm packages.

## Using your theme variables

All theme variables compile to regular CSS variables on `:root`:
```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --color-red-50: oklch(0.971 0.013 17.38);
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  /* ... */
}
```

### With custom CSS
```css
@import "tailwindcss";

@layer components {
  .typography {
    p {
      font-size: var(--text-base);
      color: var(--color-gray-700);
    }
    h1 {
      font-size: var(--text-2xl);
      font-weight: var(--font-weight-semibold);
      color: var(--color-gray-950);
    }
    h2 {
      font-size: var(--text-xl);
      font-weight: var(--font-weight-semibold);
      color: var(--color-gray-950);
    }
  }
}
```

### With arbitrary values
```html
<div class="relative rounded-xl">
  <div class="absolute inset-px rounded-[calc(var(--radius-xl)-1px)]">
    <!-- ... -->
  </div>
</div>
```

### Referencing in JavaScript
```javascript
let styles = getComputedStyle(document.documentElement);
let shadow = styles.getPropertyValue("--shadow-xl");
```

Or directly with animation libraries like Motion:
```jsx
<motion.div animate={{ backgroundColor: "var(--color-blue-500)" }} />
```

## Default theme variables

Importing `tailwindcss` includes default theme variables for colors, typography, shadows, spacing, breakpoints, and animations, providing hundreds of pre-configured variables across all namespaces above.
