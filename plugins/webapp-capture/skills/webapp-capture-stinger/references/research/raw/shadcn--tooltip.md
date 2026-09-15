# Tooltip

- URL: https://ui.shadcn.com/docs/components/tooltip
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/tooltip.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/tooltip.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`, links to Radix UI Tooltip docs/API reference.

## Description

"A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it."

## Installation

CLI, plus a required manual step: add `TooltipProvider` to the app root.

```bash
npx shadcn@latest add tooltip
```

```tsx title="app/layout.tsx" showLineNumbers {1,7}
import { TooltipProvider } from "@/components/ui/tooltip"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <TooltipProvider>{children}</TooltipProvider>
      </body>
    </html>
  )
}
```

Manual install: `npm install radix-ui`, copy the source below, update import paths, then add `TooltipProvider` as above.

## Usage

```tsx showLineNumbers
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
```

```tsx showLineNumbers
<Tooltip>
  <TooltipTrigger>Hover</TooltipTrigger>
  <TooltipContent>
    <p>Add to library</p>
  </TooltipContent>
</Tooltip>
```

## Composition (anatomy)

```
Tooltip
├── TooltipTrigger
└── TooltipContent
```

Full exported list (from source): `Tooltip`, `TooltipContent`, `TooltipProvider`, `TooltipTrigger`.

## Documented variations

- **Side**: `side` prop changes tooltip position.
- **With Keyboard Shortcut**.
- **Disabled Button**: show a tooltip on a disabled button by wrapping it with a `<span>`.
- **RTL**.

## API Reference

Links out to Radix UI's Tooltip API reference: https://www.radix-ui.com/docs/primitives/components/tooltip#api-reference

## Component source (`components/ui/tooltip.tsx`, `radix` base)

```tsx
"use client"

import * as React from "react"
import { cn } from "cn"
import { Tooltip as TooltipPrimitive } from "radix-ui"

function TooltipProvider({
  delayDuration = 0,
  ...props
}: React.ComponentProps<typeof TooltipPrimitive.Provider>) {
  return (
    <TooltipPrimitive.Provider
      data-slot="tooltip-provider"
      delayDuration={delayDuration}
      {...props}
    />
  )
}

function Tooltip({
  ...props
}: React.ComponentProps<typeof TooltipPrimitive.Root>) {
  return <TooltipPrimitive.Root data-slot="tooltip" {...props} />
}

function TooltipTrigger({
  ...props
}: React.ComponentProps<typeof TooltipPrimitive.Trigger>) {
  return <TooltipPrimitive.Trigger data-slot="tooltip-trigger" {...props} />
}

function TooltipContent({
  className,
  sideOffset = 0,
  children,
  ...props
}: React.ComponentProps<typeof TooltipPrimitive.Content>) {
  return (
    <TooltipPrimitive.Portal>
      <TooltipPrimitive.Content
        data-slot="tooltip-content"
        sideOffset={sideOffset}
        className={cn(
          "cn-tooltip-content z-50 w-fit max-w-xs origin-(--radix-tooltip-content-transform-origin) bg-foreground text-background",
          className
        )}
        {...props}
      >
        {children}
        <TooltipPrimitive.Arrow className="cn-tooltip-arrow z-50 translate-y-[calc(-50%_-_2px)] bg-foreground fill-foreground" />
      </TooltipPrimitive.Content>
    </TooltipPrimitive.Portal>
  )
}

export { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger }
```

Note: `TooltipProvider` defaults `delayDuration` to `0` (instant tooltips), and `TooltipContent` defaults `sideOffset` to `0` in this version (older shadcn/ui releases commonly defaulted `sideOffset` to `4`).
