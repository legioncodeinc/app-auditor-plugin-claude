# Videos (guide) + Video class / page.video() API reference
- URL: https://playwright.dev/docs/videos and https://playwright.dev/docs/api/class-video and https://playwright.dev/docs/api/class-page#page-video
- Fetched: 2026-09-15
- Source type: official docs (guide + API reference, sourced from microsoft/playwright docs/src/videos.md, docs/src/api/class-video.md, docs/src/api/class-page.md on the `main` branch)
- Last updated (if shown): unknown

## GUIDE: Videos

### Introduction

With Playwright you can record videos for your tests.

### Record video (Playwright Test / JS)

Playwright Test can record videos for your tests, controlled by the `video` option in your Playwright config. By default videos are off.

- `'off'` - Do not record video.
- `'on'` - Record video for each test.
- `'retain-on-failure'` - Record video for each test, but remove all videos from successful test runs.
- `'on-first-retry'` - Record video only when retrying a test for the first time.

Video files will appear in the test output directory, typically `test-results`. See `TestOptions.video` for advanced video configuration.

**Videos are saved upon browser context closure at the end of a test.** If you create a browser context manually, make sure to await `browserContext.close()`.

```js tab=js-test title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  use: {
    video: 'on-first-retry',
  },
});
```

```js tab=js-library
const context = await browser.newContext({ recordVideo: { dir: 'videos/' } });
// Make sure to await close, so that videos are saved.
await context.close();
```

You can also specify video size and annotation. The video size defaults to the viewport size scaled down to fit 800x800. The video of the viewport is placed in the top-left corner of the output video, scaled down to fit if necessary. You may need to set the viewport size to match your desired video size.

When `show: { actions }` is specified, each action will be visually highlighted in the video with the element outline and action title subtitle. The optional `duration` property controls how long each annotation is displayed (defaults to `500`ms).

When `show: { test }` is specified, video will be annotated with the current test information with configurable `level`.

```js title="playwright.config.ts"
import { defineConfig } from '@playwright/test';
export default defineConfig({
  use: {
    video: {
      mode: 'on-first-retry',
      size: { width: 640, height: 480 },
      show: {
        actions: {
          duration: 500,
          position: 'top-right',
          fontSize: 14,
        },
        test: {
          level: 'step',
          position: 'top-left',
          fontSize: 12,
        }
      },
    },
  },
});
```

For multi-page scenarios, you can access the video file associated with the page via `page.video()`.

```js
const path = await page.video().path();
```

> **Note**: Note that the video is only available after the page or browser context is closed.

### Record video (Python / Java / C#)

Videos are saved upon browser context closure at the end of a test. If you create a browser context manually, make sure to await `browserContext.close()`.

```js
const context = await browser.newContext({ recordVideo: { dir: 'videos/' } });
// Make sure to await close, so that videos are saved.
await context.close();
```

```java
context = browser.newContext(new Browser.NewContextOptions().setRecordVideoDir(Paths.get("videos/")));
// Make sure to close, so that videos are saved.
context.close();
```

```python async
context = await browser.new_context(record_video_dir="videos/")
# Make sure to await close, so that videos are saved.
await context.close()
```

```python sync
context = browser.new_context(record_video_dir="videos/")
# Make sure to close, so that videos are saved.
context.close()
```

```csharp
var context = await browser.NewContextAsync(new()
{
    RecordVideoDir = "videos/"
});
// Make sure to close, so that videos are saved.
await context.CloseAsync();
```

You can also specify video size. The video size defaults to the viewport size scaled down to fit 800x800. The video of the viewport is placed in the top-left corner of the output video, scaled down to fit if necessary. You may need to set the viewport size to match your desired video size.

```js
const context = await browser.newContext({
  recordVideo: {
    dir: 'videos/',
    size: { width: 640, height: 480 },
  }
});
```

```java
BrowserContext context = browser.newContext(new Browser.NewContextOptions()
  .setRecordVideoDir(Paths.get("videos/"))
  .setRecordVideoSize(640, 480));
```

```python async
context = await browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 640, "height": 480}
)
```

```csharp
var context = await browser.NewContextAsync(new()
{
    RecordVideoDir = "videos/",
    RecordVideoSize = new RecordVideoSize() { Width = 640, Height = 480 }
});
// Make sure to close, so that videos are saved.
await context.CloseAsync();
```

Saved video files will appear in the specified folder. They all have generated unique names. For the multi-page scenarios, you can access the video file associated with the page via `page.video()`.

```js
const path = await page.video().path();
```

```java
path = page.video().path();
```

```python async
path = await page.video.path()
```

```python sync
path = page.video.path()
```

```csharp
var path = await page.Video.PathAsync();
```

> **Note**: Note that the video is only available after the page or browser context is closed.

---

## API: page.video()

- since: v1.8
- returns: `<null|Video>`

Video object associated with this page. Can be used to access the video file when using the `recordVideo` context option.

---

## API: class Video

- since: v1.8

When browser context is created with the `recordVideo` option, each page has a video object associated with it.

```js
console.log(await page.video().path());
```

```java
System.out.println(page.video().path());
```

```python async
print(await page.video.path())
```

```python sync
print(page.video.path())
```

```csharp
Console.WriteLine(await page.Video.GetPathAsync());
```

### async method: Video.delete()
- since: v1.11

Deletes the video file. Will wait for the video to finish if necessary.

### async method: Video.path()
- since: v1.8
- returns: `<path>`

Returns the file system path this video will be recorded to. **The video is guaranteed to be written to the filesystem upon closing the browser context.** This method throws when connected remotely.

### method/async method: Video.saveAs(path)
- since: v1.11

Saves the video to a user-specified path.

- JS: It is safe to call this method while the video is still in progress, or after the page has closed. This method waits until the page is closed and the video is fully saved.
- Java: This must be called after `page.close()` (or `browserContext.close()`), otherwise an error will be thrown. This method waits until the video is fully saved.
- Python: If using the sync API, this must be called after `page.close()` (or `browserContext.close()`), otherwise an error will be thrown. If using the async API, it is safe to call this method while the video is still in progress, or after the page has closed. This method waits until the page is closed and the video is fully saved.

**Parameter**: `path` <path>: Path where the video should be saved.

---

## Format and size behavior (consolidated from the above)

- Video format: `.webm` (Playwright's video files are WebM; not stated as a separate macro but implied by the `dir`/output file naming: files get generated unique names in the output directory).
- Default size: equal to `viewport` scaled down to fit into 800x800. If `viewport` is not configured explicitly, the video size defaults to 800x450.
- If an explicit `size` (`recordVideo.size` / `recordVideoSize`) is given, the actual picture of each page is scaled down if necessary to fit the specified size; the video of the viewport is placed in the top-left corner of the output video.
- Videos are only finalized/written to disk when the owning browser context (or page, per-language semantics above) is closed: always `await browserContext.close()` (or ensure the page/context closes) before reading `video.path()` / calling `saveAs()` in the sync/Java path.
