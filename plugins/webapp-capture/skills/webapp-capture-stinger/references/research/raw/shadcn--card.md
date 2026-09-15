# Card

- URL: https://ui.shadcn.com/docs/components/card
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/card.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/card.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`.

## Description

"Displays a card with header, content, and footer."

## Installation

```bash
npx shadcn@latest add card
```

## Usage

```tsx showLineNumbers
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
```

```tsx showLineNumbers
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card Description</CardDescription>
    <CardAction>Card Action</CardAction>
  </CardHeader>
  <CardContent>
    <p>Card Content</p>
  </CardContent>
  <CardFooter>
    <p>Card Footer</p>
  </CardFooter>
</Card>
```

## Composition (anatomy)

```
Card
├── CardHeader
│   ├── CardTitle
│   ├── CardDescription
│   └── CardAction
├── CardContent
└── CardFooter
```

## Documented variations

- **Size**: `size="sm"` prop for a small card with smaller spacing.
- **Spacing**: the `--card-spacing` CSS variable controls spacing between sections and the inset of card parts. Use negative margins `-mx-(--card-spacing)` for edge-to-edge content while staying aligned with the card inset; use `-mb-(--card-spacing)` on `CardContent` when edge-to-edge content sits above a footer.
- **Image**: place an image before `CardHeader` for an image card.
- **RTL**.

## API Reference

### Card

| Prop | Type | Default |
| --- | --- | --- |
| `size` | `"default" \| "sm"` | `"default"` |
| `className` | `string` | - |

### CardHeader

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

Used for a title, description, and optional action.

### CardTitle

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardDescription

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

Helper text under the title.

### CardAction

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

Places content in the top-right of the header (e.g. a button or badge).

### CardContent

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardFooter

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

## Component source (`components/ui/card.tsx`, `radix` base)

```tsx
import * as React from "react"
import { cn } from "cn"

function Card({
  className,
  size = "default",
  ...props
}: React.ComponentProps<"div"> & { size?: "default" | "sm" }) {
  return (
    <div
      data-slot="card"
      data-size={size}
      className={cn("cn-card group/card flex flex-col", className)}
      {...props}
    />
  )
}

function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-header"
      className={cn(
        "cn-card-header group/card-header @container/card-header grid auto-rows-min items-start has-data-[slot=card-action]:grid-cols-[1fr_auto] has-data-[slot=card-description]:grid-rows-[auto_auto]",
        className
      )}
      {...props}
    />
  )
}

function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-title"
      className={cn("cn-card-title cn-font-heading", className)}
      {...props}
    />
  )
}

function CardDescription({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-description"
      className={cn("cn-card-description", className)}
      {...props}
    />
  )
}

function CardAction({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-action"
      className={cn(
        "cn-card-action col-start-2 row-span-2 row-start-1 self-start justify-self-end",
        className
      )}
      {...props}
    />
  )
}

function CardContent({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-content"
      className={cn("cn-card-content", className)}
      {...props}
    />
  )
}

function CardFooter({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-footer"
      className={cn("cn-card-footer flex items-center", className)}
      {...props}
    />
  )
}

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardAction,
  CardDescription,
  CardContent,
}
```

## Changelog: `--card-spacing` migration

If upgrading from a previous version of `Card`, the docs give this diff-based migration:

1. Card root: replace hard-coded gap/vertical padding with `--card-spacing`:
   ```diff
     className={cn(
   -   "group/card flex flex-col gap-4 overflow-hidden rounded-xl bg-card py-4 text-sm text-card-foreground ring-1 ring-foreground/10 has-data-[slot=card-footer]:pb-0 has-[>img:first-child]:pt-0 data-[size=sm]:gap-3 data-[size=sm]:py-3 data-[size=sm]:has-data-[slot=card-footer]:pb-0 *:[img:first-child]:rounded-t-xl *:[img:last-child]:rounded-b-xl",
   +   "group/card flex flex-col gap-(--card-spacing) overflow-hidden rounded-xl bg-card py-(--card-spacing) text-sm text-card-foreground ring-1 ring-foreground/10 [--card-spacing:--spacing(4)] has-data-[slot=card-footer]:pb-0 has-[>img:first-child]:pt-0 data-[size=sm]:[--card-spacing:--spacing(3)] data-[size=sm]:has-data-[slot=card-footer]:pb-0 *:[img:first-child]:rounded-t-xl *:[img:last-child]:rounded-b-xl",
       className
     )}
   ```
2. CardHeader: replace horizontal padding/border spacing with the shared variable (drop the `group-data-[size=sm]/card:px-3` special-case in favor of `px-(--card-spacing)`).
3. CardContent / CardFooter: use `px-(--card-spacing)` and `p-(--card-spacing)` respectively instead of hard-coded `px-4`/`p-4` plus a `sm` override.

After migrating, customize spacing per-instance:

```tsx
function Example() {
  return <Card className="[--card-spacing:--spacing(6)]">...</Card>
}
```
