# shadcn-svelte: Introduction and Component List

- URL: https://shadcn-svelte.com/docs (Introduction) and https://shadcn-svelte.com/docs/components (index)
- Fetched: 2026-09-15
- Source type: official docs (raw Markdown transcribed from `huntabyte/shadcn-svelte`, `docs/content/index.md` and `docs/content/components/*.md` frontmatter, `main` branch) + `docs/content/about.md`
- Last updated (if shown): unknown

## What shadcn-svelte is (per the Introduction page)

"An unofficial, community-led Svelte port of shadcn/ui. We are not affiliated with shadcn, but we did get his blessing before creating a Svelte version of his work." Maintained by Huntabyte, CokaKoala (Adrian Gonzalez), and Aidan Bleser (per `about.md`), with community contributions.

Verbatim positioning statement: "**This is not a component library. It is how you build your component library.**" Same five principles as shadcn/ui: Open Code, Composition, Distribution, Beautiful Defaults, AI-Ready.

## Credits (per `about.md`)

- shadcn: original designs/methodology/implementation.
- **Bits UI** (https://bits-ui.com): "The headless components that power this project." This is the key architectural difference from shadcn/ui, which is built on Radix UI (or, per the newer `--base` options, Base UI or React Aria). shadcn-svelte is built on Bits UI, a Svelte-native headless component library, not a Svelte port of Radix primitives.
- **Formsnap** (https://formsnap.dev): form components (the Svelte analogue of shadcn/ui's React Hook Form + Zod `form` pattern).
- **Paneforge** (https://paneforge.com): resizable components.
- **Vaul Svelte** (https://vaul-svelte.com): drawer components.
- Radix UI: credited as what the original shadcn/ui (and by extension shadcn-svelte's design lineage) was built on.
- Shu Ding: typography style adapted from his Nextra work.
- Cal: original source of the Button's first styles.

License: MIT (c) shadcn & huntabyte.

## Full component list (`docs/content/components/*.md`, GitHub file listing)

accordion, alert-dialog, alert, aspect-ratio, attachment, avatar, badge, breadcrumb, bubble, button-group, button, calendar, card, carousel, chart, checkbox, collapsible, combobox, command, context-menu, data-table, date-picker, dialog, drawer, dropdown-menu, empty, field, hover-card, input-group, input-otp, input, item, kbd, label, marker, menubar, message, native-select, navigation-menu, pagination, popover, progress, radio-group, **range-calendar**, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, spinner, switch, table, tabs, textarea, toggle-group, toggle, tooltip, typography.

(63 component doc files at fetch time, excluding the `index.md` overview file in that directory.)

## Differences from the shadcn/ui (React) component list

Compared against `shadcn--components-index.md`'s React list (from `apps/v4/content/docs/components/radix/*.mdx`):

- **shadcn-svelte has `range-calendar` as its own dedicated doc page**, which the current React docs fold into `calendar`/`date-picker` guides rather than documenting as a separate page.
- **shadcn-svelte has no `direction.mdx`, `message-scroller.mdx`, or `questionnaire.mdx`** pages (these are present in the current React docs; they may be newer React-only additions not yet ported).
- **shadcn-svelte has no `toast.md`** (React still has a deprecated `toast.mdx` page even though it recommends `sonner`; shadcn-svelte only documents `sonner`, i.e. it skipped ever shipping `toast` and went straight to the Sonner-based toast).
- Both ports document `form` under a separate "Forms" doc tree, not inside the main `components/` folder listing (Formsnap for Svelte, React Hook Form + Zod for React), so `form` does not appear in either component-folder file listing above.
- Both ports include the newer "conversation UI" primitives (`attachment`, `bubble`, `marker`, `message`), showing shadcn-svelte has kept pace with those additions; the React-only `message-scroller` is the one from that family not yet mirrored.

## Naming differences: Svelte namespace/dot-notation vs React flat exports

The single biggest structural difference is **import and usage style**, not naming of the components themselves. Where shadcn/ui (React) exports flat named components per file (e.g. `Select`, `SelectTrigger`, `SelectContent`, `SelectItem` all imported individually), shadcn-svelte exports a **namespace module accessed with dot notation**:

React:

```tsx
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Theme" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="light">Light</SelectItem>
  </SelectContent>
</Select>
```

Svelte:

```svelte
<script lang="ts">
  import * as Select from "$lib/components/ui/select/index.js";
</script>

<Select.Root type="single">
  <Select.Trigger class="w-[180px]">
    <Select.Value placeholder="Select a theme" />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="light">Light</Select.Item>
  </Select.Content>
</Select.Root>
```

Key naming/API deltas visible in this pattern (from `docs/content/components/select.md`):

- The React root component is just `Select`; the Svelte root component is `Select.Root` (i.e. shadcn-svelte adds an explicit `.Root` suffix that React's flat-export style omits).
- `Select.Root` in shadcn-svelte requires an explicit `type="single"` (or `"multiple"`) prop; this is a Bits UI API detail with no equivalent required prop on the React/Radix `Select`.
- shadcn-svelte's `Select.Value` reads its label from the matching `Select.Item` while the menu is open, but that item unmounts when the menu closes, so the docs recommend passing an `items` array (of `{ value, label }`) to `Select.Root` so the trigger's label survives after close: `<Select.Root type="single" items={themes}>`. This `items` prop has no equivalent in the React/Radix `Select`.
- `Button` similarly changes from a flat `<Button variant="outline">Button</Button>` import in both ports (Button is a single component, not a compound one, in both) to a Svelte import path convention of `import { Button } from "$lib/components/ui/button/index.js";` (named export from an `index.js` barrel) versus React's `@/components/ui/button` module path. The underlying primitive is Bits UI's `Button` (https://bits-ui.com/docs/components/button) rather than Radix's `Slot`-based approach, though the Svelte Button doc's own installation manual step lists no extra primitive dependency to install (unlike the React `radix-ui` install step for Button/Select/Switch/Tabs/Dialog/Tooltip).

## Sidebar naming note

shadcn-svelte's Sidebar doc states: "Shad doesn't like building sidebars, so he built 30+ of them with all kinds of configurations. The core components have been extracted into `sidebar-*.svelte` files, and you can use them in your own projects." This differs in file-naming convention from the React version's single `sidebar.tsx` registry file (React keeps all Sidebar subcomponents in one file; Svelte splits them into multiple `sidebar-*.svelte` files, one component per file, consistent with Svelte's single-file-component convention). The subcomponent names themselves (`Sidebar`, `SidebarProvider`, `SidebarHeader`, `SidebarContent`, `SidebarGroup`, `SidebarMenu`, etc.) match the React API 1:1 at the concept level; see `shadcn--sidebar.md`.

## CLI naming difference

The Svelte CLI package is `shadcn-svelte` (invoked as `npx shadcn-svelte@latest ...`), a separate npm package from the React `shadcn` CLI (`npx shadcn@latest ...`). See `shadcn--svelte-theming.md`'s companion CLI notes and `shadcn--cli.md` for the React CLI.
