# components.json

- URL: https://ui.shadcn.com/docs/components-json
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/(root)/components-json.mdx`, `main` branch)
- Last updated (if shown): unknown

## Summary

`components.json` holds configuration for a project so the CLI understands how the project is set up and can generate customized components. It is optional: only required when using the CLI (not needed for pure copy-paste usage).

Create it with:

```bash
npx shadcn@latest init
```

## $schema

```json title="components.json"
{
  "$schema": "https://ui.shadcn.com/schema.json"
}
```

JSON Schema is published at https://ui.shadcn.com/schema.json.

## style

The style for components. **Cannot be changed after initialization.**

```json title="components.json"
{
  "style": "new-york"
}
```

**The `default` style has been deprecated. Use `new-york` instead.** (Note: per `shadcn--cli.md`, `init --defaults` currently resolves to `--preset=nova`, suggesting a newer preset-based naming layer beyond the two classic `default`/`new-york` style names; the `components-json.mdx` page itself, at fetch time, still documents only `style: "new-york"` as the example/recommended value.)

## tailwind

Configuration that helps the CLI understand how Tailwind CSS is set up.

### tailwind.config

Path to `tailwind.config.js`/`.ts`. **For Tailwind CSS v4, leave this blank.**

```json title="components.json"
{
  "tailwind": {
    "config": "tailwind.config.js" | "tailwind.config.ts"
  }
}
```

### tailwind.css

Path to the CSS file that imports Tailwind CSS into the project.

```json title="components.json"
{
  "tailwind": {
    "css": "styles/global.css"
  }
}
```

### tailwind.baseColor

Used to generate the default theme tokens for components. **Cannot be changed after initialization.**

```json title="components.json"
{
  "tailwind": {
    "baseColor": "neutral" | "stone" | "zinc" | "mauve" | "olive" | "mist" | "taupe"
  }
}
```

(This enum is the current, expanded base-color list; see `shadcn--theming.md` for the corresponding "Base Colors" prose, which lists the same seven names: Neutral, Stone, Zinc, Mauve, Olive, Mist, Taupe.)

### tailwind.cssVariables

Set `true` to generate semantic theme tokens (`background`, `foreground`, `primary`, ...). Set `false` to generate inline Tailwind color utilities instead.

```json title="components.json"
{
  "tailwind": {
    "cssVariables": true
  }
}
```

See `shadcn--theming.md` for details. **Cannot be changed after initialization**; switching requires deleting and reinstalling components.

### tailwind.prefix

Prefix for Tailwind CSS utility classes; components are added with this prefix.

```json title="components.json"
{
  "tailwind": {
    "prefix": "tw-"
  }
}
```

## rsc

Whether to enable React Server Components support. The CLI automatically adds a `use client` directive to client components when `true`.

```json title="components.json"
{
  "rsc": true
}
```

## tsx

Choose TypeScript or JavaScript components. `false` allows components to be added as JavaScript with the `.jsx` extension.

```json title="components.json"
{
  "tsx": true
}
```

## aliases

The CLI uses these values to place generated components correctly and rewrite imports. They can be backed by either:

1. `compilerOptions.paths` in `tsconfig.json`/`jsconfig.json`, or
2. `package.json#imports` with TypeScript package import resolution enabled.

The `aliases` in `components.json` are still required when using the CLI: they tell the CLI which import roots map to `components`, `ui`, `lib`, `hooks`, and `utils`.

**Important:** If using package imports, enable `resolvePackageJsonImports` and use `moduleResolution: "bundler"` in `tsconfig.json`. If using `paths`, make sure aliases include the `src` directory when applicable.

### Using tsconfig/jsconfig paths

