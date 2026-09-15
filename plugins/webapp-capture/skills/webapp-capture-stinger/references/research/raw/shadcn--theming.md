# Theming

- URL: https://ui.shadcn.com/docs/theming
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/(root)/theming.mdx`, `main` branch)
- Last updated (if shown): unknown (no date shown on page; content reflects the current site as of fetch)

## Summary

shadcn/ui uses CSS variables for theming: semantic theme tokens like `background`, `foreground`, and `primary` that components consume by default. Overriding the tokens in CSS restyles the app without touching component classes.

```tsx
<div className="bg-background text-foreground" />
```

To use CSS variables for theming, set `tailwind.cssVariables` to `true` in `components.json` (this is the default):

```json title="components.json"
{
  "style": "base-nova",
  "rsc": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  }
}
```

Tailwind maps these tokens into utilities like `bg-background`, `text-foreground`, `border-border`, and `ring-ring`. Dark mode works by overriding the same tokens inside a `.dark` selector.

## Token convention

shadcn/ui uses semantic background/foreground pairs. The base token controls the surface color; the `-foreground` token controls the text/icon color that sits on that surface. The word "background" is omitted from the base token's own name (e.g. `primary` pairs with `primary-foreground`, not `primary-background`).

Example:

```css
--primary: oklch(0.205 0 0);
--primary-foreground: oklch(0.985 0 0);
```

```tsx
<div className="bg-primary text-primary-foreground">Hello</div>
```

## Theme tokens (full table, as documented)

These tokens live under `:root` and `.dark` in the project's CSS file.

| Token | What it controls | Used by |
| --- | --- | --- |
| `background` / `foreground` | The default app background and text color. | The page shell, page sections, and default text. |
| `card` / `card-foreground` | Elevated surfaces and the content inside them. | `Card`, dashboard panels, settings panels. |
| `popover` / `popover-foreground` | Floating surfaces and the content inside them. | `Popover`, `DropdownMenu`, `ContextMenu`, and other overlays. |
| `primary` / `primary-foreground` | High-emphasis actions and brand surfaces. | Default `Button`, selected states, badges, and active accents. |
| `secondary` / `secondary-foreground` | Lower-emphasis filled actions and supporting surfaces. | Secondary buttons, secondary badges, and supporting UI. |
| `muted` / `muted-foreground` | Subtle surfaces and lower-emphasis content. | Descriptions, placeholders, empty states, helper text, and subdued surfaces. |
| `accent` / `accent-foreground` | Interactive hover, focus, and active surfaces. | Ghost buttons, menu highlight states, hovered rows, and selected items. |
| `destructive` | Destructive actions and error emphasis. | Destructive buttons, invalid states, and destructive menu items. |
| `border` | Default borders and separators. | Cards, menus, tables, separators, and layout dividers. |
| `input` | Form control borders and input surface treatment. | `Input`, `Textarea`, `Select`, and outline-style controls. |
| `ring` | Focus rings and outlines. | Buttons, inputs, checkboxes, menus, and other focusable controls. |
| `chart-1` ... `chart-5` | The default chart palette. | Charts and chart-driven dashboard blocks. |
| `sidebar` / `sidebar-foreground` | The base sidebar surface and default sidebar text. | The `Sidebar` container and its default content. |
| `sidebar-primary` / `sidebar-primary-foreground` | High-emphasis actions inside the sidebar. | Active items, icon tiles, badges, and sidebar CTAs. |
| `sidebar-accent` / `sidebar-accent-foreground` | Hover and selected states inside the sidebar. | Sidebar menu hover states, open items, and interactive rows. |
| `sidebar-border` | Sidebar-specific borders and separators. | Sidebar headers, groups, and internal dividers. |
| `sidebar-ring` | Sidebar-specific focus rings. | Focused controls inside the sidebar. |
| `radius` | The base corner radius scale. | Cards, inputs, buttons, popovers, and the derived `radius-*` tokens. |

Note: `destructive` in this current table has no listed `destructive-foreground` row (the `default` default theme CSS below does define usage against `destructive-foreground` conventions elsewhere in the codebase; the docs table itself only lists `destructive`).

The chart tokens are covered in more detail in the Chart component's theming docs (`/docs/components/chart#theming`).

## Radius scale

`--radius` is the base radius token. A small scale is derived from it:

```css title="app/globals.css" showLineNumbers
@theme inline {
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);
}
```

- `radius-lg` is the base value.
- Smaller radii scale down from `--radius`.
- Larger radii scale up from `--radius`.
- Changing `--radius` updates the entire scale.

## Adding new tokens

Define under `:root` and `.dark`, then expose to Tailwind with `@theme inline`:

```css title="app/globals.css" showLineNumbers
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}

.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}

@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

Then use `bg-warning` and `text-warning-foreground` in components.

## Base colors

`tailwind.baseColor` controls the default token values generated for a project on `init` or via a preset.

**Available base colors (as currently documented): Neutral, Stone, Zinc, Mauve, Olive, Mist, and Taupe.**

This is a broader list than the historically well-known five (`neutral`, `gray`, `zinc`, `stone`, `slate`); as of this fetch the docs page no longer lists `gray` or `slate` and instead lists `Mauve`, `Olive`, `Mist`, `Taupe` as newer additions alongside `Neutral`, `Stone`, `Zinc`. (The CLI's `components.json` schema, see `shadcn--components-json.md`, confirms the enum: `"neutral" | "stone" | "zinc" | "mauve" | "olive" | "mist" | "taupe"`.)

## Color format: OKLCH

All values in the default theme scaffold are OKLCH, e.g. `oklch(1 0 0)`, `oklch(0.205 0 0)`, `oklch(0.577 0.245 27.325)`. The Tailwind v4 migration notes ("HSL colors are now converted to OKLCH") confirm the project moved from HSL-wrapped variables to raw OKLCH values as part of the Tailwind v4 upgrade.

## Full default theme CSS (`neutral` base color, light and dark)

```css showLineNumbers title="app/globals.css"
@import "tailwindcss";
@import "shadcn/tailwind.css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);
}

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.556 0 0);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }

  body {
    @apply bg-background text-foreground;
  }
}
```

Note: this current default scaffold imports `@import "shadcn/tailwind.css";` (a package providing shared Tailwind v4 utilities/animations, see `shadcn--cli.md`'s `eject` command) in addition to `@import "tailwindcss";`. This is new relative to earlier shadcn/ui versions, which did not depend on a separate `shadcn` npm package for base CSS utilities.

## Without CSS variables

The CLI can generate components with inline Tailwind color utilities instead of CSS variables:

```bash
npx shadcn@latest init --no-css-variables
```

This sets `tailwind.cssVariables` to `false` in `components.json`. Example output:

```tsx
<div className="bg-zinc-950 text-zinc-50 dark:bg-white dark:text-zinc-950" />
```

This is an installation-time choice; switching an existing project requires deleting and reinstalling components.
