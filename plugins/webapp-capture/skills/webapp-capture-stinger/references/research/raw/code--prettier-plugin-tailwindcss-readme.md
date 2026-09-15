# prettier-plugin-tailwindcss

- URL: https://github.com/tailwindlabs/prettier-plugin-tailwindcss
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): unknown

Content extracted verbatim (with minor reformatting) from https://raw.githubusercontent.com/tailwindlabs/prettier-plugin-tailwindcss/main/README.md

## Description

A [Prettier v3+](https://prettier.io/) plugin for Tailwind CSS v3.0+ that automatically sorts classes based on [our recommended class order](https://tailwindcss.com/blog/automatic-class-sorting-with-prettier#how-classes-are-sorted).

## Installation

```sh
npm install -D prettier prettier-plugin-tailwindcss
```

Then add the plugin to your Prettier configuration:

```json5
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

When using a JavaScript config, you can import the types for IntelliSense:

```js
// prettier.config.js

/** @type {import('prettier').Config & import('prettier-plugin-tailwindcss').PluginOptions} */
export default {
  plugins: ["prettier-plugin-tailwindcss"],
}
```

## Upgrading to v0.5.x

As of v0.5.x, this plugin now requires Prettier v3 and is ESM-only. This means it cannot be loaded via `require()`.

## Options

### Specifying your Tailwind stylesheet path (Tailwind CSS v4+)

When using Tailwind CSS v4 you must specify your CSS file entry point, which includes your theme, custom utilities, and other Tailwind configuration options. To do this, use the `tailwindStylesheet` option in your Prettier configuration.

Note that paths are resolved relative to the Prettier configuration file.

```json5
// .prettierrc
{
  "tailwindStylesheet": "./resources/css/app.css"
}
```

### Specifying your Tailwind JavaScript config path (Tailwind CSS v3)

To ensure that the class sorting takes into consideration any of your project's Tailwind customizations, it needs access to your Tailwind configuration file (`tailwind.config.js`).

By default the plugin will look for this file in the same directory as your Prettier configuration file. However, if your Tailwind configuration is somewhere else, you can specify this using the `tailwindConfig` option in your Prettier configuration.

```json5
// .prettierrc
{
  "tailwindConfig": "./styles/tailwind.config.js"
}
```

If a local configuration file cannot be found the plugin will fallback to the default Tailwind configuration.

## Sorting non-standard attributes

By default this plugin sorts classes in the `class` attribute, any framework-specific equivalents like `className`, `:class`, `[ngClass]`, and any Tailwind `@apply` directives.

You can sort additional attributes using the `tailwindAttributes` option, which takes an array of attribute names:

```json5
// .prettierrc
{
  "tailwindAttributes": ["myClassList"]
}
```

### Using regex patterns

You can also use regular expressions to match multiple attributes. Patterns should be enclosed in forward slashes. Note that JS regex literals are not supported with Prettier:

```json5
// .prettierrc
{
  "tailwindAttributes": ["myClassList", "/data-.*/"]
}
```

## Sorting classes in function calls

In addition to sorting classes in attributes, you can also sort classes in strings provided to function calls. This is useful when working with libraries like clsx or cva.

You can sort classes in function calls using the `tailwindFunctions` option, which takes a list of function names:

```json5
// .prettierrc
{
  "tailwindFunctions": ["clsx"]
}
```

## Sorting classes in template literals

This plugin also enables sorting of classes in tagged template literals, using the same `tailwindFunctions` option:

```json5
// .prettierrc
{
  "tailwindFunctions": ["tw"],
}
```

This can be used with third-party libraries like `twrnc` or a custom "identity" tagged template function:

```js
const tw = (strings, ...values) => String.raw({ raw: strings }, ...values)
```

## Public API

If you want to use the Tailwind class sorting logic outside of Prettier, import from the `sorter` entrypoint:

```js
import { createSorter } from 'prettier-plugin-tailwindcss/sorter'

let sorter = await createSorter({
  base: '/path/to/project',
  stylesheetPath: './app.css',
})

// Sort HTML class attributes (space-separated strings)
let sorted = sorter.sortClassAttributes([
  'sm:bg-tomato bg-red-500',
  'p-4 m-2'
])
// Returns: ['bg-red-500 sm:bg-tomato', 'm-2 p-4']

// Sort class lists (arrays of class names)
let sortedLists = sorter.sortClassLists([
  ['sm:bg-tomato', 'bg-red-500'],
  ['p-4', 'm-2']
])
// Returns: [['bg-red-500', 'sm:bg-tomato'], ['m-2', 'p-4']]
```

### API Options

The `createSorter` function accepts the following options:

- `base` (optional): The directory used to resolve relative file paths. Defaults to the current working directory.
- `filepath` (optional): The path to the file being formatted. When provided, Tailwind CSS is resolved relative to this path.
- `configPath` (optional): Path to the Tailwind CSS config file (v3). Paths are resolved relative to `base`.
- `stylesheetPath` (optional): Path to the CSS stylesheet used by Tailwind CSS (v4+). Paths are resolved relative to `base`.
- `preserveWhitespace` (optional): Whether to preserve whitespace around classes. Default: `false`.
- `preserveDuplicates` (optional): Whether to preserve duplicate classes. Default: `false`.

### Sorter Methods

- `sortClassAttributes(classes: string[]): string[]` — sorts one or more HTML class attributes (space-separated strings).
- `sortClassLists(classes: string[][]): (string | null)[][]` — sorts one or more class lists (arrays of individual class names). When removing duplicates (default behavior), duplicate classes are replaced with `null` in the output.

## Preserving whitespace

This plugin automatically removes unnecessary whitespace between classes to ensure consistent formatting. If you prefer to preserve whitespace, you can use the `tailwindPreserveWhitespace` option:

```json5
// .prettierrc
{
  "tailwindPreserveWhitespace": true,
}
```

## Preserving duplicate classes

This plugin automatically removes duplicate classes from your class lists. However, this can cause issues in some templating languages, like Fluid or Blade, where classes and templating syntax can't be distinguished.

If removing duplicate classes is causing issues in your project, you can use the `tailwindPreserveDuplicates` option to disable this behavior:

```json5
// .prettierrc
{
  "tailwindPreserveDuplicates": true,
}
```

## Compatibility with other Prettier plugins

This plugin uses Prettier APIs that can only be used by one plugin at a time, making it incompatible with other Prettier plugins implemented the same way. To solve this, explicit per-plugin workarounds enable compatibility with:

- `@ianvs/prettier-plugin-sort-imports`
- `@prettier/plugin-pug`
- `@shopify/prettier-plugin-liquid`
- `@trivago/prettier-plugin-sort-imports`
- `prettier-plugin-astro`
- `prettier-plugin-css-order`
- `prettier-plugin-jsdoc`
- `prettier-plugin-multiline-arrays`
- `prettier-plugin-organize-attributes`
- `prettier-plugin-organize-imports`
- `prettier-plugin-svelte`
- `prettier-plugin-sort-imports`

One limitation with this approach is that `prettier-plugin-tailwindcss` *must* be loaded last:

```json5
// .prettierrc
{
  // ..
  "plugins": [
    "prettier-plugin-svelte",
    "prettier-plugin-organize-imports",
    "prettier-plugin-tailwindcss" // MUST come last
  ]
}
```
