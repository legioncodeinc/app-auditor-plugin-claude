# BrowserType.connectOverCDP() and BrowserType.launchPersistentContext() API reference
- URL: https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp and https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context
- Fetched: 2026-09-15
- Source type: official docs (API reference, sourced from microsoft/playwright docs/src/api/class-browsertype.md + params.md macros on the `main` branch)
- Last updated (if shown): unknown

## async method: BrowserType.connectOverCDP(endpointURL, options)
- since: v1.9
- returns: `<Browser>`

This method attaches Playwright to an existing browser instance using the Chrome DevTools Protocol.

The default browser context is accessible via `browser.contexts()`.

> **Note**: Connecting over the Chrome DevTools Protocol is only supported for Chromium-based browsers.

> **Note**: This connection is significantly lower fidelity than the Playwright protocol connection via `browserType.connect()`. If you are experiencing issues or attempting to use advanced functionality, you probably want to use `browserType.connect()`.

> **Warning**: Playwright maintains a curated list of arguments for launching the browser. If you launch the browser without Playwright and do not pass the exact same arguments, some of Playwright functionality may be broken upon connecting to the browser.

**Usage**

```js
const browser = await playwright.chromium.connectOverCDP('http://localhost:9222');
const defaultContext = browser.contexts()[0];
const page = defaultContext.pages()[0];
```

```java
Browser browser = playwright.chromium().connectOverCDP("http://localhost:9222");
BrowserContext defaultContext = browser.contexts().get(0);
Page page = defaultContext.pages().get(0);
```

```python async
browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
default_context = browser.contexts[0]
page = default_context.pages[0]
```

```python sync
browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
default_context = browser.contexts[0]
page = default_context.pages[0]
```

```csharp
var browser = await playwright.Chromium.ConnectOverCDPAsync("http://localhost:9222");
var defaultContext = browser.Contexts[0];
var page = defaultContext.Pages[0];
```

### Parameter: endpointURL
- since: v1.11
- `endpointURL` <string>

A CDP websocket endpoint or http url to connect to. For example `http://localhost:9222/` or `ws://127.0.0.1:9222/devtools/browser/387adf4c-243f-4051-a181-46798f4a46f4`.

(JS: `endpointURL` also accepted as an option since v1.14, deprecated in favor of the first positional argument.)

### Options

- `headers` <Object<string, string>> (since v1.11): Additional HTTP headers to be sent with connect request. Optional.
- `isLocal` <boolean> (since v1.58): Tells Playwright that it runs on the same host as the CDP server. It will enable certain optimizations that rely upon the file system being the same between Playwright and the Browser.
- `slowMo` <float> (since v1.11): Slows down Playwright operations by the specified amount of milliseconds. Useful so that you can see what is going on. Defaults to `0`.
- `timeout` <float> (since v1.11): Maximum time in milliseconds to wait for the connection to be established. Defaults to `30000` (30 seconds). Pass `0` to disable timeout.
- `noDefaults` <boolean> (since v1.60): When true, Playwright will not apply its default overrides to the existing default browser context. Specifically, `Browser.newContext.acceptDownloads` is left at the browser's setting, focus emulation is not enabled, and media emulation options (such as `colorScheme`, `reducedMotion`, `forcedColors`, and `contrast`) are not applied. Useful when attaching to a user's daily-driver browser where these overrides would interfere with existing browser state. New contexts created via `browser.newContext()` are not affected. Defaults to `false`.
- `artifactsDir` <path> (since v1.61): If specified, browser artifacts (such as traces and downloads) are saved into this directory.

---

## async method: BrowserType.launchPersistentContext(userDataDir, options)
- since: v1.8
- returns: `<BrowserContext>`

Returns the persistent browser context instance.

Launches browser that uses persistent storage located at `userDataDir` and returns the only context. Closing this context will automatically close the browser.

### Parameter: userDataDir
- since: v1.8
- `userDataDir` <path>

Path to a User Data Directory, which stores browser session data like cookies and local storage. Pass an empty string to create a temporary directory.

