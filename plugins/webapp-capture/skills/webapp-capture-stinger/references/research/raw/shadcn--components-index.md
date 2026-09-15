# Components

- URL: https://ui.shadcn.com/docs/components
- Fetched: 2026-09-15
- Source type: official docs (site page is dynamically rendered from the registry; component list transcribed from `apps/v4/registry.json` and per-component MDX frontmatter in the `shadcn-ui/ui` GitHub repo, `main` branch)
- Last updated (if shown): unknown (registry.json and MDX files carry no per-file date; repo is under active development as of fetch date)

## Notes on source

The `/docs/components` page renders its list client-side from a `<ComponentsList />` React component, so the raw HTML does not contain a static list. The authoritative list was instead built from:

- `apps/v4/registry.json` (the machine-readable registry manifest), which enumerates every registry item, its `name` (the CLI install name) and its `type`.
- The frontmatter (`title`, `description`) of each file under `apps/v4/content/docs/components/radix/*.mdx`.

As of the fetch, shadcn/ui ships component docs in three "base" variants: `radix` (Radix UI primitives, the default/classic base), `base` (Base UI primitives, a newer alternative), and `aria` (React Aria, referenced by the CLI's `--base` flag). The `radix` variant is the one summarized below since it is the long-standing default. The install name (used with `npx shadcn add <name>`) is identical across bases.

## Full component ("registry:ui") list

Each row is `name` (registry item name / CLI install name), the doc title, and the doc description, both taken from the MDX frontmatter.

| Install name | Title | Description |
| --- | --- | --- |
| accordion | Accordion | A vertically stacked set of interactive headings that each reveal a section of content. |
| alert | Alert | Displays a callout for user attention. |
| alert-dialog | Alert Dialog | A modal dialog that interrupts the user with important content and expects a response. |
| aspect-ratio | Aspect Ratio | Displays content within a desired ratio. |
| avatar | Avatar | An image element with a fallback for representing the user. |
| badge | Badge | Displays a badge or a component that looks like a badge. |
| breadcrumb | Breadcrumb | Displays the path to the current resource using a hierarchy of links. |
| button | Button | Displays a button or a component that looks like a button. |
| button-group | Button Group | A container that groups related buttons together with consistent styling. |
| calendar | Calendar | A calendar component that allows users to select a date or a range of dates. |
| card | Card | Displays a card with header, content, and footer. |
| carousel | Carousel | A carousel with motion and swipe built using Embla. |
| chart | Chart | Beautiful charts. Built using Recharts. Copy and paste into your apps. |
| checkbox | Checkbox | A control that allows the user to toggle between checked and not checked. |
| collapsible | Collapsible | An interactive component which expands/collapses a panel. |
| command | Command | Command menu for search and quick actions. |
| context-menu | Context Menu | Displays a menu of actions triggered by a right click. |
| dialog | Dialog | A window overlaid on either the primary window or another dialog window, rendering the content underneath inert. |
| drawer | Drawer | A drawer component for React. |
| dropdown-menu | Dropdown Menu | Displays a menu to the user, such as a set of actions or functions, triggered by a button. |
| empty | Empty | Use the Empty component to display an empty state. |
| field | Field | Combine labels, controls, and help text to compose accessible form fields and grouped inputs. |
| form | Form (no separate `.mdx` doc found under `components/radix`; documented under the "Forms" guide section) | React Hook Form + Zod wrapper components. |
| hover-card | Hover Card | For sighted users to preview content available behind a link. |
| input | Input | A text input component for forms and user data entry with built-in styling and accessibility features. |
| input-group | Input Group | Add addons, buttons, and helper content to inputs. |
| input-otp | Input OTP | Accessible one-time password component with copy-paste functionality. |
| item | Item | A versatile component for displaying content with media, title, description, and actions. |
| kbd | Kbd | Used to display textual user input from keyboard. |
| label | Label | Renders an accessible label associated with controls. |
| menubar | Menubar | A visually persistent menu common in desktop applications that provides quick access to a consistent set of commands. |
| native-select | Native Select | A styled native HTML select element with consistent design system integration. |
| navigation-menu | Navigation Menu | A collection of links for navigating websites. |
| pagination | Pagination | Pagination with page navigation, next and previous links. |
| popover | Popover | Displays rich content in a portal, triggered by a button. |
| progress | Progress | Displays an indicator showing the completion progress of a task, typically displayed as a progress bar. |
| radio-group | Radio Group | A set of checkable buttons, known as radio buttons, where no more than one of the buttons can be checked at a time. |
| resizable | Resizable | Accessible resizable panel groups and layouts with keyboard support. |
| scroll-area | Scroll Area | Augments native scroll functionality for custom, cross-browser styling. |
| select | Select | Displays a list of options for the user to pick from, triggered by a button. |
| separator | Separator | Visually or semantically separates content. |
| sheet | Sheet | Extends the Dialog component to display content that complements the main content of the screen. |
| sidebar | Sidebar | A composable, themeable and customizable sidebar component. |
| skeleton | Skeleton | Use to show a placeholder while content is loading. |
| slider | Slider | An input where the user selects a value from within a given range. |
| sonner | Sonner | An opinionated toast component for React. |
| spinner | Spinner | An indicator that can be used to show a loading state. |
| switch | Switch | A control that allows the user to toggle between checked and not checked. |
| table | Table | A responsive table component. |
| tabs | Tabs | A set of layered sections of content, known as tab panels, that are displayed one at a time. |
| textarea | Textarea | Displays a form textarea or a component that looks like a textarea. |
| toggle | Toggle | A two-state button that can be either on or off. |
| toggle-group | Toggle Group | A set of two-state buttons that can be toggled on or off. |
| tooltip | Tooltip | A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it. |

Source: `apps/v4/registry.json`, `items[].type === "registry:ui"`, 54 items total (list above; `form` is a registry item name confirmed in `registry.json` even though it did not have its own `.mdx` file under `components/radix` at fetch time).

## Documented but not a single-install "registry:ui" item

These have their own doc page but are either a guide/recipe (built by combining other components) or a distinct registry type:

| Doc name | Type | Notes |
| --- | --- | --- |
| data-table | Guide (uses `table` + TanStack Table) | "Powerful table and datagrids built using TanStack Table." Not a `registry:ui` item; there is no `npx shadcn add data-table` install. See `shadcn--data-table.md`. |
| combobox | Guide (uses `popover` + `command`) | "Autocomplete input with a list of suggestions." |
| date-picker | Guide (uses `popover` + `calendar`) | "A date picker component with range and presets." |
| toast | Deprecated component doc | "A succinct message that is displayed temporarily." Superseded by `sonner` (see Tailwind v4 changelog: "We're deprecating the `toast` component in favor of `sonner`."). |
| typography | Style guide (not a component) | "Styles for headings, paragraphs, lists, etc." |
| direction | Provider (RTL) | "A provider component that sets the text direction for your application." |

## Newer / less common component doc pages found (not requested by name, listed for completeness)

Found under `apps/v4/content/docs/components/radix/`: `attachment`, `bubble`, `marker`, `message`, `message-scroller`, `questionnaire`. These appear to be recent additions (chat/conversation UI primitives) beyond the classic component set; their frontmatter descriptions:

- `attachment.mdx`: "Displays a file or image attachment with media, metadata, upload state, and actions."
- `bubble.mdx`: "Displays conversational content in a message bubble. Supports variants, alignment, grouping, reactions, and collapsible content."
- `marker.mdx`: "Displays an inline status, system note, bordered row, or labeled separator in a conversation."
- `message.mdx`: "Displays a message in a conversation, with optional avatar, header, footer, and alignment."
- `message-scroller.mdx`: "A chat scroll container that anchors turns, opens saved transcripts, follows streamed responses, loads history without jumping, and jumps to any message."
- `questionnaire.mdx`: "A multi-step questionnaire with single-choice, multiple-choice, freeform, and skippable questions."

## Registry item types found (from registry.json), counts at fetch time

| `type` | Count | Examples |
| --- | --- | --- |
| `registry:style` | 2 | `index`, `style` |
| `registry:ui` | 54 | see table above |
| `registry:block` | 97 | chart variants (`chart-area-*`, `chart-bar-*`, `chart-line-*`, `chart-pie-*`, `chart-radar-*`, `chart-radial-*`, `chart-tooltip-*`), `dashboard-01`, `login-01`..`login-05`, `sidebar-01`..`sidebar-16`, `signup-01`..`signup-05` |
| `registry:lib` | 1 | `utils` |
| `registry:hook` | 1 | `use-mobile` |
| `registry:theme` | 5 | `theme-gray`, `theme-neutral`, `theme-slate`, `theme-stone`, `theme-zinc` |
| `registry:example` | 238 | demo/example source files (e.g. `button-demo`, `data-table-demo`, `field-demo`) that back the `<ComponentPreview>` blocks on doc pages |
| `registry:internal` | 13 | internal sidebar composition examples |

## Requested components confirmed present (install names)

sidebar, chart, calendar, `data-table` (guide, not an install item; see above), sonner, drawer, input-otp, carousel, resizable, toggle-group all confirmed as current registry items or doc pages as of the fetch date.
