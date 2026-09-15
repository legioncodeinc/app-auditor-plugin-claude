# Playwright Docs - Videos (recordVideo browser context option)

- URL: https://playwright.dev/docs/videos
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live versioned docs page, no date shown)

## Overview

Playwright enables recording of browser sessions through the `video` option in test configuration or browser context settings.

## Configuration options (test config `use.video`)

The `video` option supports four modes:
- `'off'` - No recording
- `'on'` - Record all tests
- `'retain-on-failure'` - Keep videos only from failed tests
- `'on-first-retry'` - Record only on initial retry attempts

## Browser-context-level implementation (recordVideo)

At the browser context level, you can enable recording with the `recordVideo` option:

```javascript
const context = await browser.newContext({ recordVideo: { dir: 'videos/' } });
await context.close();
```

Important: the video is only fully written once the browser context is closed - the docs emphasize you must `await browserContext.close()` (or `page.close()`/`browser.close()`) to ensure videos are properly saved.

## Advanced configuration (size and annotations)

Video output supports customization through `size` and `show` (action/test annotation overlay) settings:

```javascript
video: {
  mode: 'on-first-retry',
  size: { width: 640, height: 480 },
  show: {
    actions: { duration: 500, position: 'top-right' },
    test: { level: 'step', position: 'top-left' }
  }
}
```

## Video path access

For multi-page scenarios, retrieve the video file path via:

```javascript
await page.video().path()
```

Note: "the video is only available after the page or browser context is closed."

## Performance / sizing note

The default video size is "scaled down to fit 800x800" with viewport content positioned in the top-left corner. Explicitly set `recordVideo.size` (or the `size` option above) to control the actual recorded resolution instead of relying on the default scale-to-fit behavior - relevant when a demo-video pipeline needs a specific output resolution (e.g. 1920x1080) upstream of any ffmpeg post-processing.
