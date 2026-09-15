# shadcn (CLI)

- URL: https://ui.shadcn.com/docs/cli
- Fetched: 2026-09-15
- Source type: official docs (raw MDX transcribed from `shadcn-ui/ui`, `apps/v4/content/docs/(root)/cli.mdx`, `main` branch)
- Last updated (if shown): unknown. The `eject` command's example output references `shadcn@4.8.3` as the version being ejected from, which is evidence of the CLI's current major/minor version at fetch time.

## init

Initializes configuration and dependencies for an existing project, or creates a new project with `--name`. Installs dependencies, adds the `cn` util, and configures CSS variables.

```bash
npx shadcn@latest init
```

**Options**

```
Usage: shadcn init [options] [components...]

initialize your project and install dependencies

Arguments:
  components                 names, url or local path to component

Options:
  -t, --template <template>  the template to use. (next, vite, start, react-router, laravel, astro)
  -b, --base <base>          the component library to use. (base, radix, aria)
  -p, --preset [name]        use a preset configuration
  -y, --yes                  skip confirmation prompt. (default: true)
  -d, --defaults             use default configuration: --template=next --preset=nova (default: false)
  -f, --force                force overwrite of existing configuration. (default: false)
  -c, --cwd <cwd>            the working directory. defaults to the current directory.
  -n, --name <name>          the name for the new project.
  -s, --silent               mute output. (default: false)
  --css-variables            use css variables for theming. (default: true)
  --no-css-variables         do not use css variables for theming.
  --monorepo                 scaffold a monorepo project.
  --no-monorepo              skip the monorepo prompt.
  --rtl                      enable RTL support.
  --no-rtl                   disable RTL support.
  --pointer                  enable pointer cursor for buttons.
  --no-pointer                disable pointer cursor for buttons.
  --reinstall                re-install existing UI components.
  --no-reinstall              do not re-install existing UI components.
  -h, --help                 display help for command
```

`create` is an alias for `init`: `npx shadcn@latest create`.

Note: `-b, --base <base>` (`base`, `radix`, or `aria`) selects which underlying primitive library the generated components use. `-p, --preset [name]` and `-d, --defaults` (which resolves to `--preset=nova`) reflect a newer "preset" system layered on top of the classic `style` concept (see `shadcn--components-json.md`).

## add

Adds components and dependencies to the project.

```bash
npx shadcn@latest add [component]
```

**Options**

```
Usage: shadcn add [options] [components...]

add a component to your project

Arguments:
  components           name, url or local path to component

Options:
  -y, --yes            skip confirmation prompt. (default: false)
  -o, --overwrite      overwrite existing files. (default: false)
  -c, --cwd <cwd>      the working directory. defaults to the current directory.
  -a, --all            add all available components (default: false)
  -p, --path <path>    the path to add the component to.
  -s, --silent         mute output. (default: false)
  --dry-run            preview changes without writing files. (default: false)
  --diff [path]        show diff for a file.
  --view [path]        show file contents.
  -h, --help           display help for command
```

## apply

Applies a preset to an existing project.

```bash
npx shadcn@latest apply a2r6bw
```

Apply only the theme or fonts from a preset without reinstalling UI components:

```bash
npx shadcn@latest apply a2r6bw --only theme
```

Supported values for `--only`: `theme`, `font`.

**Options**

```
Usage: shadcn apply [options] [preset]

apply a preset to an existing project

Arguments:
  preset             the preset to apply

Options:
  --preset <preset>  preset configuration to apply
  --only [parts]     apply only parts of a preset: theme, font
  -y, --yes          skip confirmation prompt. (default: false)
  -c, --cwd <cwd>    the working directory. defaults to the current directory.
  -s, --silent       mute output. (default: false)
  -h, --help         display help for command
```

## preset

Inspects preset codes and resolves the preset for an existing project.

```bash
npx shadcn@latest preset decode a2r6bw
```

### preset decode

```bash
npx shadcn@latest preset decode a2r6bw
```

```
Usage: shadcn preset decode [options] <code>

decode a preset code

Arguments:
  code        the preset code to decode

Options:
  --json      output as JSON. (default: false)
  -h, --help  display help for command
```

### preset resolve

```bash
npx shadcn@latest preset resolve
```

`preset info` is an alias: `npx shadcn@latest preset info`.

```
Usage: shadcn preset resolve|info [options]

resolve a preset from your project

Options:
  -c, --cwd <cwd>  the working directory. defaults to the current directory.
  --json            output as JSON. (default: false)
  -h, --help        display help for command
```

### preset url

```bash
npx shadcn@latest preset url a2r6bw
```

```
Usage: shadcn preset url [options] <code>

get the create URL for a preset code

Arguments:
  code        the preset code

Options:
  -h, --help  display help for command
```

### preset open

```bash
npx shadcn@latest preset open a2r6bw
```

