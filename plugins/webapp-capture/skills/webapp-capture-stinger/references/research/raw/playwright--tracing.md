# Trace viewer (guide) + Tracing.start() API reference
- URL: https://playwright.dev/docs/trace-viewer and https://playwright.dev/docs/trace-viewer-intro and https://playwright.dev/docs/api/class-tracing
- Fetched: 2026-09-15
- Source type: official docs (guide + API reference, sourced from microsoft/playwright docs/src/trace-viewer.md, docs/src/trace-viewer-intro-js.md, docs/src/api/class-tracing.md on the `main` branch)
- Last updated (if shown): unknown

## GUIDE: Trace viewer

### Introduction

Playwright Trace Viewer is a GUI tool that helps you explore recorded Playwright traces after the script has run. Traces are a great way for debugging your tests when they fail on CI. You can open traces locally or in your browser on trace.playwright.dev.

### Opening Trace Viewer

You can open a saved trace using either the Playwright CLI or in the browser at trace.playwright.dev. Make sure to add the full path to where your `trace.zip` file is located.

```bash js
npx playwright show-trace path/to/trace.zip
```

#### Using trace.playwright.dev

trace.playwright.dev is a statically hosted variant of the Trace Viewer. You can upload a trace file using drag and drop or via the `Select file` button.

Trace Viewer loads the trace entirely in your browser and does not transmit any data externally.

#### Viewing remote traces

You can open remote traces directly using its URL. This makes it easy to view the remote trace without having to manually download the file from CI runs, for example.

```bash js
npx playwright show-trace https://example.com/trace.zip
```

When using trace.playwright.dev, you can also pass the URL of your uploaded trace at some accessible storage (e.g. inside your CI) as a query parameter. CORS (Cross-Origin Resource Sharing) rules might apply.

```txt
https://trace.playwright.dev/?trace=https://demo.playwright.dev/reports/todomvc/data/e6099cadf79aa753d5500aa9508f9d1dbd87b5ee.zip
```

### Recording a trace (langs: js)

#### Tracing locally

To record a trace during development mode set the `--trace` flag to `on` when running your tests. You can also use UI Mode for a better developer experience, as it traces each test automatically.

```bash
npx playwright test --trace on
```

You can then open the HTML report and click on the trace icon to open the trace.
```bash
npx playwright show-report
```

#### Tracing on CI

Traces should be run on continuous integration on the first retry of a failed test by setting the `trace: 'on-first-retry'` option in the test configuration file. This will produce a `trace.zip` file for each test that was retried.

```js tab=js-test title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  retries: 1,
  use: {
    trace: 'on-first-retry',
  },
});
```

```js tab=js-library
const browser = await chromium.launch();
const context = await browser.newContext();

// Start tracing before creating / navigating a page.
await context.tracing.start({ screenshots: true, snapshots: true });

const page = await context.newPage();
await page.goto('https://playwright.dev');

// Stop tracing and export it into a zip archive.
await context.tracing.stop({ path: 'trace.zip' });
```