```json title="tsconfig.json"
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Using package.json#imports

```json title="package.json"
{
  "imports": {
    "#components/*": "./src/components/*.tsx",
    "#lib/*": "./src/lib/*.ts",
    "#hooks/*": "./src/hooks/*.ts"
  }
}
```

```json title="tsconfig.json"
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "resolvePackageJsonImports": true
  }
}
```

```json title="components.json"
{
  "aliases": {
    "components": "#components",
    "ui": "#components/ui",
    "lib": "#lib",
    "hooks": "#hooks",
    "utils": "#lib/utils"
  }
}
```

`aliases` in `components.json` still tells the CLI where to place `components`, `ui`, `lib`, `hooks`, and `utils`; `package.json#imports` provides runtime and TypeScript resolution for the `#...` specifiers.

Whether generated `#...` imports keep file extensions depends on the matched `imports` target:

- `"#components/*": "./src/components/*"` preserves source extensions: `#components/button.tsx`
- `"#components/*": "./src/components/*.tsx"` strips them: `#components/button`

For monorepos: local workspace aliases can use `package.json#imports`; shared workspace imports such as `@workspace/ui/components` resolve from the target package's `exports`.

### aliases.utils

```json title="components.json"
{
  "aliases": {
    "utils": "@/lib/utils"
  }
}
```

### aliases.components

```json title="components.json"
{
  "aliases": {
    "components": "@/components"
  }
}
```

### aliases.ui

The CLI uses `aliases.ui` to determine where to place `ui` components. Use to customize the installation directory.

```json title="components.json"
{
  "aliases": {
    "ui": "@/app/ui"
  }
}
```

### aliases.lib

Import alias for `lib` functions such as `format-date` or `generate-id`.

```json title="components.json"
{
  "aliases": {
    "lib": "@/lib"
  }
}
```

### aliases.hooks

Import alias for `hooks` such as `use-media-query` or `use-toast`.

```json title="components.json"
{
  "aliases": {
    "hooks": "@/hooks"
  }
}
```

## registries

Configure multiple resource registries for a project: install components, libraries, utilities, and other resources from various sources including private registries.

### Basic configuration

```json title="components.json"
{
  "registries": {
    "@v0": "https://v0.dev/chat/b/{name}",
    "@acme": "https://registry.acme.com/{name}.json",
    "@internal": "https://internal.company.com/{name}.json"
  }
}
```

`{name}` is replaced with the resource name when installing.

### Advanced configuration with authentication

```json title="components.json"
{
  "registries": {
    "@private": {
      "url": "https://api.company.com/registry/{name}.json",
      "headers": {
        "Authorization": "Bearer ${REGISTRY_TOKEN}",
        "X-API-Key": "${API_KEY}"
      },
      "params": {
        "version": "latest"
      }
    }
  }
}
```

Environment variables in `${VAR_NAME}` format are expanded automatically.

### Using namespaced registries

```bash
# Install from a configured registry
npx shadcn@latest add @v0/dashboard

# Install from private registry
npx shadcn@latest add @private/button

# Install multiple resources
npx shadcn@latest add @acme/header @internal/auth-utils
```

### Example: multiple registry setup

```json title="components.json"
{
  "registries": {
    "@shadcn": "https://ui.shadcn.com/r/{name}.json",
    "@company-ui": {
      "url": "https://registry.company.com/ui/{name}.json",
      "headers": {
        "Authorization": "Bearer ${COMPANY_TOKEN}"
      }
    },
    "@team": {
      "url": "https://team.company.com/{name}.json",
      "params": {
        "team": "frontend",
        "version": "${REGISTRY_VERSION}"
      }
    }
  }
}
```

## iconLibrary

Not documented as a top-level key on this specific page at fetch time, but the `iconLibrary` field is referenced directly by the CLI's `migrate icons` command (see `shadcn--cli.md`): running `migrate icons` "update[s] `iconLibrary` in your `components.json` so future `npx shadcn add` installs use the new library." Supported values (per the migration's supported-libraries list): `lucide`, `tabler`, `hugeicons`, `phosphor`, `remixicon`, and `radix` (legacy).