```
Usage: shadcn preset open [options] <code>

open a preset code in the browser

Arguments:
  code        the preset code

Options:
  -h, --help  display help for command
```

## view

Views registry items before installing.

```bash
npx shadcn@latest view [item]
npx shadcn@latest view button card dialog
npx shadcn@latest view @acme/auth @v0/dashboard
```

```
Usage: shadcn view [options] <items...>

view items from the registry

Arguments:
  items            the item names or URLs to view

Options:
  -c, --cwd <cwd>  the working directory. defaults to the current directory.
  -h, --help       display help for command
```

## search

Searches for items from registries.

```bash
npx shadcn@latest search [registry]
npx shadcn@latest search @shadcn -q "button"
npx shadcn@latest search @shadcn @v0 @acme
```

`list` is an alias for `search`: `npx shadcn@latest list @acme`.

```
Usage: shadcn search|list [options] <registries...>

search items from registries

Arguments:
  registries             the registry names or urls to search items from. Names
                         must be prefixed with @.

Options:
  -c, --cwd <cwd>        the working directory. defaults to the current directory.
  -q, --query <query>    query string
  -l, --limit <number>   maximum number of items to display per registry (default: "100")
  -o, --offset <number>  number of items to skip (default: "0")
  -h, --help             display help for command
```

## build

Generates registry JSON files.

```bash
npx shadcn@latest build
```

Reads `registry.json` and generates registry JSON files in `public/r`.

```
Usage: shadcn build [options] [registry]

build components for a shadcn registry

Arguments:
  registry             path to registry.json file (default: "./registry.json")

Options:
  -o, --output <path>  destination directory for json files (default: "./public/r")
  -c, --cwd <cwd>      the working directory. defaults to the current directory.
  -h, --help           display help for command
```

Custom output directory:

```bash
npx shadcn@latest build --output ./public/registry
```

## docs

Fetches documentation and API references for components.

```bash
npx shadcn@latest docs [component]
```

```
Usage: shadcn docs [options] [component]

fetch documentation and API references for components

Arguments:
  component          the component to get docs for

Options:
  -c, --cwd <cwd>    the working directory. defaults to the current directory.
  -b, --base <base>  the base to use: base, radix, or aria. defaults to project base.
  --json             output as JSON. (default: false)
  -h, --help         display help for command
```

## info

Gets information about the project.

```bash
npx shadcn@latest info
```

```
Usage: shadcn info [options]

get information about your project

Options:
  -c, --cwd <cwd>  the working directory. defaults to the current directory.
  --json            output as JSON. (default: false)
  -h, --help        display help for command
```

## migrate

Runs migrations on the project.

```bash
npx shadcn@latest migrate [migration]
```

**Available migrations**

| Migration | Description |
| --- | --- |
| `cn` | Migrate `clsx` and `tailwind-merge` to `cn`. |
| `icons` | Migrate UI components to a different icon library. |
| `base-color` | Migrate the theme to a different base color. |
| `radix` | Migrate to radix-ui (the unified package). |
| `rtl` | Migrate components to support RTL (right-to-left). |

```
Usage: shadcn migrate [options] [migration] [path]

run a migration.

Arguments:
  migration          the migration to run.
  path               optional path or glob pattern to migrate.

Options:
  -c, --cwd <cwd>    the working directory. defaults to the current directory.
  -l, --list         list all migrations. (default: false)
  -y, --yes          skip confirmation prompt. (default: false)
  -f, --from <name>  the base color or icon library to migrate from.
  -t, --to <name>    the base color or icon library to migrate to.
  -h, --help         display help for command
```

### migrate cn

