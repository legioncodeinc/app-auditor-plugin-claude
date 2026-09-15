# Registry: Getting Started, registry.json, registry-item.json

- URL: https://ui.shadcn.com/docs/registry/getting-started (primary); schema pages https://ui.shadcn.com/docs/registry/registry-json and https://ui.shadcn.com/docs/registry/registry-item-json
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/registry/getting-started.mdx`, `registry-json.mdx`, `registry-item-json.mdx`, `main` branch)
- Last updated (if shown): unknown

## What a registry is

A shadcn registry is a JSON payload (or set of JSON payloads) served over HTTP that the `shadcn` CLI can install components, hooks, utilities, and other files from. A registry can be a Next.js, Vite, Vue, Svelte, PHP, or any other framework project, as long as it serves JSON over HTTP; it can also simply be a public GitHub repository with a `registry.json` file at its root (see "GitHub Registries" docs, not separately archived here).

If you have an existing public GitHub repository, turning it into a registry only requires adding a `registry.json` at the root. A starter template exists at https://github.com/shadcn-ui/registry-template.

The only hard requirement: the registry catalog and its items must conform to the `registry.json` schema and the `registry-item.json` schema (both summarized below).

## registry.json

The entry point for a registry: name, homepage, and the items present.

```json title="registry.json" showLineNumbers
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "acme",
  "homepage": "https://acme.com",
  "items": [
    {
      "name": "button",
      "type": "registry:ui",
      "title": "Button",
      "description": "A simple button component.",
      "files": [
        {
          "path": "components/ui/button.tsx",
          "type": "registry:ui"
        }
      ]
    }
  ]
}
```

JSON Schema: https://ui.shadcn.com/schema/registry.json

### Definitions

- **$schema**: the schema URL, e.g. `"https://ui.shadcn.com/schema/registry.json"`.
- **name**: registry name, used for data attributes and other metadata, e.g. `"acme"`.
- **homepage**: the registry's homepage URL, used for metadata.
- **include**: composes a registry from other `registry.json` files, e.g.:
  ```json
  { "include": ["components/ui/registry.json", "hooks/registry.json"] }
  ```
  Each `include` path must be a relative path to an explicit `registry.json` file (folder shorthand is not supported). Included files may omit `name`/`homepage` (required only on the root file). When `shadcn build` resolves includes, item file paths are read relative to the `registry.json` that declares the item; the generated output is flattened and has no `include`. Item names must be unique across the whole resolved registry.
- **items**: the registry's items; each must satisfy the `registry-item.json` schema. The root `registry.json` must define at least one of `items` or `include`; if `items` is omitted it defaults to an empty array.

### Structuring a registry

**Option A: single `registry.json`.** All items in one `items` array at the project root. Simplest approach.

**Option B: `include`.** For larger registries, compose from multiple files, e.g.:

```
registry.json
components
└── ui
    ├── button.tsx
    ├── input.tsx
    └── registry.json
