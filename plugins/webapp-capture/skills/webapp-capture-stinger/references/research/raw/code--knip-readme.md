# Knip

- URL: https://github.com/webpro-nl/knip
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): unknown

Content extracted verbatim (with minor reformatting) from the GitHub README at https://raw.githubusercontent.com/webpro-nl/knip/main/packages/knip/README.md, supplemented with a brief description from the official docs site https://knip.dev/.

## Core Purpose (verbatim from README)

Knip finds and fixes **unused dependencies, exports and files** in your JavaScript and TypeScript projects. Less code and dependencies lead to improved performance, less maintenance and easier refactorings.

- Website: [knip.dev](https://knip.dev)
- GitHub repo: [webpro-nl/knip](https://github.com/webpro-nl/knip)
- Official npm packages: `knip`, `@knip/create-config`, `@knip/language-server`, `@knip/mcp`
- Knip on the VS Code Marketplace, Knip on the Open VSX Registry
- Follow @webpro.nl on Bluesky for updates

## Name

/'knɪp/ means "(to) cut" and is pronounced with a hard "K" (Dutch origin, denoted with a 🇳🇱 flag emoji in the README).

## License

Knip is free and open-source software licensed under the ISC License.

Parts of Knip have been inspired by and/or partially copy code from the following projects:
- `@npmcli/package-json` (ISC)
- `@pnpm/deps.graph-sequencer` (MIT)
- `file-entry-cache` (MIT)
- `json-parse-even-better-errors` (MIT)

## Supplementary description (from knip.dev homepage, paraphrased and quoted)

Knip is a static analysis tool for JavaScript and TypeScript projects that identifies and reports unused code artifacts. It detects:
- Unused files
- Unused npm dependencies
- Unused TypeScript exports
- Unused class members
- Duplicate exports

Homepage value proposition: Knip helps to "Declutter your JavaScript & TypeScript projects" by finding and fixing unused dependencies, exports and files through "advanced analysis starting from fine-grained entry points based on the actual frameworks and tooling in (mono)repos for accurate and actionable results."

Knip includes 150+ plugins for frameworks and tools such as Astro, Cypress, ESLint, Jest, GitHub Actions, Next.js, Nx, Remix, Storybook, Svelte, Vite, Vitest, and Webpack. Output is reported to the terminal, listing unused files, dependencies, and exports so developers can review and remove dead code. Per the homepage, Knip is used in 15,000+ public projects, with adopters including Adobe, Google, Microsoft, Shopify, and Vercel.
