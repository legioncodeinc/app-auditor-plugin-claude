# Playwright Docs - browserType.launch() (slowMo option)

- URL: https://playwright.dev/docs/api/class-browsertype#browser-type-launch
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live versioned docs page, no date shown)

## Method signature

```javascript
browserType.launch();
browserType.launch(options);
```

Returns: `Promise<Browser>`

## Key options relevant to demo/recording use

### slowMo
- Type: `number` (optional)
- Default: `0`
- Description: "Slows down Playwright operations by the specified amount of milliseconds. Useful so that you can see what is going on."

### headless
- Type: `boolean` (optional)
- Default: `true`
- Description: Determines whether the browser runs without a visible UI. More details available for both Chromium and Firefox implementations.

### args
- Type: `Array<string>` (optional)
- Description: "Additional arguments to pass to the browser instance. The list of Chromium flags can be found [here]."
- Warning noted in docs: using custom browser arguments risks breaking Playwright functionality.

## Usage note for demo recording

The `slowMo` option is specifically designed to enable observation of automation actions, making it valuable for creating visual demonstrations or debugging scenarios where you need to monitor what Playwright is executing (e.g. `chromium.launch({ headless: false, slowMo: 250 })` to pace clicks/typing at a human-watchable speed for screen recording).