hooks
├── registry.json
├── use-media-query.ts
└── use-toggle.ts
```

The root `registry.json` defines registry metadata and `include`s the nested files.

## registry-item.json

Defines a single registry item.

```json title="registry-item.json" showLineNumbers
{
  "$schema": "https://ui.shadcn.com/schema/registry-item.json",
  "name": "hello-world",
  "type": "registry:block",
  "title": "Hello World",
  "description": "A simple hello world component.",
  "registryDependencies": [
    "button",
    "@acme/input-form",
    "https://example.com/r/foo"
  ],
  "dependencies": ["is-even@3.0.0", "motion"],
  "devDependencies": ["tw-animate-css"],
  "files": [
    {
      "path": "registry/new-york/hello-world/hello-world.tsx",
      "type": "registry:component"
    },
    {
      "path": "registry/new-york/hello-world/use-hello-world.ts",
      "type": "registry:hook"
    }
  ],
  "cssVars": {
    "theme": {
      "font-heading": "Poppins, sans-serif"
    },
    "light": {
      "brand": "oklch(0.205 0.015 18)"
    },
    "dark": {
      "brand": "oklch(0.205 0.015 18)"
    }
  }
}
```

JSON Schema: https://ui.shadcn.com/schema/registry-item.json

### Field reference

- **$schema**: schema URL.
- **name**: unique item identifier within the registry.
- **title**: short human-readable title.
- **description**: longer, more detailed description than `title`.
- **type**: determines the item's type and target install path. Supported values:

  | Type | Description |
  | --- | --- |
  | `registry:base` | Use for entire design systems. |
  | `registry:block` | Use for complex components with multiple files. |
  | `registry:component` | Use for simple components. |
  | `registry:font` | Use for fonts. |
  | `registry:lib` | Use for lib and utils. |
  | `registry:hook` | Use for hooks. |
  | `registry:ui` | Use for UI components and single-file primitives. |
  | `registry:page` | Use for page or file-based routes. |
  | `registry:file` | Use for miscellaneous files. |
  | `registry:style` | Use for registry styles, e.g. `new-york`. |
  | `registry:theme` | Use for themes. |
  | `registry:item` | Use for universal registry items. |

- **author**: e.g. `"John Doe <john@doe.com>"`.
- **dependencies**: npm packages, optionally versioned with `@version`, e.g. `["@radix-ui/react-accordion", "zod", "lucide-react", "name@1.0.2"]`.
- **devDependencies**: npm dev-only packages, e.g. `["tw-animate-css", "name@1.2.0"]`.
- **registryDependencies**: other registry items this item depends on. Address forms:
  - Bare name for `shadcn/ui` items: `["button", "input", "select"]`.
  - Namespaced items: `["@acme/input-form"]`.
  - GitHub registry items: `["owner/repo/item-name"]`; for published/reproducible registries, prefer a tag or full commit SHA: `["acme/ui/button#v1.2.0"]`.
  - Custom registry items: full URL, e.g. `["https://example.com/r/hello-world.json"]`.
  - Local files: relative path, e.g. `["./hello-world.json"]`.

  Note: bare names keep existing behavior, i.e. `button` always means the built-in shadcn `button` item, never an item of the same name from the current GitHub repository; for same-repo GitHub dependencies use the full `owner/repo/item-name` address. Refs are not inherited across dependencies; pin a GitHub dependency to a tag or commit SHA for reproducibility.

- **files**: each entry has `path`, `type`, and optional `target`. `target` is *required* for `registry:page` and `registry:file` types.

  ```json
  {
    "files": [
      {
        "path": "registry/new-york/hello-world/page.tsx",
        "type": "registry:page",
        "target": "app/hello/page.tsx"
      },
      {
        "path": "registry/new-york/hello-world/hello-world.tsx",
        "type": "registry:component"
      },
      {
        "path": "registry/new-york/hello-world/use-hello-world.ts",
        "type": "registry:hook"
      },
      {
        "path": "registry/new-york/hello-world/.env",
        "type": "registry:file",
        "target": "~/.env"
      }
    ]
  }
  ```

  - `path`: path to the file in the source registry; used by the build script.
  - `type`: same enum as the item `type`.
  - `target`: where the file lands in the consuming project. By default the CLI reads the project's `components.json` to determine the target; for routes/config, set it explicitly. `~` refers to project root, e.g. `~/foo.config.js`.

  **Registry target placeholders** (only at the start of `target`, independent of the project's import prefix):

  | Placeholder | Resolves to |
  | --- | --- |
  | `@components/` | `aliases.components` |
  | `@ui/` | `aliases.ui` |
  | `@lib/` | `aliases.lib` |
  | `@hooks/` | `aliases.hooks` |

  These let an item install into the user's configured shadcn directories regardless of whether the project imports with `@/`, `#`, package imports, or workspace exports. Anything after the placeholder is preserved (`@ui/ai/prompt-input.tsx` installs at `ai/prompt-input.tsx` under the configured `ui` directory). `target` can point to a different shadcn directory than the file's own `type` (e.g. a `registry:ui` file targeted at `@lib/format-date.ts`). Unknown placeholders (`@foo/bar.ts`) are written as regular paths (`foo/bar.ts`); embedded placeholders (`components/@ui/button.tsx`) are also treated as regular paths. `@utils/` is not supported because `utils` points to a file, not a directory.

