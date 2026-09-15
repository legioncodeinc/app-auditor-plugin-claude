# Badge

- URL: https://ui.shadcn.com/docs/components/badge
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/badge.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/badge.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`.

## Description

"Displays a badge or a component that looks like a badge."

## Installation

```bash
npx shadcn@latest add badge
```

Manual: copy the component source below (no extra runtime dependency beyond `cn`).

## Usage

```tsx
import { Badge } from "@/components/ui/badge"
```

```tsx
<Badge variant="default | outline | secondary | destructive">Badge</Badge>
```

## Documented variations (section headings on the page)

Variants, With Icon (`data-icon="inline-start"` / `data-icon="inline-end"`), With Spinner (same `data-icon` convention), Link (`asChild` prop to render a link as a badge), Custom Colors (e.g. `bg-green-50 dark:bg-green-800` custom classes), RTL.

## API Reference

### Badge

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline" \| "ghost" \| "link"` | `"default"` |
| `className` | `string` | - |

Note: the doc's API table lists six variant values (`default`, `secondary`, `destructive`, `outline`, `ghost`, `link`), which matches the `cva` source below exactly, even though the "Usage" code sample only shows four (`default | outline | secondary | destructive`).

## Component source (`components/ui/badge.tsx`, `radix` base)

```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "cn"
import { Slot } from "radix-ui"

const badgeVariants = cva(
  "cn-badge group/badge inline-flex w-fit shrink-0 items-center justify-center overflow-hidden whitespace-nowrap focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 aria-invalid:border-destructive aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 [&>svg]:pointer-events-none",
  {
    variants: {
      variant: {
        default: "cn-badge-variant-default",
        secondary: "cn-badge-variant-secondary",
        destructive: "cn-badge-variant-destructive",
        outline: "cn-badge-variant-outline",
        ghost: "cn-badge-variant-ghost",
        link: "cn-badge-variant-link",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({
  className,
  variant = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"span"> &
  VariantProps<typeof badgeVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot.Root : "span"

  return (
    <Comp
      data-slot="badge"
      data-variant={variant}
      className={cn(badgeVariants({ variant }), className)}
      {...props}
    />
  )
}

export { Badge, badgeVariants }
```

Same semantic-class architecture note applies as for Button: variant values map to `cn-badge-variant-*` classes plus `data-slot`/`data-variant` attributes, with actual colors defined in the imported `shadcn/tailwind.css` layer rather than inline per-variant utility strings.
