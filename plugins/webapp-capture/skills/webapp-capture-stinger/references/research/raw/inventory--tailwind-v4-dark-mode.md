# Dark mode - Tailwind CSS
- URL: https://tailwindcss.com/docs/dark-mode
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (Tailwind CSS v4 docs)

## Overview

Tailwind CSS includes a `dark` variant that enables styling for dark mode. By default, it uses the `prefers-color-scheme` CSS media feature to detect the user's operating system dark mode preference.

### Basic usage example
```html
<div class="bg-white dark:bg-gray-800 rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
  <div>
    <span class="inline-flex items-center justify-center rounded-md bg-indigo-500 p-2 shadow-lg">
      <svg class="h-6 w-6 stroke-white" ...>
        <!-- ... -->
      </svg>
    </span>
  </div>
  <h3 class="text-gray-900 dark:text-white mt-5 text-base font-medium tracking-tight">
    Writes upside-down
  </h3>
  <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm">
    The Zero Gravity Pen can be used to write in any orientation, including upside-down.
    It even works in outer space.
  </p>
</div>
```

## Toggling dark mode manually

Override the default `prefers-color-scheme` behavior to use a custom selector via `@custom-variant`.

### Class-based dark mode
```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

```html
<html class="dark">
  <body>
    <div class="bg-white dark:bg-black">
      <!-- ... -->
    </div>
  </body>
</html>
```

### Data attribute approach
```css
@import "tailwindcss";
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

```html
<html data-theme="dark">
  <body>
    <div class="bg-white dark:bg-black">
      <!-- ... -->
    </div>
  </body>
</html>
```

## System theme support with three-way toggle

Combine localStorage with `window.matchMedia()` to support light mode, dark mode, and system preference:

```javascript
// On page load or when changing themes, add inline in <head> to avoid FOUC
document.documentElement.classList.toggle(
  "dark",
  localStorage.theme === "dark" ||
    (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches),
);

// Whenever the user explicitly chooses light mode
localStorage.theme = "light";

// Whenever the user explicitly chooses dark mode
localStorage.theme = "dark";

// Whenever the user explicitly chooses to respect the OS preference
localStorage.removeItem("theme");
```

## Key points

- Default behavior: uses `prefers-color-scheme` media query.
- Manual toggle: override with `@custom-variant` for class- or data-attribute-based toggling.
- localStorage: common approach to persist user theme preference.
- FOUC prevention: add theme detection inline in `<head>` to prevent flash of unstyled content.
