# Button

- URL: https://ui.shadcn.com/docs/components/button
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/button.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/button.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter includes `featured: true`, `base: radix`, `component: true`.

## Description

"Displays a button or a component that looks like a button."

## Installation

CLI:

```bash
npx shadcn@latest add button
```

Manual: install `radix-ui`, then copy the component source below.

```bash
npm install radix-ui
```

## Usage

```tsx
import { Button } from "@/components/ui/button"
```

```tsx
<Button variant="outline">Button</Button>
```

## Cursor behavior (Tailwind v4 note)

Tailwind v4 switched from `cursor: pointer` to `cursor: default` for the button component. To keep `cursor: pointer`, add to the CSS file (or pass `--pointer` to `init`):

```css showLineNumbers title="globals.css"
@layer base {
  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}
```

## Documented variations (section headings on the page)

Size, Default, Outline, Secondary, Ghost, Destructive, Link, Icon, With Icon (use `data-icon="inline-start"` / `data-icon="inline-end"` on the icon for correct spacing), Rounded (`rounded-full` class), Spinner (render `<Spinner />` inside; same `data-icon` attribute convention), Button Group (see the `ButtonGroup` component), As Child (`asChild` prop makes another component look like a button), RTL.

## API Reference

### Button

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" \| "outline" \| "ghost" \| "destructive" \| "secondary" \| "link"` | `"default"` |
| `size` | `"default" \| "xs" \| "sm" \| "lg" \| "icon" \| "icon-xs" \| "icon-sm" \| "icon-lg"` | `"default"` |
| `asChild` | `boolean` | `false` |

## Component source (`components/ui/button.tsx`, `radix` base)

```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "cn"
import { Slot } from "radix-ui"

const buttonVariants = cva(
  "cn-button group/button inline-flex shrink-0 items-center justify-center whitespace-nowrap transition-all outline-none select-none disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "cn-button-variant-default",
        outline: "cn-button-variant-outline",
        secondary: "cn-button-variant-secondary",
        ghost: "cn-button-variant-ghost",
        destructive: "cn-button-variant-destructive",
        link: "cn-button-variant-link",
      },
      size: {
        default: "cn-button-size-default",
        xs: "cn-button-size-xs",
        sm: "cn-button-size-sm",
        lg: "cn-button-size-lg",
        icon: "cn-button-size-icon",
        "icon-xs": "cn-button-size-icon-xs",
        "icon-sm": "cn-button-size-icon-sm",
        "icon-lg": "cn-button-size-icon-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot.Root : "button"

  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
```

## Important architecture note (current vs. classic shadcn output)

This current source is notably different from the historically documented shadcn/ui pattern where `cva` variant entries hold literal Tailwind utility strings (e.g. `"bg-primary text-primary-foreground hover:bg-primary/90"`). In the version fetched here, each `cva` variant/size resolves to a single **semantic class name** (e.g. `cn-button-variant-default`, `cn-button-size-icon-lg`) plus `data-slot`, `data-variant`, and `data-size` attributes on the rendered element. The actual visual styling for those semantic classes lives in the `shadcn/tailwind.css` import pulled in via `@import "shadcn/tailwind.css";` in the project's global CSS (see `shadcn--theming.md` and the `eject` command in `shadcn--cli.md`), not inline in the component file. Also notable: `cn` is imported from a package literally named `cn` (see the `migrate cn` command in `shadcn--cli.md`), not hand-rolled from `clsx` + `tailwind-merge`, and `Slot` comes from the unified `radix-ui` package (`Slot.Root`), not `@radix-ui/react-slot`.

When auditing a captured app's Button usage against "the shadcn Button," check whether the app is on this newer semantic-class/`cn`-package architecture or the older inline-Tailwind-per-variant architecture; both are legitimate shadcn output depending on when the project was scaffolded or last re-synced.
