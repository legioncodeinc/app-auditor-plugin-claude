# Styling with utility classes - Using arbitrary values | Tailwind CSS

- URL: https://tailwindcss.com/docs/styling-with-utility-classes
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (Tailwind CSS v4 docs)

## Overview

Arbitrary values in Tailwind CSS allow you to use one-off values outside of your predefined theme by using the special square bracket syntax for specifying custom values.

## Basic Syntax

Many utilities in Tailwind are driven by theme variables (like `bg-blue-500`, `text-xl`, and `shadow-md`). When you need a value outside your theme, use square brackets:

```html
<button class="bg-[#316ff6] ...">
  Sign in with Facebook
</button>
```

This is useful for one-off colors outside your color palette, such as the Facebook blue above. The same syntax applies to arbitrary font sizes, e.g. `text-[18px]`, and arbitrary colors, e.g. `bg-[#bada55]`.

## Complex Custom Values

Arbitrary values work for complex custom values like specific grid configurations:

```html
<div class="grid grid-cols-[24rem_2.5rem_minmax(0,1fr)]">
  <!-- ... -->
</div>
```

(Note: spaces within an arbitrary value are written as underscores, which Tailwind converts to spaces when generating the CSS.)

## Using calc() with Theme Values

You can use CSS features like `calc()` even when referencing theme values:

```html
<div class="max-h-[calc(100dvh-(--spacing(6)))]">
  <!-- ... -->
</div>
```

## Arbitrary Properties

Tailwind supports generating completely arbitrary CSS, including arbitrary property names, which is useful for setting CSS variables:

```html
<div class="[--gutter-width:1rem] lg:[--gutter-width:2rem]">
  <!-- ... -->
</div>
```

This syntax allows you to define custom CSS properties that can be modified at different breakpoints/variants.

## Type Hints (from broader Tailwind v4 documentation)

Tailwind can usually infer the CSS data type an arbitrary value represents from the value itself. Available type-hint data types referenced in Tailwind's docs include: `absolute-size`, `angle`, `bg-size`, `color`, `family-name`, `generic-name`, `image`, `integer`, `length`, `line-width`, `number`, `percentage`, `position`, `ratio`, `relative-size`, `url`, `vector`, and `*`. When an arbitrary value references a CSS variable and the property is ambiguous (for example with a non-color property), a type hint can be added, e.g. `text-[length:var(--my-var)]` or `w-[length:var(--width)]`.

## How It Works

Tailwind CSS generates CSS based on the classes you're actually using. It scans your project files for symbols that look like class names, including those with arbitrary values like `bg-[#316ff6]`, and generates the necessary CSS on demand even when the value isn't part of your theme.

## Modifiers and Variants

Arbitrary values can be combined with modifiers/variants such as hover, focus, responsive breakpoints, and dark mode, for example `hover:bg-[#2563eb]`.
