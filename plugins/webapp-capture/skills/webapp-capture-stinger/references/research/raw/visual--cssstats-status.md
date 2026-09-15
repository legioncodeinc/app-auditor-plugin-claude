# CSS Stats (cssstats/core, cssstats/cssstats) — maintenance status
- URL: https://github.com/cssstats/core ; https://github.com/cssstats/cssstats
- Fetched: 2026-09-15
- Source type: README (status record, not a maintained tool)
- Last updated (if shown): cssstats/core archived January 27, 2019

## Status summary

**cssstats/core is archived.** GitHub shows: "Archived — The repository was archived on January 27, 2019 and is now read-only."

Description: "cssstats/core is a Node.js module that parses stylesheets and returns an object with statistics." It served as the foundational library behind cssstats.com.

Functionality (historical): analyzes CSS and generates metrics including file size and gzip compression size, rule statistics (count, size distribution), selector analysis (type/class/ID counts and specificity), declaration metrics and property tracking, media query breakdowns. Provided both direct usage and a PostCSS plugin integration, with helper methods for specificity graphing, selector sorting/deduplication, font-size/family extraction, property-reset detection, and vendor-prefix identification.

**Project relocated, not actively continued as `core`.** The README explicitly states: "Moved to monorepo," pointing to `github.com/cssstats/cssstats/tree/master/packages/cssstats` as the active code location instead of the archived standalone `core` package.

## cssstats/cssstats (the web app / monorepo)

Description: a tool that "visualizes and analyzes various statistics about CSS stylesheets" via a web interface at cssstats.com.

README content is minimal:
- Install: clone repo, run `yarn`.
- Usage: `yarn start`, access at `localhost:8000`.
- License: MIT.
- Built by: mrmrs, jxnblk, johno.

Maintenance signals observed: 10 open issues, 5 open pull requests, 698 total commits on main, 2.8k stars, 197 forks, 42 watchers — no clear recent-activity indicators surfaced in the fetched page; overall posture reads as low/inactive maintenance rather than a fast-moving, currently-developed project.

## Conclusion for webapp-capture-stinger

Treat CSS Stats (`cssstats`) as a **legacy/inactive** tool for this skill's purposes: the underlying `core` analysis package is formally archived (2019) and its functionality has effectively been superseded in the current ecosystem by actively maintained alternatives such as `@projectwallace/css-analyzer` (200+ metrics, TypeScript, zero-config, still published and used to power projectwallace.com as of 2026). Prefer Project Wallace's css-analyzer over CSS Stats for any new static-CSS-metrics tooling in this skill.
