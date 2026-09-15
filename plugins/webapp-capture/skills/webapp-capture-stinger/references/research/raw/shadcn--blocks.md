# Blocks

- URL: https://ui.shadcn.com/blocks (gallery) and https://ui.shadcn.com/docs/blocks (contribution guide)
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/(root)/_blocks.mdx`, `main` branch)
- Last updated (if shown): unknown

## What blocks are

Blocks are larger, ready-made compositions of components (a login page, a dashboard, a signup form, a full sidebar layout) distributed through the same registry mechanism as individual components, with `type: "registry:block"` in `registry.json`/`registry-item.json` (see `shadcn--registry-basics.md`). Per the docs: "We are inviting the community to contribute to the blocks library. Share your components and blocks with other developers and help build a library of high-quality, reusable components... We'd love to see all types of blocks: applications, marketing, products, and more."

Confirmed current block inventory (from `apps/v4/registry.json`, `type === "registry:block"`, 97 items total): chart blocks (`chart-area-*`, `chart-bar-*`, `chart-line-*`, `chart-pie-*`, `chart-radar-*`, `chart-radial-*`, `chart-tooltip-*` variants), `dashboard-01`, `login-01` through `login-05`, `sidebar-01` through `sidebar-16`, `signup-01` through `signup-05`. See `shadcn--components-index.md` for the full type-count table.

## How a block is added (as an end user)

Per the CLI docs (`shadcn--cli.md`), blocks are installed exactly like components, via `npx shadcn@latest add <block-name>` or by browsing https://ui.shadcn.com/blocks and copying the shown install command. Blocks can also be viewed before installing with `npx shadcn@latest view <block-name>`.

## How a block is added (as a contributor to shadcn/ui itself)

**Note on source freshness:** the contribution guide (`_blocks.mdx`) still describes the path `apps/www/registry/new-york/blocks`, but the live repository structure at fetch time uses `apps/v4/registry/bases/<base>/blocks` (see `shadcn--components-index.md`'s "Notes on source" section). The steps and concepts below are transcribed faithfully from the doc as written; treat the specific `apps/www/...` paths as potentially stale relative to the current `apps/v4/...` layout.

### Setup workspace

```bash
git clone https://github.com/shadcn-ui/ui.git
git checkout -b username/my-new-block
pnpm install
pnpm www:dev
```

### Add a block (as documented)

A block can be a single component (a variation of a ui component) or a complex component (e.g. a dashboard) with multiple components, hooks, and utils.

1. Create a new folder under `apps/www/registry/new-york/blocks` (kebab-case), e.g. `dashboard-01`. Per callout: "The build script will take care of building the block for the `default` style."
2. Add files to the block folder, e.g.:
   ```
   dashboard-01
   └── page.tsx
   └── components
       └── hello-world.tsx
       └── example-card.tsx
   └── hooks
       └── use-hello-world.ts
   └── lib
       └── format-date.ts
   ```
   Per callout: you can start with one file and add more later.

### Register the block

Add a block definition to `registry-blocks.tsx`, conforming to the `registry-item.json` schema (https://ui.shadcn.com/schema/registry-item.json):

```tsx title="apps/www/registry/registry-blocks.tsx" showLineNumbers
export const blocks = [
  // ...
  {
    name: "dashboard-01",
    author: "shadcn (https://ui.shadcn.com)",
    title: "Dashboard",
    description: "A simple dashboard with a hello world component.",
    type: "registry:block",
    registryDependencies: ["input", "button", "card"],
    dependencies: ["zod"],
    files: [
      {
        path: "blocks/dashboard-01/page.tsx",
        type: "registry:page",
        target: "app/dashboard/page.tsx",
      },
      {
        path: "blocks/dashboard-01/components/hello-world.tsx",
        type: "registry:component",
      },
      {
        path: "blocks/dashboard-01/components/example-card.tsx",
        type: "registry:component",
      },
      {
        path: "blocks/dashboard-01/hooks/use-hello-world.ts",
        type: "registry:hook",
      },
      {
        path: "blocks/dashboard-01/lib/format-date.ts",
        type: "registry:lib",
      },
    ],
    categories: ["dashboard"],
  },
]
```

Required fields per the guidelines below: `name`, `description`, `type`, `files`, `categories`.

### Build, view, and iterate

```bash
pnpm registry:build
```

Note: only needed when the block definition changes, not for every file edit.

View at `http://localhost:3333/blocks/[CATEGORY]`, or a full-screen preview at `http://localhost:3333/view/styles/new-york/dashboard-01`.

### Publish

```bash
pnpm registry:build
pnpm registry:capture
```

`registry:capture` captures light/dark screenshots (re-run after deleting existing screenshots at `apps/www/public/r/styles/new-york` if re-capturing). Then commit and submit a pull request; once merged, the block is published to the site and installable via the CLI.

## Categories

`categories` organizes a block in the registry. New categories are added to `registryCategories` in `apps/www/registry/registry-categories.ts`:

```tsx title="apps/www/registry/registry-categories.ts" showLineNumbers
export const registryCategories = [
  // ...
  {
    name: "Input",
    slug: "input",
    hidden: false,
  },
]
```

## Contribution guidelines (verbatim list from the page)

- Required block-definition properties: `name`, `description`, `type`, `files`, `categories`.
- List all registry dependencies in `registryDependencies` (the name of the component in the registry, e.g. `input`, `button`, `card`).
- List all npm dependencies in `dependencies` (e.g. `zod`, `sonner`).
- If a block has a page (optional), it should be the first entry in `files` and have a `target` property, so the CLI places it correctly for file-based routing.
- **Imports should always use the `@/registry` path**, e.g. `import { Input } from "@/registry/new-york/input"`.
