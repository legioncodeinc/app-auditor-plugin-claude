import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import test from "node:test";

import { chromiumPath } from "../lib/common.mjs";
import { DemoSceneError, installCursorOverlay, runAction, runVerify, visibleText } from "../lib/demo-actions.mjs";
import { assertSafeDemoTarget, demoDenyPattern } from "../lib/demo-guard.mjs";

const PAGE = `<!doctype html><html><body style="margin:0;font:14px sans-serif">
  <div id="card" style="position:absolute;left:20px;top:20px;width:90px;height:40px;background:#ddd;touch-action:none">Lawn care</div>
  <div id="lane" style="position:absolute;left:300px;top:10px;width:200px;height:120px;border:1px solid #333">Tuesday lane</div>
  <div id="chip" draggable="true" style="position:absolute;left:20px;top:160px;width:60px;height:30px;background:#cef">Sam</div>
  <div id="slot" style="position:absolute;left:300px;top:160px;width:200px;height:40px;border:1px dashed #333">Unassigned</div>
  <div style="position:absolute;left:20px;top:230px">
    <select name="service"><option>Hedge trim</option><option>Lawn care</option></select>
    <select name="status">
      <option>Scheduled</option>
      <option>Remove from route</option>
    </select>
    <label><input type="checkbox" name="repeats" checked> Repeats</label>
    <button id="danger">Delete account</button>
    <button id="open">Book</button>
    <span id="later"></span>
  </div>
  <div id="grid" style="position:absolute;left:20px;top:280px;width:200px;height:100px;overflow:auto">
    ${Array.from({ length: 24 }, (_, h) => `<div data-time="${String(h).padStart(2, "0")}:00" style="height:40px">${h}:00</div>`).join("")}
  </div>
  <div id="card2" style="position:absolute;left:250px;top:420px;width:90px;height:30px;background:#eee">Mowing</div>
  <div id="day" style="position:absolute;left:520px;top:400px;width:200px;height:90px;border:1px solid">Wednesday <div class="appt"><b>Reset</b> sprinkler heads</div></div>
  <div id="trash" style="position:absolute;left:250px;top:500px;width:90px;height:40px"><svg width="10" height="10"></svg><span>Delete</span></div>
  <div id="dialog" role="dialog" hidden style="position:absolute;left:400px;top:300px;background:#fff;border:1px solid">
    <p>Book Lawn care on Tuesday at 9:00?</p><button>Book appointment</button><button>Cancel</button>
  </div>
  <script>
    let dragging = false;
    card.addEventListener("pointerdown", () => { dragging = true; });
    addEventListener("pointerup", (e) => {
      if (!dragging) return; dragging = false;
      const r = lane.getBoundingClientRect();
      if (e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) { lane.appendChild(card); card.style.position = "static"; document.body.dataset.dropped = "lane"; }
    });
    chip.addEventListener("dragstart", (e) => e.dataTransfer.setData("text/plain", "sam"));
    slot.addEventListener("dragover", (e) => e.preventDefault());
    slot.addEventListener("drop", (e) => { e.preventDefault(); slot.textContent = "Assigned to " + (e.dataTransfer.getData("text/plain") === "sam" ? "Sam" : "?"); });
    document.getElementById("open").addEventListener("click", () => { dialog.hidden = false; });
    dialog.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { dialog.hidden = true; if (b.textContent === "Book appointment") document.body.dataset.booked = "yes"; }));
    setTimeout(() => { later.textContent = "Ready now"; later.className = "ready"; }, 400);
  </script>
</body></html>`;

