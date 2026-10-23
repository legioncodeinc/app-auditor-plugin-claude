// Render the numbered beginner guides (plugins/webapp-capture/docs/01..06) plus a reference
// appendix into one Legion Code Inc. branded PDF with a clickable contents page and bookmarks.
// Uses the Chromium and playwright-core the capture scripts already need; the Markdown and
// Mermaid renderers load in the page from jsDelivr at pinned versions (needs network).
// Designed and built by Legion Code Inc.
// Usage: node tools/build-guide-pdf.mjs [output.pdf]
//   (run `npm install` in plugins/webapp-capture/skills/webapp-capture-stinger/scripts first)
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PLUGIN = path.join(ROOT, "plugins", "webapp-capture");
const SCRIPTS = path.join(PLUGIN, "skills", "webapp-capture-stinger", "scripts");
const DOCS = path.join(PLUGIN, "docs");
const REPO_URL = "https://github.com/legioncodeinc/app-auditor-plugin-claude/blob/main/plugins/webapp-capture/docs/";
// Reference appendix: these sections of USAGE-GUIDE.md, in this order.
const REFERENCE = ["What it installs", "Demo route in depth", "How it stays safe", "Where outputs go"];
const OUT = path.resolve(process.argv[2] || path.join(PLUGIN, "docs", "webapp-capture-usage-guide.pdf"));
const MARKED = "https://cdn.jsdelivr.net/npm/marked@15.0.7/marked.min.js";
const MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js";
const BRAND = { ink: "#0A0B0D", green: "#18A968", greenTint: "#E8F6EF", amber: "#F7A823", muted: "#6E6A62", rule: "#E4E2DD" };

let chromium;
try { ({ chromium } = createRequire(path.join(SCRIPTS, "package.json"))("playwright-core")); }
catch { console.error(`playwright-core not found. Run: cd "${SCRIPTS}" && npm install`); process.exit(1); }
const { chromiumPath } = await import(pathToFileURL(path.join(SCRIPTS, "lib", "common.mjs")).href);

const version = JSON.parse(fs.readFileSync(path.join(PLUGIN, ".claude-plugin", "plugin.json"), "utf8")).version;
const stripNav = (md) => md.split("\n").filter((l) => !l.startsWith("**[Home]")).join("\n");
const guides = fs.readdirSync(DOCS).filter((f) => /^\d{2}-.+\.md$/.test(f)).sort()
  .map((f) => ({ slug: f.replace(/\.md$/, ""), file: f, md: stripNav(fs.readFileSync(path.join(DOCS, f), "utf8")) }));
const usage = fs.readFileSync(path.join(DOCS, "USAGE-GUIDE.md"), "utf8");
const section = (title) => { const a = usage.indexOf(`## ${title}`); const b = usage.indexOf("\n## ", a + 3); if (a < 0) throw new Error(`USAGE-GUIDE.md has no section ${title}`); return usage.slice(a, b < 0 ? undefined : b); };
const docs = [...guides, { slug: "reference", file: "USAGE-GUIDE.md", md: ["# Reference", "", "Details for when you want to know exactly what happens. The full reference is USAGE-GUIDE.md in the plugin's docs folder.", "", ...REFERENCE.map(section)].join("\n") }];
// Logo: drop the SVG's own title text so it is not read twice, keep the artwork.
const logo = fs.readFileSync(path.join(ROOT, "assets", "brand", "legion-logo-light.svg"), "utf8").replace(/<title>[\s\S]*?<\/title>|<desc>[\s\S]*?<\/desc>/g, "");
const today = new Date().toISOString().slice(0, 10);

