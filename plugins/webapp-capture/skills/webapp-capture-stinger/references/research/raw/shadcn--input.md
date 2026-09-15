# Input

- URL: https://ui.shadcn.com/docs/components/input
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/input.mdx`) + GitHub source (`apps/v4/registry/bases/radix/ui/input.tsx`), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`.

## Description

"A text input component for forms and user data entry with built-in styling and accessibility features."

## Installation

```bash
npx shadcn@latest add input
```

## Usage

```tsx
import { Input } from "@/components/ui/input"
```

```tsx
<Input />
```

## Documented variations (section headings on the page)

- **Basic**
- **Field**: use `Field`, `FieldLabel`, `FieldDescription` to build an input with a label and description.
- **Field Group**: use `FieldGroup` to show multiple `Field` blocks and build forms.
- **Disabled**: `disabled` prop on `Input`; add `data-disabled` to the `Field` for styling.
- **Invalid**: `aria-invalid` prop on `Input`; add `data-invalid` to the `Field` for styling.
- **File**: `type="file"`.
- **Inline**: `Field` with `orientation="horizontal"`; pair with `Button` for a search-input-with-button pattern.
- **Grid**: grid layout for multiple inputs side by side.
- **Required**: `required` attribute.
- **Badge**: render `Badge` in the label to highlight a recommended field.
- **Input Group**: use the `InputGroup` component to add icons/text/buttons inside an input (separate component, see `/docs/components/input-group`).
- **Button Group**: use `ButtonGroup` to add buttons to an input (separate component, see `/docs/components/button-group`).
- **Form**: a full form example combining multiple inputs, a select, and a button.
- **RTL**.

This page does not include an explicit "API Reference" prop table (unlike Button, Badge, Card, Alert, Select links to Radix docs); the anatomy is a single native `<input>` wrapped with the `cn-input` semantic class.

## Component source (`components/ui/input.tsx`, `radix` base)

```tsx
import * as React from "react"
import { cn } from "cn"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "cn-input w-full min-w-0 outline-none file:inline-flex file:border-0 file:bg-transparent file:text-foreground placeholder:text-muted-foreground disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
}

export { Input }
```

Note: as with Button/Badge/Card, most of the visual styling (border, background, focus ring, sizing) lives in the `cn-input` semantic class provided by the imported `shadcn/tailwind.css` layer, not as inline Tailwind utilities in this file.