test("demo actions and verify checks work against real Chromium", async (t) => {
  let chromium;
  try { ({ chromium } = await import("playwright-core")); }
  catch { t.skip("playwright-core is not installed"); return; }
  const executablePath = chromiumPath({ browser: {} }) || chromium.executablePath();
  if (!executablePath || !fs.existsSync(executablePath)) { t.skip("no Chromium build installed (npx playwright install chromium)"); return; }

  const server = http.createServer((_, res) => { res.setHeader("content-type", "text/html; charset=utf-8"); res.end(PAGE); });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser = await chromium.launch({ executablePath, headless: true });
    const context = await browser.newContext({ viewport: { width: 900, height: 600 } });
    await context.addInitScript(installCursorOverlay);
    const page = await context.newPage();
    await page.goto(origin);
    const deny = demoDenyPattern("harmless-custom-label");
    const ctx = { guard: (loc, a) => assertSafeDemoTarget(loc, a, deny), deny, parkAt: { x: 880, y: 580 }, pointer: { x: 880, y: 580 } };
    const act = (a) => runAction(page, a, ctx);
    const body = (key) => page.evaluate((k) => document.body.dataset[k], key);

    await t.test("pointer drag between selectors drops the card and parks the cursor", async () => {
      await act({ type: "drag", from: "#card", to: "#lane", steps: 15 });
      assert.equal(await body("dropped"), "lane");
      assert.deepEqual(ctx.pointer, { x: 880, y: 580 });
      const transform = await page.locator("[data-demo-cursor]").evaluate((n) => n.style.transform);
      assert.equal(transform.replace(/\s+/g, ""), "translate(877px,578px)");
    });

    await t.test("native dragTo assigns the chip", async () => {
      await act({ type: "dragTo", selector: "#chip", target: "#slot" });
      assert.equal(await page.locator("#slot").innerText(), "Assigned to Sam");
    });

    await t.test("select by label and uncheck", async () => {
      await act({ type: "select", selector: "select[name=service]", label: "Lawn care" });
      assert.equal(await page.locator("select[name=service]").inputValue(), "Lawn care");
      await act({ type: "uncheck", selector: "input[name=repeats]" });
      assert.equal(await page.locator("input[name=repeats]").isChecked(), false);
      await act({ type: "check", selector: "input[name=repeats]" });
      assert.equal(await page.locator("input[name=repeats]").isChecked(), true);
    });

    await t.test("scrollElement scrolls the container by offset and into view", async () => {
      await act({ type: "scrollElement", selector: "#grid", y: 80, ms: 50 });
      assert.equal(await page.locator("#grid").evaluate((n) => n.scrollTop), 80);
      await act({ type: "scrollElement", selector: "#grid", intoView: "[data-time='08:00']", block: "start", ms: 50 });
      assert.equal(await page.locator("#grid").evaluate((n) => n.scrollTop), 320);
    });

    await t.test("waitFor a selector and a text, and time out cleanly", async () => {
      await act({ type: "waitFor", selector: "#later.ready" });
      await act({ type: "waitFor", text: "Ready now" });
      await assert.rejects(act({ type: "waitFor", selector: "#never", timeoutMs: 300 }), (e) => e instanceof DemoSceneError && /waitFor timed out/.test(e.message));
    });

    await t.test("confirmDialog cancels and throws when the dialog text does not match", async () => {
      await act({ type: "click", selector: "#open" });
      await assert.rejects(act({ type: "confirmDialog", expect: "Reschedule", button: "Book appointment" }), (e) => e instanceof DemoSceneError && /did not match \/Reschedule\/ and was cancelled/.test(e.message));
      assert.equal(await page.locator("#dialog").isHidden(), true);
      assert.equal(await body("booked"), undefined);
    });

    await t.test("confirmDialog clicks the named button when the text matches", async () => {
      await act({ type: "click", selector: "#open" });
      await act({ type: "confirmDialog", expect: "Book Lawn care on Tuesday", button: "Book appointment" });
      assert.equal(await body("booked"), "yes");
    });

    await t.test("the built-in deny list still refuses with a custom pattern", async () => {
      await assert.rejects(act({ type: "click", selector: "#danger" }), /refusing destructive-looking demo control/);
      await assert.rejects(act({ type: "select", selector: "select[name=service]", label: "Delete everything" }), /refusing destructive-looking demo option/);
    });

    await t.test("drag ends and selects are judged on their own name, not their contents", async () => {
      // A day column holding an appointment called "Reset sprinkler heads" is a safe drop target.
      await act({ type: "drag", from: "#card2", to: "#day", steps: 5 });
      await act({ type: "dragTo", selector: "#card2", target: "#day" });
      // A status menu that merely offers "Remove from route" is safe when picking "Scheduled".
      await act({ type: "select", selector: "select[name=status]", label: "Scheduled" });
      assert.equal(await page.locator("select[name=status]").inputValue(), "Scheduled");
      // But a zone whose own label says Delete, and picking the destructive option, are refused.
      await assert.rejects(act({ type: "drag", from: "#card2", to: "#trash" }), /refusing destructive-looking demo control/);
      await assert.rejects(act({ type: "dragTo", selector: "#card2", target: "#trash" }), /refusing destructive-looking demo control/);
      await assert.rejects(act({ type: "select", selector: "select[name=status]", label: "Remove from route" }), /refusing destructive-looking demo option/);
    });

    await t.test("runVerify reports pass and fail without touching the page", async () => {
      const results = [
        await runVerify(page, { type: "visible", selector: "#lane #card" }),
        await runVerify(page, { type: "hidden", selector: "#dialog" }),
        await runVerify(page, { type: "text", selector: "#slot", expect: "Sam" }),
        await runVerify(page, { type: "count", selector: "[data-time]", equals: 24 }),
        await runVerify(page, { type: "count", selector: "[data-time]", atLeast: 10 }),
      ];
      assert.deepEqual(results.map((r) => r.pass), [true, true, true, true, true]);
      const misses = [
        await runVerify(page, { type: "visible", selector: "#never", timeoutMs: 300 }),
        await runVerify(page, { type: "text", selector: "#slot", expect: "Alex", timeoutMs: 300 }),
        await runVerify(page, { type: "count", selector: "[data-time]", equals: 1, timeoutMs: 300 }),
      ];
      assert.deepEqual(misses.map((r) => r.pass), [false, false, false]);
      assert.equal(misses[1].actual, "Assigned to Sam");
      assert.equal(misses[2].actual, 24);
      assert.equal(await body("booked"), "yes");
    });

    await t.test("visibleText returns the page text for the privacy scan", async () => {
      assert.match(await visibleText(page), /Tuesday lane/);
    });
  } finally {
    await browser?.close();
    await new Promise((resolve) => server.close(resolve));
  }
});