Replaces `clsx`, `tailwind-merge`, and `cnfast` with the `cn` package (https://github.com/shadcn-ui/cn).

```bash
npx shadcn@latest migrate cn
```

Does not require `components.json`; works in any JS/TS package using Tailwind CSS v4. It rewrites imports from `clsx`, `clsx/lite`, `tailwind-merge`, `cnfast`; replaces `twMerge(clsx(...))` compositions with direct `cn(...)` calls; replaces the standard shadcn utility with a direct re-export; installs `cn` and removes old packages when no references remain.

Before:

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

After:

```tsx
export { cn } from "cn"
```

Preserves separate APIs when used independently:

```diff
- import { clsx } from "clsx"
- import { twMerge } from "tailwind-merge"
+ import { clsx, twMerge } from "cn"
```

`cnfast` module specifiers replaced directly (same root API):

```diff
- import { cn } from "cnfast"
+ import { cn } from "cn"
```

Custom configuration APIs move to `cn/config`:

```diff
- import { createTailwindMerge, getDefaultConfig } from "tailwind-merge"
+ import {
+   createTwMerge as createTailwindMerge,
+   defaultConfig as getDefaultConfig,
+ } from "cn/config"
```

**Caution (per page):** The `cn` merge engine supports Tailwind CSS v4, like `tailwind-merge` v3. Projects using Tailwind CSS v3 should continue using `tailwind-merge` v2. A `clsx`-only migration is safe in a Tailwind CSS v3 project.

Migrate specific files/globs:

```bash
npx shadcn@latest migrate cn src/lib/utils.ts
npx shadcn@latest migrate cn "src/**/*.{ts,tsx}"
```

Scoped migrations install `cn` but keep the old packages in `package.json` (other files may still use them). Unsupported imports (`experimentalParseClassName`, namespace imports, dynamic import shapes, direct calls to `validators`, variadic `createTailwindMerge` calls) are left unchanged and reported for manual review.

### migrate icons

Moves components from one icon library to another.

```bash
npx shadcn@latest migrate icons
```

Prompts for source/target libraries, rewrites icon imports and JSX usage in the `ui` directory, installs the target library, updates `iconLibrary` in `components.json`.

Supported libraries: `lucide`, `tabler`, `hugeicons`, `phosphor`, `remixicon`, `radix` (legacy).

Non-interactive:

```bash
npx shadcn@latest migrate icons --from lucide --to phosphor --yes
```

Specific files/globs (scoped runs do not update `components.json`):

```bash
npx shadcn@latest migrate icons src/components/ui/button.tsx --from lucide --to tabler
npx shadcn@latest migrate icons "src/components/**" --from lucide --to tabler
```

Icons without a target-library equivalent are left untouched and reported at the end.

### migrate base-color

Switches the theme's base color.

```bash
npx shadcn@latest migrate base-color
```

Prompts for source/target base colors, rewrites the theme CSS variables (the file configured by `tailwind.css`), updates `baseColor`.

Supported base colors: `neutral`, `zinc`, `stone`, `mauve`, `olive`, `mist`, `taupe`.

Non-interactive:

```bash
npx shadcn@latest migrate base-color --to zinc --yes
```

Theme tokens that no longer match the source base color are left untouched and reported.

### migrate rtl

Transforms components to support RTL languages.

```bash
npx shadcn@latest migrate rtl
```

1. Updates `components.json` to set `rtl: true`.
2. Transforms physical CSS properties to logical equivalents (e.g. `ml-4` -> `ms-4`, `text-left` -> `text-start`).
3. Adds `rtl:` variants where needed (e.g. `space-x-4` -> `space-x-4 rtl:space-x-reverse`).

Specific files/globs:

```bash
npx shadcn@latest migrate rtl src/components/ui/button.tsx
npx shadcn@latest migrate rtl "src/components/ui/**"
```

With no path, transforms all files in the `ui` directory (from `components.json`).

### migrate radix

Updates imports from individual `@radix-ui/react-*` packages to the unified `radix-ui` package.

```bash
npx shadcn@latest migrate radix
```

1. Transforms imports from `@radix-ui/react-*` to `radix-ui`.
2. Adds the `radix-ui` package to `package.json`.

Before:

```tsx
import * as DialogPrimitive from "@radix-ui/react-dialog"
import * as SelectPrimitive from "@radix-ui/react-select"
```

After:

```tsx
import { Dialog as DialogPrimitive, Select as SelectPrimitive } from "radix-ui"
```

Specific files/globs:

```bash
npx shadcn@latest migrate radix src/components/ui/dialog.tsx
npx shadcn@latest migrate radix "src/components/ui/**"
```

With no path, transforms all files in the `ui` directory. Afterward, unused `@radix-ui/react-*` packages can be removed from `package.json`.

## eject

`init` adds `@import "shadcn/tailwind.css"` to the global CSS file. This import provides shared Tailwind v4 utilities (custom variants like `data-open:`, `data-closed:`, and accordion animations).

`eject` inlines `shadcn/tailwind.css` into the global CSS file and removes the `shadcn` dependency.

**Note (irreversible):** After ejecting, future shadcn CLI updates to `shadcn/tailwind.css` will not apply automatically.

```bash
npx shadcn@latest eject
```

Before:

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
```

After (excerpt; version shown is illustrative of the CLI's current release line):

```css
@import "tailwindcss";
@import "tw-animate-css";
/* ejected from shadcn@4.8.3 */
@theme inline {
  @keyframes accordion-down {
    from {
      height: 0;
    }
    to {
      height: var(
        --radix-accordion-content-height,
        var(--accordion-panel-height, auto)
      );
    }
  }
}

@custom-variant data-open {
  &:where([data-state="open"]),
  &:where([data-open]:not([data-open="false"])) {
    @slot;
  }
}

@utility no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}
```

Monorepo: run from the workspace containing `components.json` and the global CSS file:

```bash
npx shadcn@latest eject -c packages/ui
```

**Options**

```
Usage: shadcn eject [options]

inline shadcn/tailwind.css and remove the shadcn dependency

Options:
  -c, --cwd <cwd>  the working directory. defaults to the current directory.
  -y, --yes        skip confirmation prompt. (default: false)
  -s, --silent     mute output. (default: false)
  -h, --help       display help for command
```