More details for Chromium and Firefox user data directories. Chromium's user data directory is the **parent** directory of the "Profile Path" seen at `chrome://version`.

Note that browsers do not allow launching multiple instances with the same User Data Directory.

> **Warning**: Chromium/Chrome: Due to recent Chrome policy changes, automating the default Chrome user profile is not supported. Pointing `userDataDir` to Chrome's main "User Data" directory (the profile used for your regular browsing) may result in pages not loading or the browser exiting. Create and use a separate directory (for example, an empty folder) as your automation profile instead. See https://developer.chrome.com/blog/remote-debugging-port for details.

### Options

`launchPersistentContext` accepts the union of:
1. The **shared browser launch options** list (same as `browserType.launch()`):
   - `args` <Array<string>>: additional arguments to pass to the browser instance. (Warning: custom browser args at your own risk, may break Playwright functionality.)
   - `channel` <string>: browser distribution channel. Use `"chromium"` to opt in to new headless mode. Use `"chrome"`, `"chrome-beta"`, `"chrome-dev"`, `"chrome-canary"`, `"msedge"`, `"msedge-beta"`, `"msedge-dev"`, or `"msedge-canary"` for branded Chrome/Edge.
   - `chromiumSandbox` <boolean>: Enable Chromium sandboxing. Defaults to `false`.
   - `downloadsPath` <path>: If specified, accepted downloads are downloaded into this directory. Otherwise a temporary directory is created and deleted when the browser is closed. In either case, downloads are deleted when the browser context they were created in is closed.
   - `env` <Object<string, string>>: environment variables visible to the browser. Defaults to `process.env`.
   - `executablePath` <path>: Path to a browser executable to run instead of the bundled one. Playwright only officially supports the bundled Chromium, Firefox, or WebKit: use at your own risk.
   - `handleSIGINT` <boolean>: Close the browser process on Ctrl-C. Defaults to `true`.
   - `headless` <boolean>: whether to run in headless mode.
   - `ignoreDefaultArgs` <boolean|Array<string>>: whether to ignore the default list of Playwright-curated launch args, or a subset of them.
   - `proxy` <Object>: network proxy settings.
   - `timeout` <float>: max time in ms to wait for the browser instance to start. Defaults to `30000` (30 seconds). Pass `0` to disable timeout.
   - `tracesDir` <path>: location to write Playwright trace files.
   - `artifactsDir` <path>
2. `slowMo` <float>: Slows down Playwright operations by the specified amount of milliseconds.
3. `ignoreDefaultArgs` (C#/Java flavor) and `ignoreAllDefaultArgs` (since v1.9): bypass the full default-args list.
4. The **shared context options** list: i.e. the same options as `browser.newContext()`: `viewport`, `deviceScaleFactor`, `colorScheme`, `reducedMotion`, `forcedColors`, `contrast`, `locale`, `timezoneId`, `geolocation`, `permissions`, `extraHTTPHeaders`, `offline`, `httpCredentials`, `recordHar`/`recordHarPath` etc., `recordVideo`/`recordVideoDir` etc., `userAgent`, `isMobile`, `hasTouch`, `javaScriptEnabled`, `acceptDownloads`, `ignoreHTTPSErrors`, `bypassCSP`, `baseURL`, `screen`, `strictSelectors`, `serviceWorkers`. (See the `playwright--browser-context-options.md` archive file for the full per-option table: `launchPersistentContext` does NOT take `storageState`, since it always launches from the given `userDataDir`'s existing persistent storage.)
   - `firefoxUserPrefs` (since v1.40, JS/Python) / `firefoxUserPrefs2` (C#/Java): Firefox user preferences object.
5. `clientCertificates` (since 1.46): TLS client authentication configuration.

**Key distinction vs. `browser.newContext()`**: `launchPersistentContext` combines browser *launch* options and browser *context* options into a single call, and returns the context directly (there's no separate `Browser` object exposed in the return type semantics) because the persistent profile IS the browser session: closing the context closes the browser.