Available options to record a trace:
- `'on-first-retry'` - Record a trace only when retrying a test for the first time.
- `'on-all-retries'` - Record traces for all test retries.
- `'off'` - Do not record a trace.
- `'on'` - Record a trace for each test. (not recommended as it's performance heavy)
- `'retain-on-failure'` - Record a trace for each test, but remove it from successful test runs.

You can also use `trace: 'retain-on-failure'` if you do not enable retries but still want traces for failed tests.

There are more granular options available, see `TestOptions.trace`.

**If you are not using Playwright as a Test Runner, use the `BrowserContext.tracing` API instead** (this is the relevant path for a headless-capture/automation tool that is not running under the Playwright Test runner).

### Recording a trace (langs: python, non-pytest)

```python async
browser = await chromium.launch()
context = await browser.new_context()

# Start tracing before creating / navigating a page.
await context.tracing.start(screenshots=True, snapshots=True, sources=True)

page = await context.new_page()
await page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
await context.tracing.stop(path = "trace.zip")
```

### Recording a trace (langs: java)

```java
Browser browser = browserType.launch();
BrowserContext context = browser.newContext();

// Start tracing before creating / navigating a page.
context.tracing().start(new Tracing.StartOptions()
  .setScreenshots(true)
  .setSnapshots(true)
  .setSources(true));

Page page = context.newPage();
page.navigate("https://playwright.dev");

// Stop tracing and export it into a zip archive.
context.tracing().stop(new Tracing.StopOptions()
  .setPath(Paths.get("trace.zip")));
```

This will record the trace and place it into the file named `trace.zip`.

---

## GUIDE: Trace viewer intro (getting-started tutorial page)

### Introduction

Playwright Trace Viewer is a GUI tool that lets you explore recorded Playwright traces of your tests, meaning you can go back and forward through each action of your test and visually see what was happening during each action.

### Recording a Trace

By default the playwright.config file contains the configuration needed to create a `trace.zip` file for each test. Traces are setup to run `on-first-retry`, meaning they run on the first retry of a failed test. Also `retries` are set to 2 when running on CI and 0 locally. This means the traces are recorded on the first retry of a failed test but not on the first run and not on the second retry.

```js title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  retries: process.env.CI ? 2 : 0, // set to 2 when running on CI
  // ...
  use: {
    trace: 'on-first-retry', // record traces on first retry of each test
  },
});
```

Traces are normally run in a Continuous Integration (CI) environment, because locally you can use UI Mode for developing and debugging tests. However, if you want to run traces locally without using UI Mode, you can force tracing to be on with `--trace on`.

```bash
npx playwright test --trace on
```

### Opening the HTML report

```bash
npx playwright show-report
```

### Viewing the trace

View traces of your test by clicking through each action or hovering using the timeline and see the state of the page before and after the action. Inspect the log, source and network, errors, and console during each step of the test. The trace viewer creates a DOM snapshot so you can fully interact with it and open the browser DevTools to inspect the HTML, CSS, etc.

---

## API: class Tracing (context.tracing)

Playwright note (from `Tracing.start`, since v1.12): "You probably want to enable tracing in your config file instead of using `Tracing.start`. The `context.tracing` API captures browser operations and network activity, but it doesn't record test assertions (like `expect` calls). We recommend enabling tracing through Playwright Test configuration, which includes those assertions and provides a more complete trace for debugging test failures."

### async method: Tracing.start(options)
- since: v1.12

Start tracing.

**Usage**

```js
await context.tracing.start({ screenshots: true, snapshots: true });
const page = await context.newPage();
await page.goto('https://playwright.dev');
expect(page.url()).toBe('https://playwright.dev');
await context.tracing.stop({ path: 'trace.zip' });
```

```java
context.tracing().start(new Tracing.StartOptions()
  .setScreenshots(true)
  .setSnapshots(true));
Page page = context.newPage();
page.navigate("https://playwright.dev");
context.tracing().stop(new Tracing.StopOptions()
  .setPath(Paths.get("trace.zip")));
```

```python async
await context.tracing.start(screenshots=True, snapshots=True)
page = await context.new_page()
await page.goto("https://playwright.dev")
await context.tracing.stop(path = "trace.zip")
```

**Options:**

- `name` <string> (since v1.12): If specified, intermediate trace files are going to be saved into the files with the given name prefix inside the `BrowserType.launch.tracesDir` directory specified in `browserType.launch()`. To specify the final trace zip file name, you need to pass `path` option to `Tracing.stop()` instead.

- `screenshots` <boolean> (since v1.12): Whether to capture screenshots during tracing. Screenshots are used to build a timeline preview.

- `snapshots` <boolean|Object> (since v1.12, JS): Which snapshots to capture on every action. Passing `true` is a shortcut for `{ dom: true }`.
  - `dom` ?<boolean> Capture DOM snapshot on every action and record network activity. Optional.
  - `aria` ?<boolean> Capture aria snapshot of the page on every action. Optional.
  - `screen` ?<boolean> Capture a screenshot of the page on every action. Optional.
  (Java/Python/C#: `snapshots` <boolean>: Whether to capture DOM snapshot and record network activity on every action.)

- `ariaSnapshots` <boolean> (since v1.63, langs: java, python, csharp): Whether to capture aria snapshot of the page on every action.

- `screenSnapshots` <boolean> (since v1.63, langs: java, python, csharp): Whether to capture a screenshot of the page on every action.

- `sources` <boolean> (since v1.17): Whether to include source files for trace actions. (Java: List of the directories with source code for the application must be provided via `PLAYWRIGHT_JAVA_SRC` environment variable, paths separated by `;` on Windows and `:` on other platforms.)

- `title` <string> (since v1.17): Trace name to be shown in the Trace Viewer.

- `live` <boolean> (since v1.59): When enabled, the trace is written to an unarchived file that is updated in real time as actions occur, instead of caching changes and archiving them into a zip file at the end. This is useful for live trace viewing during test execution.

### async method: Tracing.startChunk(options)
- since: v1.15

Start a new trace chunk. If you'd like to record multiple traces on the same BrowserContext, use `Tracing.start()` once, and then create multiple trace chunks with `Tracing.startChunk()` and `Tracing.stopChunk()`.

**Usage**

```js
await context.tracing.start({ screenshots: true, snapshots: true });
const page = await context.newPage();
await page.goto('https://playwright.dev');

await context.tracing.startChunk();
await page.getByText('Get Started').click();
// Everything between startChunk and stopChunk will be recorded in the trace.
await context.tracing.stopChunk({ path: 'trace1.zip' });

await context.tracing.startChunk();
await page.goto('http://example.com');
// Save a second trace file with different actions.
await context.tracing.stopChunk({ path: 'trace2.zip' });
```

**Options:**
- `title` <string> (since v1.17): Trace name to be shown in the Trace Viewer.
- `name` <string> (since v1.32): If specified, intermediate trace files are going to be saved into the files with the given name prefix inside the `BrowserType.launch.tracesDir` directory specified in `browserType.launch()`. To specify the final trace zip file name, pass `path` option to `Tracing.stopChunk()` instead.

### async method: Tracing.startHar(path, options)
- since: v1.60
- returns: `<Disposable>`

Start recording a HAR (HTTP Archive) of network activity in this context. The HAR file is written to disk when `Tracing.stopHar()` is called, or when the returned Disposable is disposed. Only one HAR recording can be active at a time per Tracing instance.

**Usage**

```js
await context.tracing.startHar('trace.har');
const page = await context.newPage();
await page.goto('https://playwright.dev');
await context.tracing.stopHar();
```

**Parameter:**
- `path` <path>: Path on the filesystem to write the HAR file to. If the file name ends with `.zip`, the HAR is saved as a zip archive with response bodies attached as separate files.

**Options:**
- `content` <HarContentPolicy<"omit"|"embed"|"attach">>: If `omit`, content is not persisted. If `attach`, resources are persisted as separate files or ZIP entries. If `embed`, content is stored inline the HAR file per HAR spec. Defaults to `attach` for `.zip` output files and to `embed` for all other file extensions.
- `mode` <HarMode<"full"|"minimal">>: When `minimal`, only record information necessary for routing from HAR (omits sizes, timing, page, cookies, security, etc). Defaults to `full`.
- `urlFilter` <string|RegExp>: A glob or regex pattern to filter requests that are stored in the HAR. Defaults to none.
- `resourcesDir` <path> (JS only): Only used together with `content: 'attach'`. When set, response bodies are placed in this directory instead of next to the HAR file. Not compatible with a `.zip` HAR file.

### async method: Tracing.group(name, options) / Tracing.groupEnd()
- since: v1.49
- `group` returns: `<Disposable>`

> **Caution**: Use `test.step` instead when available.

Creates a new group within the trace, assigning any subsequent API calls to this group, until `Tracing.groupEnd()` is called. Groups can be nested and will be visible in the trace viewer.

**Usage**

```java
// All actions between group and groupEnd
// will be shown in the trace viewer as a group.
page.context().tracing().group("Open Playwright.dev > API");
page.navigate("https://playwright.dev/");
page.getByRole(AriaRole.LINK, new Page.GetByRoleOptions().setName("API")).click();
page.context().tracing().groupEnd();
```

**Parameter:** `name` <string>: Group name shown in the trace viewer.

**Option:** `location` ?<Object>: Specifies a custom location for the group to be shown in the trace viewer. Defaults to the location of the `Tracing.group()` call.
  - `file` <string>
  - `line` ?<int>
  - `column` ?<int>

`Tracing.groupEnd()` closes the last group created by `Tracing.group()`.

### async method: Tracing.stop(options)
- since: v1.12

Stop tracing.

**Option:** `path` <path>: Export trace into the file with the given path.

### async method: Tracing.stopChunk(options)
- since: v1.15

Stop the trace chunk. See `Tracing.startChunk()` for more details about multiple trace chunks.

**Option:** `path` <path>: Export trace collected since the last `Tracing.startChunk()` call into the file with the given path.

### async method: Tracing.stopHar()
- since: v1.60

Stop HAR recording and save the HAR file to the path given to `Tracing.startHar()`.
