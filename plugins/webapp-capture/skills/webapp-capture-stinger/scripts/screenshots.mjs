// Route-by-route scrolling screenshots, including real tabs. Read-only: navigates
// same-origin routes and clicks only tabs that pass the tab filter.
// Files: <screenshots>/<route-slug>/<route-slug>-001.png and <route-slug>__<tab>-001.png
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... [ROUTES=/a,/b] [SHARD=0 SHARDS=4] node screenshots.mjs
//        or: node parallel.mjs screenshots.mjs
import fs from "node:fs";
import path from "node:path";
import { assertTheme, discoverRoutes, gotoChecked, listTabs, loadConfig, log, openApp, pad, routeSlug, settle, shard, shotOptions, tabName, withTimeout } from "./lib/common.mjs";

const cfg = loadConfig();
const OUT = cfg.output.screenshots || path.join(cfg.output.inventory, "screenshots");
const MAX = cfg.routes.maxShots || 30;
const { browser, page } = await openApp(cfg);
let failures = 0;

try {
  let routes = process.env.ROUTES ? process.env.ROUTES.split(",").filter(Boolean) : await discoverRoutes(cfg, page);
  if (process.env.SHARDS) routes = shard(routes, Number(process.env.SHARDS))[Number(process.env.SHARD || 0)] || [];
  fs.mkdirSync(OUT, { recursive: true });
  const manifest = path.join(OUT, `manifest${process.env.SHARDS ? `-${process.env.SHARD || 0}` : ""}.tsv`);
  fs.writeFileSync(manifest, "route\tstate\tshots\ttruncated\turl\n");

  const scrollShots = async (dir, base) => {
    await page.mouse.move(-1, -1); // avoid incidental :hover states
    await page.evaluate(() => {
      const doc = document.scrollingElement;
      let best = doc.scrollHeight > doc.clientHeight + 1 ? doc : null;
      let area = best ? innerWidth * innerHeight : 0;
      for (const el of document.querySelectorAll("*")) {
        const oy = getComputedStyle(el).overflowY;
        if (!["auto", "scroll", "overlay"].includes(oy) || el.scrollHeight <= el.clientHeight + 1) continue;
        if (el.getBoundingClientRect().width < innerWidth * 0.4) continue; // ignore sidebars and dropdowns
        const a = el.clientWidth * el.clientHeight;
        if (a > area) { best = el; area = a; }
      }
      window.__scroller = best || doc;
      window.__scroller.scrollTop = 0;
    });
    fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; ; i++) {
      await page.waitForTimeout(450);
      await page.screenshot(shotOptions(cfg, page, { path: path.join(dir, `${base}-${pad(i)}.png`) }));
      const done = await page.evaluate(() => {
        const s = window.__scroller;
        if (s.scrollTop + s.clientHeight >= s.scrollHeight - 1) return true;
        const before = s.scrollTop;
        s.scrollTop += s.clientHeight;
        return s.scrollTop === before;
      });
      if (done) return { shots: i, truncated: false };
      if (i >= MAX) return { shots: i, truncated: true };
    }
  };

  for (const route of routes) {
    const slug = routeSlug(route);
    const dir = path.join(OUT, slug);
    try {
      await withTimeout((async () => {
        await gotoChecked(cfg, page, route);
        const main = await scrollShots(dir, slug);
        fs.appendFileSync(manifest, `${route}\t${slug}\t${main.shots}\t${main.truncated}\t${page.url()}\n`);
        log(`${route}: ${main.shots} shots${main.truncated ? " (truncated at routes.maxShots)" : ""}`);
        for (const t of (await listTabs(cfg, page, route)).filter((x) => !x.selected)) {
          const before = page.url();
          await page.locator(`${cfg.tabs.selector}:visible`).nth(t.index).click({ timeout: 5000 });
          await settle(page);
          await assertTheme(cfg, page);
          const name = tabName(before, page.url(), t.label);
          const res = await scrollShots(dir, `${slug}__${name}`);
          fs.appendFileSync(manifest, `${route}\t${slug}__${name}\t${res.shots}\t${res.truncated}\t${page.url()}\n`);
          log(`  tab ${name}: ${res.shots} shots`);
        }
      })(), 10 * 60000, route);
    } catch (err) {
      failures++;
      const msg = err.message.split("\n")[0];
      log(`${route}: ERROR ${msg}`);
      fs.appendFileSync(manifest, `${route}\t${slug}\t0\tfalse\terror: ${msg}\n`);
      if (/session expired/.test(msg)) break; // every later route would fail too
    }
  }
} finally {
  await browser.close();
}
log(failures ? `done with ${failures} route error(s)` : "done");
process.exit(failures ? 1 : 0);
