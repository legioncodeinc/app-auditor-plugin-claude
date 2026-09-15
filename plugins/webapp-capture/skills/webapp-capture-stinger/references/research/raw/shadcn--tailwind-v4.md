# Tailwind v4

- URL: https://ui.shadcn.com/docs/tailwind-v4
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/(root)/tailwind-v4.mdx`, `main` branch)
- Last updated (if shown): Two dated changelog entries appear at the bottom of the page: "March 19, 2025" and "March 12, 2025" (see Changelog section below). No page-level "last updated" date is shown.

## What's new (per the page)

- The CLI can initialize projects with Tailwind v4.
- Full support for the `@theme` directive and `@theme inline` option.
- All components are updated for Tailwind v4 and React 19.
- `forwardRef` removed; types adjusted accordingly.
- Every primitive now has a `data-slot` attribute for styling.
- Component styles fixed and cleaned up.
- The `toast` component is deprecated in favor of `sonner`.
- Buttons now use the default cursor (`cursor: default`, not `cursor: pointer`).
- The `default` style is deprecated; new projects use `new-york`. (Note: by the time of this fetch, the CLI's own `init` help further shows `--defaults` producing `--preset=nova`, i.e. style naming has continued to evolve past `new-york` toward "nova"-suffixed presets; see `shadcn--cli.md`.)
- HSL colors are now converted to OKLCH.

**Note (verbatim):** "this is non-breaking. Your existing apps with Tailwind v3 and React 18 will still work. When you add new components, they'll still be in v3 and React 18 until you upgrade. Only new projects start with Tailwind v4 and React 19."

## Framework guides linked from this page

Next.js, Vite, Laravel, React Router, Astro, TanStack Start, Gatsby, Manual (React).

## Upgrading an existing project

**Important (per page callout):** Before upgrading, read the Tailwind v4 Compatibility docs (https://tailwindcss.com/docs/compatibility). Tailwind v4 uses bleeding-edge browser features and targets modern browsers.

Because shadcn/ui ships code you own (no hidden abstraction), you follow each dependency's own official upgrade path.

### 1. Follow the Tailwind v4 upgrade guide

- Upgrade to Tailwind v4 per the official guide: https://tailwindcss.com/docs/upgrade-guide
- Use the `@tailwindcss/upgrade@next` codemod to remove deprecated utility classes and update the Tailwind config.

### 2. Update CSS variables (the `@theme inline` mapping)

The codemod migrates CSS variables as references under `@theme`:

```css showLineNumbers
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
  }
}

@theme {
  --color-background: hsl(var(--background));
  --color-foreground: hsl(var(--foreground));
}
```

This works, but to make colors easier to use elsewhere (including reading values in JavaScript), move the `hsl()` wrapper out to the variable declaration and use `@theme inline`:

1. Move `:root` and `.dark` out of `@layer base`.
2. Wrap the color values in `hsl()`.
3. Add the `inline` option to `@theme` (`@theme inline`).
4. Remove the `hsl()` wrappers from inside `@theme`.

```css showLineNumbers
:root {
  --background: hsl(0 0% 100%); // <-- Wrap in hsl
  --foreground: hsl(0 0% 3.9%);
}

.dark {
  --background: hsl(0 0% 3.9%); // <-- Wrap in hsl
  --foreground: hsl(0 0% 98%);
}

@theme inline {
  --color-background: var(--background); // <-- Remove hsl
  --color-foreground: var(--foreground);
}
```

This is the general `@theme inline` mapping pattern: every semantic color/radius token defined on `:root`/`.dark` gets a matching `--color-*` (or `--radius-*`) entry inside `@theme inline` that just references the bare `var(--token)`, letting Tailwind generate utilities (`bg-background`, `text-foreground`, etc.) while keeping the actual color values (and their color function, OKLCH in the current default scaffold) declared once in `:root`/`.dark`. See `shadcn--theming.md` for the full current default scaffold using OKLCH values directly (no `hsl()` wrapper needed since OKLCH values do not require one).

### 3. Update chart colors

Since theme colors already resolve through `var()`, drop any `hsl()` wrapper in `chartConfig`:

```diff
const chartConfig = {
  desktop: {
    label: "Desktop",
-    color: "hsl(var(--chart-1))",
+    color: "var(--chart-1)",
  },
  mobile: {
    label: "Mobile",
-   color: "hsl(var(--chart-2))",
+   color: "var(--chart-2)",
  },
} satisfies ChartConfig
```

### 4. Use the new `size-*` utility

`size-*` (added in Tailwind v3.4) is now fully supported by `tailwind-merge`:

```diff
- w-4 h-4
+ size-4
```

### 5. Update dependencies

```bash
pnpm up "@radix-ui/*" cmdk lucide-react recharts tailwind-merge clsx --latest
```

### 6. Remove `forwardRef`

Use the `remove-forward-ref` codemod (https://github.com/reactjs/react-codemod#remove-forward-ref) or do it manually:

1. Replace `React.forwardRef<...>` with `React.ComponentProps<...>`.
2. Remove `ref={ref}` from the component.
3. Add a `data-slot` attribute (useful for styling with Tailwind).
4. Optionally convert to a named function and remove `displayName`.

Before:

```tsx showLineNumbers
const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item
    ref={ref}
    className={cn("border-b last:border-b-0", className)}
    {...props}
  />
))
AccordionItem.displayName = "AccordionItem"
```

After:

```tsx showLineNumbers
function AccordionItem({
  className,
  ...props
}: React.ComponentProps<typeof AccordionPrimitive.Item>) {
  return (
    <AccordionPrimitive.Item
      data-slot="accordion-item"
      className={cn("border-b last:border-b-0", className)}
      {...props}
    />
  )
}
```

## Changelog (dated entries shown on this page)

### March 19, 2025: Deprecate `tailwindcss-animate`

`tailwindcss-animate` is deprecated in favor of `tw-animate-css`. New projects install `tw-animate-css` by default. For existing projects:

1. Remove `tailwindcss-animate` from dependencies.
2. Remove `@plugin 'tailwindcss-animate';` from `globals.css`.
3. Install `tw-animate-css` as a dev dependency.
4. Add `@import "tw-animate-css";` to `globals.css`.

```diff showLineNumbers
- @plugin 'tailwindcss-animate';
+ @import "tw-animate-css";
```

### March 12, 2025: New dark mode colors

Dark mode colors were revisited for better accessibility. For an existing Tailwind v4 project (not an upgraded one; upgraded projects are unaffected and can keep the old dark mode colors), update components to the new dark mode colors by re-adding components via the CLI:

1. Commit any changes (the CLI overwrites existing components):
   ```bash
   git add .
   git commit -m "..."
   ```
2. Update components:
   ```bash
   npx shadcn@latest add --all --overwrite
   ```
3. Update the dark mode colors in `globals.css` to the new OKLCH colors (see the Base Colors reference at `/docs/theming#base-colors`, transcribed in `shadcn--theming.md`).
4. Review and re-apply any changes made to components.
