# css-analyzer (Project Wallace) README and metrics docs
- URL: https://github.com/projectwallace/css-analyzer ; npm: https://www.npmjs.com/package/@projectwallace/css-analyzer ; metrics docs: https://www.projectwallace.com/docs/metrics
- Fetched: 2026-09-15
- Source type: README + official docs
- Last updated (if shown): unknown

## Description

`@projectwallace/css-analyzer` turns CSS into actionable stats — "specificity, complexity, design tokens, and 200+ more metrics." Features: "Extremely detailed (200+ metrics)," TypeScript types built-in, zero config, runs anywhere (Node.js and browsers), tiny footprint (one dependency), battle-tested (it powers Project Wallace itself).

## Installation

```bash
npm install @projectwallace/css-analyzer
```

## Core API usage

Basic analysis:
```javascript
import { analyze } from '@projectwallace/css-analyzer'

const result = analyze(`
  p {
    color: blue;
    font-size: 100%;
  }
  .component[data-state="loading"] {
    background-color: whitesmoke;
  }
`)
```

Specificity comparison:
```javascript
import { compareSpecificity } from '@projectwallace/css-analyzer'

const sorted = [[0,1,1], [2,0,0], [0,0,1]]
  .sort((a,b) => compareSpecificity(a,b))
```

## Metrics categories (package README summary)

- **Colors & Formats** — total/unique counts, color format analysis.
- **Typography** — font families, font sizes, line heights.
- **Spacing & Layout** — z-indexes, box shadows, text shadows, border radiuses.
- **Selectors** — specificity analysis, complexity, nesting levels, pseudo-classes/elements.
- **Properties** — standard and custom properties, shorthands, browser hacks.
- **At-Rules** — media queries, keyframes, @supports, @layer, @container.
- **Design Tokens** — custom property usage, uniqueness ratios.
- **CSS Complexity** — nesting depth, declaration counts, selector complexity.
- **Code Quality** — empty rules, prefixed properties, `!important` usage.

Output structure provides min/max/mean/mode statistics across most analyzed dimensions.

## Metrics documented at projectwallace.com/docs/metrics (site explanation)

Project Wallace organizes tracked CSS metrics into seven categories:

1. **Stylesheet metrics** — whole-stylesheet measures: file size, lines of code, cohesion, simplicity, browser hacks. Examples: "Gzip filesize," "Uncompressed filesize."
2. **Atrules** — counts (total and unique) of `@keyframes`, `@media`, `@font-face`, `@import`, `@supports`, etc.
3. **Rules** — rule composition: "Total empty rules," selector counts per rule (average/min/max), total rules.
4. **Selectors** — specificity, complexity, categorization: ID selectors, universal selectors, accessibility selectors, "Total selectors having maximum specificity."
5. **Declarations** — usage patterns including "Ratio of `!important` declarations" and total unique declarations.
6. **Properties** — vendor-prefixed properties, browser hacks, total property counts.
7. **Values** — the design-token-relevant category: "Total unique colors," font families, font sizes, box-shadows, text-shadows, z-indexes, animation durations, and timing functions.

The tool provides both aggregate and unique counts for most metrics, "enabling comprehensive CSS quality assessment."

## Design tokens analysis (from projectwallace.com/lint-css)

Project Wallace offers a dedicated "Design Tokens" stylelint preset (`@projectwallace/stylelint-plugin`, 60+ rules total) that "contains all rules that keep track of unique design tokens in your CSS and raises issues if you use too many different font-sizes, colors and other tokens." Related presets:
- **Correctness preset** — flags issues like invalid z-indexes and undeclared container names.
- **Maintainability preset** — monitors rule sizes, complexity, specificity, and spacing resets.
- **Performance preset** — tracks overall stylesheet size and duplicate data URLs.

The docs note the plugin should not be relied on alone — combine with Stylelint's built-in rules and other defensive-CSS plugins.

## Notes for webapp-capture-stinger

The "Values" metric category (unique colors, font-sizes, font-families, box-shadows, z-indexes) is the direct mechanism for detecting design-token drift/inconsistency purely from static CSS extraction — complementary to pixel-level visual diffing (pixelmatch/Playwright/Percy/etc.), since it catches inconsistency even when it hasn't yet produced a visually obvious pixel diff (e.g., two near-identical blues used inconsistently).
