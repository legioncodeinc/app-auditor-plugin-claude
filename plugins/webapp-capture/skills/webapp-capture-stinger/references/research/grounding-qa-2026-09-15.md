# Grounding QA: webapp-capture-stinger (2026-09-15)

Independent grounding audit of SKILL.md, the four guides, and REFERENCE.md against
the raw research corpus, plus a scripts-versus-guides contradiction check.

## Summary counts

Sampled claims: 37 (at least 6 per guide, spread across all four guides).

| Verdict | Count |
| --- | --- |
| SUPPORTED | 35 |
| PARTIAL | 2 |
| UNSUPPORTED | 0 |

Both PARTIAL findings are narrow: one attaches an accurate implementation detail
(file mode) to a citation that does not discuss it, the other names the wrong CSS
color function for Tailwind v4's palette output. Neither is a fabrication; both are
citation-precision issues rather than made-up facts.

## Sampled claim table

Guide column: 00 = foundation, 01 = demo, 02 = component library, 03 = inconsistency
audit.

| # | Guide | Claim excerpt | Cited file | Verdict | Evidence |
| --- | --- | --- | --- | --- | --- |
| A1 | 00 | "saves cookies and storage with `context.storageState()` to the configured path, mode 600" | playwright--authentication.md | PARTIAL | Raw file documents `context.storageState({ path })` and warns the file can hold sensitive cookies, but never mentions file permissions or "mode 600." That detail is accurate (confirmed in `scripts/save-session.mjs`: `fs.chmodSync(cfg.auth.storageState, 0o600)`) but is not supported by the cited source. |
| A2 | 00 | Headless runs load the saved session with the `storageState` context option | playwright--browser-context-options.md | SUPPORTED | "Populates context with given storage state. This option can be used to initialize context with logged-in information obtained via `browserContext.storageState()`." |
| A3 | 00 | `connectOverCDP` "is meant for an already-running browser" | playwright--cdp-persistent-context.md | SUPPORTED | "This method attaches Playwright to an existing browser instance using the Chrome DevTools Protocol." |
| A4 | 00 | "`launchPersistentContext` rejects `storageState`" | playwright--cdp-persistent-context.md | SUPPORTED | "`launchPersistentContext` does NOT take `storageState`, since it always launches from the given `userDataDir`'s existing persistent storage." |
| A5 | 00 | Form submits/PUT/PATCH/DELETE, "which MDN does not classify as safe" | code--mdn-http-request-methods.md | SUPPORTED | Classification table lists POST, PUT, DELETE, PATCH all as Safe: No. |
| A6 | 00 | "Plain screenshots default to `scale: 'device'`" | playwright--screenshots.md | SUPPORTED | `scale` option: "Defaults to `'device'`." |
| A7 | 00 | "Plain screenshot APIs default to `'allow'`, unlike `toHaveScreenshot()`" | playwright--screenshots.md + playwright--visual-comparisons.md | SUPPORTED | screenshots.md: animations "Defaults to `'allow'`"; visual-comparisons.md: for `toHaveScreenshot()` "this defaults to `'disabled'`." |
| A8 | 00 | Cross-origin `cssRules` throws `SecurityError` | inventory--mdn-cssstylesheet-cssrules.md | SUPPORTED | "if a stylesheet is loaded from a different domain, accessing `cssRules` results in a `SecurityError`." |
| B1 | 01 | Demo structure timings: hook 10-15s, aha 15-20s, walkthrough 45-60s (max 3 features), social proof 10s, CTA 10s, total 60-90s | demo--demo-script-structure.md | SUPPORTED | Matches the five-section timing table and "Demonstrate three core features maximum" verbatim. |
| B2 | 01 | "Pace narration at 130 to 150 words per minute; the recorder defaults to 140" | demo--demo-script-structure.md + demo--narration-speaking-rate-wpm.md | SUPPORTED | First source: "Speaking pace assumed: 130-150 words per minute." Second source gives an overlapping but wider 130-160 band, matching the guide's "overlap but do not fully agree." Recorder default of 140 confirmed in `scripts/demo/record-demo.mjs`: `plan.narration?.wordsPerMinute \|\| 140`. |
| B3 | 01 | recordVideo "default scales the viewport down to fit 800x800" | playwright--browser-context-options.md + playwright--videos.md | SUPPORTED | "If not specified the size will be equal to `viewport` scaled down to fit into 800x800." |
| B4 | 01 | "Launches with `slowMo` (default 250ms) so actions are watchable" | demo--playwright-launch-slowmo.md | SUPPORTED | Raw source's own usage note demonstrates `slowMo: 250` for exactly this purpose ("pace clicks/typing at a human-watchable speed for screen recording"); "default 250ms" describes the recorder's own default, confirmed in code: `slowMo: plan.video?.slowMo ?? 250`. (Playwright's own library default is 0, but the guide is describing this skill's recorder default, not Playwright's.) |
| B5 | 01 | "videos are only written on context close" | playwright--videos.md | SUPPORTED | "The video is guaranteed to be written to the filesystem upon closing the browser context." |
| B6 | 01 | Concat demuxer + `-c copy` "requires identical codec parameters across clips" | demo--ffmpeg-concat-demuxer.md | SUPPORTED | "All files must have the same streams (same codecs, same time base, etc.)" for `-c copy` to work. |
| B7 | 01 | GIF: two-pass `palettegen` then `paletteuse`, commonly `fps=15,scale=480:-1` | demo--ffmpeg-gif-palettegen-paletteuse.md | SUPPORTED | Raw source's combined example uses exactly `fps=15,scale=480:-1,split` feeding palettegen/paletteuse. |
| B8 | 01 | "chunk OpenAI input over 4096 characters" | demo--openai-audio-speech-api.md | SUPPORTED | `input`: "The maximum length is 4096 characters." |
| B9 | 01 | "SRT uses a comma before milliseconds" | demo--srt-basics.md | SUPPORTED | "The comma serves as the millisecond separator, distinguishing SRT from... WebVTT... that use a period instead." |
| C1 | 02 | Colors converted to hex "including `lab()` and `oklab()` output from Tailwind v4 palettes, using Ottosson's Oklab matrices" | inventory--oklab-bottosson.md + inventory--tailwind-v4-colors.md | PARTIAL | Both cited sources say Tailwind v4's palette is expressed in **OKLCH**, not `lab()`/`oklab()`. tailwind-v4-colors.md: "Colors are expressed in OKLCH format... All colors use OKLCH format," with every example using `oklch(...)`. oklab-bottosson.md's own adoption note: "Tailwind CSS v4's default palette is also expressed in OKLCH." The Oklab-matrices mechanism is real and well documented, but the specific claim that Tailwind v4 emits `lab()`/`oklab()` values is contradicted by the very sources cited for it. |
| C2 | 02 | DTCG shape: `$type` on groups, `$value` per token, color as `colorSpace`/`components`/`alpha`/`hex` | inventory--dtcg-format-spec.md + inventory--dtcg-color-module.md | SUPPORTED | Format spec confirms `$value`/`$type` structure and group-level `$type`; color module confirms the exact `colorSpace`, `components`, optional `alpha`, optional `hex` shape. |
| C3 | 02 | "`$extensions`, which tools must preserve" | inventory--dtcg-format-spec.md | SUPPORTED | "Tools that process design token files MUST preserve any extension data they do not themselves understand." |
| C4 | 02 | "the spec forbids" inferring `$type` from a value | inventory--dtcg-format-spec.md | SUPPORTED | "Tools MUST NOT attempt to guess the type of a token by inspecting" its value. |
| C5 | 02 | "Style Dictionary v4 consumes DTCG, but does not yet fully support 2025.10" | inventory--style-dictionary-dtcg.md | SUPPORTED | "first-class support for the DTCG format... as of version 4"; "The latest format 2025.10 does not have full support yet in Style Dictionary. This is a work in progress in v5." |
| C6 | 02 | Tailwind v4 `@theme` namespaces: `--color-*`, `--font-*`, `--text-*`, `--radius-*`, `--shadow-*`, `--spacing-*` | inventory--tailwind-v4-theme.md | SUPPORTED | Namespace table lists exactly these (plus others) mapped to utility classes. |
| C7 | 02 | "Record icon font axes... fill, weight, grade, optical size" | inventory--material-symbols-guide.md | SUPPORTED | Confirms Fill, Weight (wght), Grade (GRAD), Optical Size (opsz) as the four variable axes. |
| C8 | 02 | `getBoundingClientRect` "gives geometry relative to the viewport" | inventory--mdn-element-getboundingclientrect.md | SUPPORTED | "information about the size of an element and its position relative to the viewport." |
| D1 | 03 | Delta E thresholds: below 1 imperceptible, 1-2 JND, 2+ clearly different | visual--ciede2000-deltae-culori.md | SUPPORTED | Matches the raw file's aggregated thresholds; the guide also correctly notes ("does not publish numeric cut points") that culori's own docs do not give this table directly, matching the raw file's own caveat. |
| D2 | 03 | WCAG 4.5:1 normal text, 3:1 large text (SC 1.4.3) | visual--wcag22-contrast-minimum.md | SUPPORTED | "4.5:1... Large text - 3:1 ratio." |
| D3 | 03 | 3:1 for UI components/graphics (SC 1.4.11) | visual--wcag22-non-text-contrast.md | SUPPORTED | "a contrast ratio of at least 3:1... User Interface Components... Graphical Objects." |
| D4 | 03 | pixelmatch "threshold 0 to 1, anti-aliasing detection" | visual--pixelmatch-readme.md | SUPPORTED | `threshold` default 0.1, "ranges from 0 to 1"; `includeAA` controls anti-aliased pixel detection. |
| D5 | 03 | `toHaveScreenshot` "threshold default 0.2" | visual--playwright-tohavescreenshot.md | SUPPORTED | "threshold... Defaults to `0.2`." |
| D6 | 03 | Tailwind arbitrary values (`text-[11px]`, `bg-[#316ff6]`) are "values outside the theme scale" | code--tailwindcss-v4-arbitrary-values.md | SUPPORTED | `bg-[#316ff6]` is the raw source's own example; "use a value outside your theme" matches "outside the theme scale." (The `text-[11px]` example is illustrative, not a literal quote; raw shows `text-[18px]` as its arbitrary-font-size example.) |
| D7 | 03 | jscpd `--min-tokens`, `--similarity` flags | code--jscpd-readme.md | SUPPORTED | Both flags documented with defaults (`--min-tokens` 50, `--similarity` off/1). |
| D8 | 03 | Stylelint rule names: `color-no-hex`, `color-named`, `unit-allowed-list`, `font-family-no-duplicate-names`, `declaration-property-value-allowed-list` | five stylelint rule raw files | SUPPORTED | Each rule's raw file confirms name and purpose exactly as described. |
| E1 | 03 | Scale-sprawl "metric families mirror Project Wallace's analyzer (unique colors, font sizes, families, shadows, z-indexes)" | visual--project-wallace-css-analyzer.md | SUPPORTED | The citation is scoped only to "metric families," and the raw file's Values category lists exactly unique colors, font sizes, font families, box shadows, and z-indexes. The specific numeric thresholds (8 distinct, 1%, 4px/2px grid) are correctly disclosed elsewhere in the same guide as the skill's own defensible default, not sourced to this file. |
| E2 | 03 | Component-drift "drift taxonomy (token, component, pattern drift)," marked "(community source)" | visual--design-system-drift-community.md | SUPPORTED | Raw file lists five drift types including token drift, component variant drift, and pattern drift; correctly labeled as a community source. |
| E3 | 03 | "Hardcoded hex and functional color literals outside variable definitions... Literal values instead of semantic tokens" | code--duplicate-ui-components-detection.md | SUPPORTED | Raw file: "Literal color values versus semantic tokens (a signal that a component drifted from the design-token system)." |
| E4 | 03 | "Long class lists repeated 3+ times... Copy-pasted components that should be one component" | code--duplicate-ui-components-detection.md | SUPPORTED | Raw file: "Repeated local implementations versus shared primitives (i.e. the same visual/functional component re-implemented locally instead of imported from the shared library)." General concept matches; the "3+" repeat threshold is the skill's own script default (confirmed in `scripts/audit/audit-code.mjs`: `locs.length >= 3`), not sourced to this file. |

## Uncited claims asserting external facts

Claims below assert something about an external tool, spec, or platform rather than
this skill's own design choice or a lesson from its own production run, and carry no
`[raw/...]` citation.

1. **Guide 00** (Parallelism section): "Subagent concurrency is capped by the harness
   (Claude Code: 20 concurrent)." This is a factual claim about Claude Code's own
   subagent limit, stated with no citation anywhere in the raw corpus.
2. **Guide 03**, Part B: "Tailwind state selectors such as `data-[state=checked]` are
   not values and are excluded." This asserts a fact about Tailwind's arbitrary-value
   syntax (that `data-[...]`, `aria-[...]`, etc. are selector variants rather than
   values) without a citation. `code--tailwindcss-v4-arbitrary-values.md` is cited
   elsewhere in the same paragraph for arbitrary values generally, but that file does
   not discuss state-selector syntax, and this sentence carries no citation of its own.
3. **Guide 00** (session limits table), lower confidence: "Cookies without an expiry
   vanish when the login browser closes" is general browser-cookie behavior presented
   as fact with no citation. This is common, uncontroversial web-platform knowledge,
   so it is a weaker case than the two above, but it is still an uncited external
   claim rather than a design choice.

## Script-versus-guide contradictions

1. **Screenshot masking is described but not implemented.** Guide 00's safety
   contract says: "Screenshots are not redacted by regex... For shareable
   screenshots, cover sensitive regions with Playwright's `mask` option
   [raw/playwright--screenshots.md], using a fully opaque solid overlay rather than
   blur." This reads as a capability of the capture pipeline. In practice, no script
   passes a `mask` option anywhere: `scripts/screenshots.mjs`'s `page.screenshot()`
   call only sets `{ path, animations: "disabled" }`, `scripts/demo/record-demo.mjs`'s
   screenshot call is the same, and `scripts/capture.config.example.json` has no
   masking-related config field at all (a project-wide grep for `mask` across
   `scripts/` returns zero hits). By contrast, the text/HTML `redact.patterns`
   mechanism the guide describes in the same section is fully wired end to end (see
   `scripts/inventory/extract.mjs`'s `redact()` function). The masking guidance is
   real, correctly sourced advice, but it is documentation of a manual practice the
   operator must add themselves, not something any current script does automatically.
   The guide does not make this distinction explicit, so a reader could reasonably
   expect masking to already be wired in.

No other contradictions were found between the six scripts read
(`scripts/lib/common.mjs`, `scripts/screenshots.mjs`, `scripts/demo/record-demo.mjs`,
`scripts/audit/audit-visual.mjs`, `scripts/audit/audit-code.mjs`,
`scripts/inventory/tokens-dtcg.mjs`) and the guides. Specifically checked and
confirmed **consistent** (not contradictions, listed for completeness):

- Off-origin navigation blocking (`common.mjs`'s `openApp()` route handler) matches
  guide 00's description of `route.abort()` / `isNavigationRequest()` / main-frame
  checks.
- `gotoChecked()`'s session-expiry and theme-guard throws match guide 00's described
  behavior.
- `record-demo.mjs`'s deny-pattern list, secret-field refusal, explicit video size,
  `animations: 'disabled'` screenshots, narration-based minimum scene hold, and
  context-close-before-read ordering all match guide 01.
- `audit-visual.mjs`'s CIEDE2000 threshold (2, overridable via `DE`), 5+ combined-use
  gate, ">8 distinct values" / "<1% rare" / "4px spacing, 2px radius grid" scale rules,
  ">3 font stacks", ">5 shadows", and "3+ variants differing in 2+ of
  background/radius/font/padding" component-drift rule all match guide 03's stated
  thresholds exactly.
- `audit-code.mjs`'s hex/functional-color detection (excluding variable-definition
  lines), arbitrary-value versus arbitrary-token-value split, state-selector exclusion
  list (`data-`, `aria-`, `group-`, `peer-`, `supports-`, `has-`, `not-`, `nth-`),
  z-index 3+-digit detection, and 3+-repeat class-list threshold all match guide 03.
- `tokens-dtcg.mjs`'s DTCG output shape (`$type` per group, `$value` per token, color
  objects with `colorSpace`/`components`/optional `alpha`/`hex`, dimensions as
  `{value, unit}`, observation data under a vendor `$extensions` key, CSS-variable-name
  reuse for candidate names) matches guide 02's Stage 3 description exactly.