- **tailwind** (DEPRECATED: use `cssVars.theme` instead for Tailwind v4 projects): `theme`, `plugins`, `content` config, e.g. colors/keyframes/animation additions.
- **cssVars**: CSS variables for the item, under `theme`, `light`, `dark` keys, e.g.:
  ```json
  {
    "cssVars": {
      "theme": { "font-heading": "Poppins, sans-serif" },
      "light": { "brand": "20 14.3% 4.1%", "radius": "0.5rem" },
      "dark": { "brand": "20 14.3% 4.1%" }
    }
  }
  ```
- **css**: adds new CSS rules to the project's CSS file, e.g. `@layer base`, `@layer components`, `@utility`, `@keyframes`, `@plugin`.
  ```json
  {
    "css": {
      "@plugin @tailwindcss/typography": {},
      "@plugin foo": {},
      "@layer base": { "body": { "font-size": "var(--text-base)", "line-height": "1.5" } },
      "@layer components": { "button": { "background-color": "var(--color-primary)", "color": "var(--color-white)" } },
      "@utility text-magic": { "font-size": "var(--text-base)", "line-height": "1.5" },
      "@keyframes wiggle": { "0%, 100%": { "transform": "rotate(-3deg)" }, "50%": { "transform": "rotate(3deg)" } }
    }
  }
  ```
- **envVars**: environment variables added to `.env.local`/`.env` (existing variables are not overwritten). Intended for development/example variables, not production secrets.
  ```json
  {
    "envVars": {
      "NEXT_PUBLIC_APP_URL": "http://localhost:4000",
      "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/postgres",
      "OPENAI_API_KEY": ""
    }
  }
  ```
- **font**: required for `registry:font` items.

  | Property | Type | Required | Description |
  | --- | --- | --- | --- |
  | `family` | `string` | Yes | The CSS font-family value. |
  | `provider` | `string` | Yes | The font provider. Currently only `google` is supported. |
  | `import` | `string` | Yes | The import name for the font from `next/font/google`. |
  | `variable` | `string` | Yes | The CSS variable name for the font (e.g. `--font-sans`, `--font-mono`). |
  | `weight` | `string[]` | No | Array of font weights to include. |
  | `subsets` | `string[]` | No | Array of font subsets to include. |
  | `selector` | `string` | No | CSS selector to apply the font to. Defaults to `html`. |
  | `dependency` | `string` | No | The npm package to install for non-Next.js projects (e.g. `@fontsource-variable/inter`). |

  ```json
  {
    "font": {
      "family": "'Inter Variable', sans-serif",
      "provider": "google",
      "import": "Inter",
      "variable": "--font-sans",
      "subsets": ["latin"],
      "dependency": "@fontsource-variable/inter"
    }
  }
  ```

- **docs**: custom documentation/message shown by the CLI when installing, e.g. `"To get an OPENAI_API_KEY, sign up for an account at https://platform.openai.com."`
- **categories**: organizes the item, e.g. `["sidebar", "dashboard"]`.
- **meta**: arbitrary additional key/value metadata, e.g. `{"foo": "bar"}`.

## CLI commands that touch the registry (cross-reference)

See `shadcn--cli.md` for full option tables: `add @namespace/item` (install from a namespaced registry), `view`, `search`/`list`, `build` (turns a source `registry.json` into served JSON, default output `./public/r`), and the `registries` block in `components.json` (see `shadcn--components-json.md`) for configuring private/namespaced registries with headers and params.
