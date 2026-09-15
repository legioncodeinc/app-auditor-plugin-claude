# Switch

- URL: https://ui.shadcn.com/docs/components/switch
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/switch.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/switch.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`, links to Radix UI Switch docs/API reference.

## Description

"A control that allows the user to toggle between checked and not checked."

## Installation

```bash
npx shadcn@latest add switch
```

Manual: `npm install radix-ui`, then copy the source below.

## Usage

```tsx
import { Switch } from "@/components/ui/switch"
```

```tsx
<Switch />
```

## Documented variations

- **Description**.
- **Choice Card**: card-style selection where `FieldLabel` wraps the entire `Field` for a clickable card pattern.
- **Disabled**: `disabled` prop on `Switch`; `data-disabled` on `Field` for styling.
- **Invalid**: `aria-invalid` prop on `Switch`; `data-invalid` on `Field` for styling.
- **Size**: `size` prop changes the switch size.
- **RTL**.

## API Reference

Links out to Radix UI's Switch API reference: https://www.radix-ui.com/docs/primitives/components/switch#api-reference

## Component source (`components/ui/switch.tsx`, `radix` base)

```tsx
"use client"

import * as React from "react"
import { cn } from "cn"
import { Switch as SwitchPrimitive } from "radix-ui"

function Switch({
  className,
  size = "default",
  ...props
}: React.ComponentProps<typeof SwitchPrimitive.Root> & {
  size?: "sm" | "default"
}) {
  return (
    <SwitchPrimitive.Root
      data-slot="switch"
      data-size={size}
      className={cn(
        "cn-switch peer group/switch relative inline-flex items-center transition-all outline-none after:absolute after:-inset-x-3 after:-inset-y-2 data-disabled:cursor-not-allowed data-disabled:opacity-50",
        className
      )}
      {...props}
    >
      <SwitchPrimitive.Thumb
        data-slot="switch-thumb"
        className="cn-switch-thumb pointer-events-none block ring-0 transition-transform"
      />
    </SwitchPrimitive.Root>
  )
}

export { Switch }
```

Anatomy: `Switch` (wraps `SwitchPrimitive.Root`) containing a single `SwitchPrimitive.Thumb` (`data-slot="switch-thumb"`). The `size` prop (`"sm" | "default"`) is exposed via `data-size`; the enlarged invisible hit-target is created with `after:-inset-x-3 after:-inset-y-2`.
