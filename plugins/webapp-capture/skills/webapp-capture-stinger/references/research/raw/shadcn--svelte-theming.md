# shadcn-svelte: Theming

- URL: https://shadcn-svelte.com/docs/theming
- Fetched: 2026-09-15
- Source type: official docs (raw Markdown transcribed from `huntabyte/shadcn-svelte`, `docs/content/theming.md`, `main` branch, first 220 of 530 lines transcribed) plus `docs/content/cli.md` and `docs/content/components-json.md` for CLI/config cross-reference
- Last updated (if shown): unknown

## Summary

shadcn-svelte uses the same CSS-variable theming approach as shadcn/ui: a `background`/`foreground` convention (`background` suffix omitted on the base token, e.g. `primary` pairs with `primary-foreground`), and Tailwind utilities like `bg-primary text-primary-foreground` map to those variables:

```css
--primary: oklch(0.205 0 0);
--primary-foreground: oklch(0.985 0 0);
```

```svelte
<div class="bg-primary text-primary-foreground">Hello</div>
```

## Color format: OKLCH (same as shadcn/ui)

shadcn-svelte's current default theme scaffold also uses raw OKLCH values (`oklch(1 0 0)`, `oklch(0.205 0 0)`, etc.), matching shadcn/ui's move away from HSL-wrapped variables.

## List of variables (default `neutral`-equivalent theme, light and dark)

```css title="src/routes/layout.css" showLineNumbers
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
  --popover: oklch(0.269 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.371 0 0);
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
  --sidebar-ring: oklch(0.439 0 0);
}
```

Same token set as shadcn/ui: `background`/`foreground`, `card`, `popover`, `primary`, `secondary`, `muted`, `accent`, `destructive`, `border`, `input`, `ring`, `chart-1..5`, `sidebar` and `sidebar-*`, `radius`.

## Value differences found versus the current shadcn/ui default scaffold

Comparing this scaffold token-for-token against the shadcn/ui React default (`shadcn--theming.md`), two small numeric differences were found in the dark theme:

| Token | shadcn/ui (React) dark value | shadcn-svelte dark value |
| --- | --- | --- |
| `.dark --popover` | `oklch(0.205 0 0)` | `oklch(0.269 0 0)` |
| `.dark --accent` | `oklch(0.269 0 0)` | `oklch(0.371 0 0)` |
| `.dark --sidebar-ring` | `oklch(0.556 0 0)` | `oklch(0.439 0 0)` |

All other tokens (light and dark) matched exactly at fetch time. This suggests shadcn-svelte's default theme has drifted slightly from the React scaffold's most recent dark-mode color revision (see the "March 12, 2025: New dark mode colors" changelog entry in `shadcn--tailwind-v4.md`) rather than a deliberate design difference; treat these three values as a possible version-lag indicator when comparing a captured app's tokens against "canonical" shadcn values.

## Adding new colors (same pattern as shadcn/ui)

```css title="src/routes/layout.css" showLineNumbers
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

```svelte
<div class="bg-warning text-warning-foreground"></div>
```

## Base colors: enum lag versus shadcn/ui

`docs/content/components-json.md` (shadcn-svelte's `components.json` reference) documents `tailwind.baseColor` as:

```json title="components.json"
{
  "tailwind": {
    "baseColor": "gray" | "neutral" | "slate" | "stone" | "zinc"
  }
}
```

This is the **older, five-color** base color set (`gray`, `neutral`, `slate`, `stone`, `zinc`). The shadcn-svelte CLI's own `init` help (`docs/content/cli.md`) shows a **different, newer** seven-color set matching the current shadcn/ui React enum:

```
--base-color <name>        the base color for the components (choices: "neutral", "stone", "zinc", "mauve", "olive", "mist", "taupe")
```

So at fetch time, shadcn-svelte's `components.json` reference page (`gray`/`neutral`/`slate`/`stone`/`zinc`) is stale relative to its own CLI's `init --base-color` choices (`neutral`/`stone`/`zinc`/`mauve`/`olive`/`mist`/`taupe`), and neither matches exactly: the CLI has already adopted `mauve`/`olive`/`mist`/`taupe` (dropping `gray` and `slate`) to track shadcn/ui's React base-color set (see `shadcn--theming.md`), but the `components.json` doc page had not yet been updated to reflect it. Also note: the `init` interactive prompt example on the CLI page still shows `Which base color would you like to use? › Slate` as its example answer, reinforcing that `slate` was very recently still a live default even though it is now absent from `init`'s own `--base-color` choices list.

## Sidebar-specific CSS variables: separate manual step

Unlike the main theme scaffold (installed automatically by `init`), the Sidebar component's docs (`docs/content/components/sidebar.md`) show the `--sidebar*` variables being added as an explicit **second step** after running `npx shadcn-svelte@latest add sidebar`, i.e. the CLI add step for `sidebar` is documented as requiring the developer to manually paste the sidebar color block into their CSS file, rather than the CLI writing it automatically:

```css title="src/routes/layout.css"
:root {
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
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.439 0 0);
}
```

(Note these sidebar-only values match the "value differences" table above for `--sidebar-ring` dark: `oklch(0.439 0 0)`, confirming it is the intentional current shadcn-svelte value, not a typo, and is simply out of sync with shadcn/ui React's `oklch(0.556 0 0)`.)

## CLI package name difference (cross-reference)

The theming/config pages above are served by the `shadcn-svelte` CLI package (`npx shadcn-svelte@latest init`), a separate package from React's `shadcn` CLI. `components.json`'s `$schema` also points at a Svelte-specific schema URL: `https://shadcn-svelte.com/schema.json` (vs React's `https://ui.shadcn.com/schema.json`). See `shadcn--svelte-components-index.md` for more naming/API differences.
