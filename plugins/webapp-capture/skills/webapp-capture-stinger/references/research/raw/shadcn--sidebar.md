# Sidebar

- URL: https://ui.shadcn.com/docs/components/sidebar
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/sidebar.mdx`, first ~250 of 664 lines transcribed) + GitHub source (`apps/v4/registry/bases/radix/ui/sidebar.tsx`, export list), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`.

## Description

"A composable, themeable and customizable sidebar component." Per the page intro: "Sidebars are one of the most complex components to build. They are central to any application and often contain a lot of moving parts. We now have a solid foundation to build on top of. Composable. Themeable. Customizable." Links to the Blocks library (https://ui.shadcn.com/blocks) for ready-made sidebar layouts.

## Installation

```bash
npx shadcn@latest add sidebar
```

## Usage

```tsx showLineNumbers title="app/layout.tsx"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        {children}
      </main>
    </SidebarProvider>
  )
}
```

```tsx showLineNumbers title="components/app-sidebar.tsx"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar"

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader />
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  )
}
```

## Composition (anatomy)

```
SidebarProvider
├── Sidebar
│   ├── SidebarHeader
│   ├── SidebarContent
│   │   ├── SidebarGroup
│   │   │   ├── SidebarGroupLabel
│   │   │   ├── SidebarGroupAction
│   │   │   ├── SidebarGroupContent
│   │   │   └── SidebarMenu
│   │   │       ├── SidebarMenuItem
│   │   │       │   ├── SidebarMenuButton
│   │   │       │   ├── SidebarMenuAction
│   │   │       │   └── SidebarMenuBadge
│   │   │       └── SidebarMenuItem
│   │   │           ├── SidebarMenuButton
│   │   │           └── SidebarMenuSub
│   │   │               ├── SidebarMenuSubItem
│   │   │               └── SidebarMenuSubItem
│   │   └── SidebarGroup
│   │       └── SidebarMenu
│   │           ├── SidebarMenuItem
│   │           └── SidebarMenuItem
│   ├── SidebarFooter
│   └── SidebarRail
├── SidebarInset
└── SidebarTrigger
```

## Structure (per docs prose)

- **SidebarProvider**: handles collapsible state and provides sidebar context to child components.
- **Sidebar**: the main collapsible sidebar panel.
- **SidebarHeader**: sticky at the top; branding, titles, or workspace switchers.
- **SidebarFooter**: sticky at the bottom; user menus, settings, or actions.
- **SidebarContent**: scrollable region between header and footer.
- **SidebarGroup**: groups related navigation with optional label, action, and content areas.
- **SidebarMenu** / **SidebarMenuItem**: menu structure for links, badges, actions, and nested submenus.
- **SidebarRail**: resize handle for adjusting sidebar width when applicable.
- **SidebarInset**: wraps main content when using the `inset` variant.
- **SidebarTrigger**: control that toggles the sidebar open or collapsed.

## SidebarProvider

Wraps the app; provides sidebar context. Always wrap the application in a `SidebarProvider`.

### Props

| Name | Type | Description |
| --- | --- | --- |
| `defaultOpen` | `boolean` | Default open state of the sidebar. |
| `open` | `boolean` | Open state of the sidebar (controlled). |
| `onOpenChange` | `(open: boolean) => void` | Sets open state of the sidebar (controlled). |

### Width

Single sidebar: use the `SIDEBAR_WIDTH` and `SIDEBAR_WIDTH_MOBILE` constants in `sidebar.tsx`:

```tsx showLineNumbers title="components/ui/sidebar.tsx"
const SIDEBAR_WIDTH = "16rem"
const SIDEBAR_WIDTH_MOBILE = "18rem"
```

Multiple sidebars: use `--sidebar-width` and `--sidebar-width-mobile` CSS variables via the `style` prop:

```tsx showLineNumbers
<SidebarProvider
  style={
    {
      "--sidebar-width": "20rem",
      "--sidebar-width-mobile": "20rem",
    } as React.CSSProperties
  }
>
  <Sidebar />
</SidebarProvider>
```

### Keyboard shortcut

`cmd+b` (Mac) / `ctrl+b` (Windows) toggles the sidebar:

```tsx showLineNumbers title="components/ui/sidebar.tsx"
const SIDEBAR_KEYBOARD_SHORTCUT = "b"
```

## Sidebar

The main collapsible sidebar panel.

### Props

| Property | Type | Description |
| --- | --- | --- |
| `side` | `left` or `right` | The side of the sidebar. |
| `variant` | `sidebar`, `floating`, or `inset` | The variant of the sidebar. |
| `collapsible` | `offcanvas`, `icon`, or `none` | Collapsible state of the sidebar. |

`collapsible` values:

| Value | Description |
| --- | --- |
| `offcanvas` | A collapsible sidebar that slides in from the left or right. |
| `icon` | A sidebar that collapses to icons. |
| `none` | A non-collapsible sidebar. |

**Note:** when using the `inset` variant, wrap main content in `SidebarInset`:

```tsx showLineNumbers
<SidebarProvider>
  <Sidebar variant="inset" />
  <SidebarInset>
    <main>{children}</main>
  </SidebarInset>
</SidebarProvider>
```

## useSidebar

Hook to control the sidebar:

```tsx showLineNumbers
import { useSidebar } from "@/components/ui/sidebar"

export function AppSidebar() {
  const {
    state,
    open,
    setOpen,
    openMobile,
    setOpenMobile,
    // ...additional fields documented further down the page (not transcribed
    // in this excerpt): isMobile, toggleSidebar
  } = useSidebar()
}
```

## Full exported symbol list (from GitHub source, `apps/v4/registry/bases/radix/ui/sidebar.tsx`)

Function/hook names found in the source (54 KB / 708 lines total; not fully transcribed here beyond the anatomy above):

`useSidebar`, `SidebarProvider`, `Sidebar`, `SidebarTrigger`, `SidebarRail`, `SidebarInset`, `SidebarInput`, `SidebarHeader`, `SidebarFooter`, `SidebarSeparator`, `SidebarContent`, `SidebarGroup`, `SidebarGroupLabel`, `SidebarGroupAction`, `SidebarGroupContent`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`, `SidebarMenuAction`, `SidebarMenuBadge`, `SidebarMenuSkeleton`, `SidebarMenuSub`, `SidebarMenuSubItem`, `SidebarMenuSubButton`.

This confirms the anatomy tree above is complete and no subcomponent names have changed from the classic shadcn/ui Sidebar API.

## Cross-reference: sidebar blocks

The registry ships 16 pre-built sidebar block variants (`sidebar-01` through `sidebar-16`, `type: "registry:block"`) plus a `dashboard-01` block and numerous `login-*`/`signup-*` blocks that use `Sidebar`. See `shadcn--components-index.md` and `shadcn--blocks.md`.
