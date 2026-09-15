# Alert

- URL: https://ui.shadcn.com/docs/components/alert
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/alert.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/alert.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`.

## Description

"Displays a callout for user attention."

## Installation

```bash
npx shadcn@latest add alert
```

## Usage

```tsx showLineNumbers
import {
  Alert,
  AlertAction,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
```

```tsx showLineNumbers
<Alert>
  <InfoIcon />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components and dependencies to your app using the cli.
  </AlertDescription>
  <AlertAction>
    <Button variant="outline">Enable</Button>
  </AlertAction>
</Alert>
```

## Composition (anatomy)

```
Alert
├── Icon
├── AlertTitle
├── AlertDescription
└── AlertAction
```

Note: the icon is passed directly as a child of `Alert` (e.g. `<InfoIcon />`), not wrapped in a dedicated `AlertIcon` subcomponent; positioning is handled by CSS selectors inside the `Alert` semantic class.

## Documented variations

- **Basic**: icon, title, description.
- **Destructive**: `variant="destructive"`.
- **Action**: `AlertAction` adds a button or other action element.
- **Custom Colors**: custom classes such as `bg-amber-50 dark:bg-amber-950` on `Alert`.
- **RTL**.

## API Reference

### Alert

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" \| "destructive"` | `"default"` |

### AlertTitle

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AlertDescription

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AlertAction

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

"Displays an action element (like a button) positioned absolutely in the top-right corner of the alert."

## Component source (`components/ui/alert.tsx`, `radix` base)

```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "cn"

const alertVariants = cva("cn-alert group/alert relative w-full", {
  variants: {
    variant: {
      default: "cn-alert-variant-default",
      destructive: "cn-alert-variant-destructive",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})

function Alert({
  className,
  variant,
  ...props
}: React.ComponentProps<"div"> & VariantProps<typeof alertVariants>) {
  return (
    <div
      data-slot="alert"
      role="alert"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    />
  )
}

function AlertTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="alert-title"
      className={cn(
        "cn-alert-title [&_a]:underline [&_a]:underline-offset-3 [&_a]:hover:text-foreground",
        className
      )}
      {...props}
    />
  )
}

function AlertDescription({
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="alert-description"
      className={cn(
        "cn-alert-description [&_a]:underline [&_a]:underline-offset-3 [&_a]:hover:text-foreground",
        className
      )}
      {...props}
    />
  )
}

function AlertAction({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="alert-action"
      className={cn("cn-alert-action", className)}
      {...props}
    />
  )
}

export { Alert, AlertTitle, AlertDescription, AlertAction }
```

Note: `Alert` has `role="alert"` baked in, and only two `cva` variants (`default`, `destructive`); the two-color (background/foreground) `destructive` variant lives entirely in the `cn-alert-variant-destructive` semantic class rather than inline utility strings.