// Runs in the page: render each guide, number nothing by hand, link and theme everything.
async function renderPage(BRAND) {
  try {
    const main = document.getElementById("content");
    const slugify = (t) => t.toLowerCase().trim().replace(/[^\p{L}\p{N}\- ]/gu, "").replace(/ /g, "-");
    const files = new Map(window.__docs.map((d) => [d.file, d.slug]));
    const tocList = document.getElementById("toc-list");
    for (const doc of window.__docs) {
      const sec = document.createElement("section");
      sec.className = "doc";
      sec.id = "doc-" + doc.slug;
      sec.innerHTML = marked.parse(doc.md);
      const ids = new Set();
      for (const h of sec.querySelectorAll("h1, h2, h3")) { const id = doc.slug + "--" + slugify(h.textContent); h.id = id; ids.add(id); }
      main.appendChild(sec);
      // Contents: the guide title, then its main steps.
      const h1 = sec.querySelector("h1");
      const li = document.createElement("li");
      li.innerHTML = `<a href="#doc-${doc.slug}">${h1 ? h1.textContent.replace(/^\d+\.\s*/, "") : doc.slug}</a>`;
      const subs = [...sec.querySelectorAll("h2")].filter((h) => !/^What's next|^Prompts for|^Before you|^The whole trip$/i.test(h.textContent));
      if (subs.length) { const ul = document.createElement("ul"); for (const h of subs) ul.insertAdjacentHTML("beforeend", `<li><a href="#${h.id}">${h.textContent}</a></li>`); li.appendChild(ul); }
      tocList.appendChild(li);
      doc.ids = ids;
    }
    // Links: other guides and their headings jump inside the PDF; everything else points at GitHub.
    for (const doc of window.__docs) {
      for (const a of document.querySelectorAll(`#doc-${doc.slug} a[href]`)) {
        const href = a.getAttribute("href");
        if (/^(https?:|mailto:)/.test(href)) continue;
        const [file, hash] = href.split("#");
        const target = file ? files.get(file) : doc.slug;
        if (target) {
          const id = hash ? `${target}--${hash}` : `doc-${target}`;
          const known = window.__docs.find((d) => d.slug === target).ids;
          a.setAttribute("href", "#" + (hash && !known.has(id) ? `doc-${target}` : id));
        } else if (file === "README.md") a.setAttribute("href", "#toc");
        else if (/\.pdf$/.test(file)) a.replaceWith(...a.childNodes);
        else a.setAttribute("href", new URL(href, window.__repo).href);
      }
    }
    for (const code of main.querySelectorAll("pre > code.language-mermaid")) {
      const box = document.createElement("div");
      box.className = "diagram";
      if (/^flowchart TD/.test(code.textContent.trim()) && code.textContent.trim().split("\n").length > 10) box.classList.add("tall");
      const graph = document.createElement("pre");
      graph.className = "mermaid";
      graph.style.cssText = "background:none;color:inherit;padding:0;margin:0";
      graph.textContent = code.textContent;
      box.appendChild(graph);
      code.parentElement.replaceWith(box);
    }
    // Configure before any await: otherwise mermaid's own startOnLoad renders on window load with the default theme.
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "base", fontFamily: "Inter, Helvetica Neue, Arial, sans-serif",
      themeVariables: { primaryColor: BRAND.greenTint, primaryBorderColor: BRAND.green, primaryTextColor: BRAND.ink, lineColor: BRAND.ink, secondaryColor: "#FFF4DE", tertiaryColor: "#F4F3F0", actorBkg: BRAND.greenTint, actorBorder: BRAND.green, noteBkgColor: "#FFF4DE", fontSize: "14px" } });
    // Mermaid sizes boxes from measured text, so the webfont must be loaded first or labels clip.
    await Promise.all(["400", "600", "700"].map((w) => document.fonts.load(w + " 14px Inter")));
    await document.fonts.ready;
    await mermaid.run({ querySelector: ".mermaid" });
    await document.fonts.ready;
    window.__ready = true;
  } catch (e) { window.__error = String(e && e.message || e); }
}

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Webapp Capture Guides</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
  @page { size: Letter; margin: 0.8in 0.75in 0.85in; }
  * { box-sizing: border-box; }
  body { margin: 0; font: 10.5pt/1.55 Inter, "Helvetica Neue", Arial, sans-serif; color: ${BRAND.ink}; }
  .cover { height: 9.1in; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
  .cover .logo svg { height: 46px; width: auto; }
  .cover .band { border-left: 8px solid ${BRAND.green}; padding: 6px 0 6px 22px; }
  .cover .kicker { color: ${BRAND.green}; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; font-size: 10pt; }
  .cover h1 { font-size: 40pt; line-height: 1.05; margin: 10px 0 14px; font-weight: 800; letter-spacing: -.02em; }
  .cover .sub { font-size: 14pt; color: ${BRAND.muted}; max-width: 5.6in; }
  .cover .meta { display: flex; justify-content: space-between; align-items: flex-end; border-top: 2px solid ${BRAND.ink}; padding-top: 12px; font-size: 9.5pt; color: ${BRAND.muted}; }
  .cover .meta strong { color: ${BRAND.ink}; }
  .cover .motto { font-weight: 700; color: ${BRAND.ink}; }
  h2 { font-size: 17pt; margin: 26px 0 10px; padding-bottom: 6px; border-bottom: 2px solid ${BRAND.green}; page-break-after: avoid; }
  h3 { font-size: 12.5pt; margin: 20px 0 6px; color: ${BRAND.ink}; page-break-after: avoid; }
  h2 + p, h3 + p { margin-top: 6px; }
  p, li { orphans: 3; widows: 3; }
  a { color: #0E7C4C; text-decoration: none; border-bottom: 1px solid #A9DCC4; }
  strong { font-weight: 700; }
  code { font-family: "JetBrains Mono", Menlo, monospace; font-size: 8.8pt; background: #F4F3F0; padding: 1px 4px; border-radius: 3px; }
  pre { background: ${BRAND.ink}; color: #E9F5EF; padding: 12px 14px; border-radius: 6px; overflow: hidden; white-space: pre-wrap; page-break-inside: avoid; }
  pre code { background: none; color: inherit; padding: 0; font-size: 8.8pt; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0 14px; font-size: 9pt; page-break-inside: auto; }
  tr { page-break-inside: avoid; }
  th { background: ${BRAND.greenTint}; text-align: left; font-weight: 700; border-bottom: 2px solid ${BRAND.green}; }
  th, td { padding: 6px 8px; vertical-align: top; border-bottom: 1px solid ${BRAND.rule}; }
  hr { border: 0; border-top: 1px solid ${BRAND.rule}; margin: 22px 0; }
  .diagram { margin: 12px 0 16px; padding: 14px; border: 1px solid ${BRAND.rule}; border-top: 3px solid ${BRAND.green}; border-radius: 6px; text-align: center; page-break-inside: avoid; }
  .diagram svg { max-width: 100% !important; height: auto; max-height: 4.5in; }
  .diagram.tall svg { height: 8in !important; width: auto !important; max-height: none; }
  .diagram.tall { page-break-before: always; }
  .toc { page-break-after: always; }
  .toc h1 { font-size: 24pt; margin: 0 0 14px; border-bottom: 3px solid ${BRAND.green}; padding-bottom: 8px; }
  .toc ol { padding-left: 1.2em; font-size: 12pt; font-weight: 700; }
  .toc ol > li { margin: 10px 0 4px; }
  .toc ul { font-size: 9.5pt; font-weight: 400; margin: 4px 0 0; padding-left: 1.1em; columns: 2; column-gap: 24px; }
  .toc a { border-bottom: 0; color: ${BRAND.ink}; }
  .toc ol > li > a { color: #0E7C4C; }
  section.doc { page-break-before: always; }
  section.doc h1 { font-size: 24pt; margin: 0 0 12px; border-bottom: 3px solid ${BRAND.green}; padding-bottom: 8px; }
</style></head><body>
<section class="cover">
  <div class="logo">${logo}</div>
  <div class="band">
    <div class="kicker">Webapp Capture · Beginner Guides</div>
    <h1>Make Demo Videos &amp; Audit My UX/UI with Claude</h1>
    <div class="sub">Six step-by-step guides: install, your first demo video, screenshots and audits, finishing in ChatGPT, selling the work, and fixing problems.</div>
  </div>
  <div class="meta">
    <div><strong>Plugin version ${version}</strong><br>Generated ${today}<br>legioncodeinc.com</div>
    <div class="motto">I am Legion. We are Legion.</div>
  </div>
</section>
<section id="toc" class="toc"><h1>Contents</h1><ol id="toc-list"></ol></section>
<main id="content"></main>
<script>window.__docs = ${JSON.stringify(docs).replace(/</g, "\\u003c")}; window.__repo = ${JSON.stringify(REPO_URL)};</script>
<script src="${MARKED}"></script>
<script src="${MERMAID}"></script>
<script>
(${renderPage.toString()})(${JSON.stringify(BRAND)});
</script></body></html>`;

const browser = await chromium.launch({ executablePath: chromiumPath({ browser: {} }), headless: true });
try {
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForFunction(() => window.__ready || window.__error, null, { timeout: 60000 });
  const error = await page.evaluate(() => window.__error);
  if (error) throw new Error(`render failed: ${error}`);
  const diagrams = await page.locator(".diagram svg").count();
  const pdf = await page.pdf({
    format: "Letter", printBackground: true, displayHeaderFooter: true, preferCSSPageSize: true, outline: true, tagged: true,
    headerTemplate: "<div></div>",
    footerTemplate: `<div style="width:100%;font:7.5pt Inter,Arial,sans-serif;color:${BRAND.muted};padding:0 0.75in;display:flex;justify-content:space-between"><span><span style="color:${BRAND.green};font-weight:700">Legion Code Inc.</span> · Webapp Capture guides · v${version}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
  });
  if (fs.existsSync(OUT) && fs.lstatSync(OUT).isSymbolicLink()) throw new Error(`refusing to write through a symlink: ${OUT}`);
  fs.writeFileSync(OUT, pdf);
  console.log(`wrote ${path.relative(ROOT, OUT)} (${(pdf.length / 1024).toFixed(0)} KB, ${diagrams} diagrams)`);
} finally {
  await browser.close();
}
