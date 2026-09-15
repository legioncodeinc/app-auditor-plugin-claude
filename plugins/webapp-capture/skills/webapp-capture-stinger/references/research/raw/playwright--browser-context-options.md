# Browser.newContext(): Browser context options API reference
- URL: https://playwright.dev/docs/api/class-browser#browser-new-context
- Fetched: 2026-09-15
- Source type: official docs (API reference, sourced from microsoft/playwright docs/src/api/class-browser.md + params.md macros on the `main` branch)
- Last updated (if shown): unknown (no per-page date shown on playwright.dev)

## async method: Browser.newContext()

- since: v1.8
- returns: `<BrowserContext>`

Creates a new browser context. It won't share cookies/cache with other browser contexts.

> **Note**: If directly using this method to create BrowserContexts, it is best practice to explicitly close the returned context via `browserContext.close()` when your code is done with the BrowserContext, and before calling `browser.close()`. This will ensure the `context` is closed gracefully and any artifacts: like HARs and videos: are fully flushed and saved.

**Usage**

```js
(async () => {
  const browser = await playwright.firefox.launch();  // Or 'chromium' or 'webkit'.
  // Create a new incognito browser context.
  const context = await browser.newContext();
  // Create a new page in a pristine context.
  const page = await context.newPage();
  await page.goto('https://example.com');

  // Gracefully close up everything
  await context.close();
  await browser.close();
})();
```

```python async
browser = await playwright.firefox.launch() # or "chromium" or "webkit".
# create a new incognito browser context.
context = await browser.new_context()
# create a new page in a pristine context.
page = await context.new_page()
await page.goto("https://example.com")

# gracefully close up everything
await context.close()
await browser.close()
```

---

## Options (full table)

### acceptDownloads
- `acceptDownloads` <boolean>

Whether to automatically download all the attachments. Defaults to `true` where all the downloads are accepted.

### ignoreHTTPSErrors
- `ignoreHTTPSErrors` <boolean>

Whether to ignore HTTPS errors when sending network requests. Defaults to `false`.

### bypassCSP
- `bypassCSP` <boolean>

Toggles bypassing page's Content-Security-Policy. Defaults to `false`.

### baseURL
- `baseURL` <string>

When using `page.goto()`, `page.route()`, `page.waitForURL()`, `page.waitForRequest()`, or `page.waitForResponse()` it takes the base URL in consideration by using the `URL()` constructor for building the corresponding URL. Unset by default. Examples:
- baseURL: `http://localhost:3000` and navigating to `/bar.html` results in `http://localhost:3000/bar.html`
- baseURL: `http://localhost:3000/foo/` and navigating to `./bar.html` results in `http://localhost:3000/foo/bar.html`
- baseURL: `http://localhost:3000/foo` (without trailing slash) and navigating to `./bar.html` results in `http://localhost:3000/bar.html`

### viewport
- (JS/Java) `viewport` <null|Object>
  - `width` <int> page width in pixels.
  - `height` <int> page height in pixels.

Emulates consistent viewport for each page. Defaults to an 1280x720 viewport. Use `null` to disable the consistent viewport emulation. Learn more about viewport emulation.

> **Note**: The `null` value opts out from the default presets, makes viewport depend on the host window size defined by the operating system. It makes the execution of the tests non-deterministic.

(C#: same concept via `ViewportSize.NoViewport` to disable.)

### screen
- `screen` <Object>
  - `width` <int> page width in pixels.
  - `height` <int> page height in pixels.

Emulates consistent window screen size available inside web page via `window.screen`. Is only used when `viewport` is set.

### userAgent
- `userAgent` <string>

Specific user agent to use in this context.

### deviceScaleFactor
- `deviceScaleFactor` <float>

Specify device scale factor (can be thought of as dpr). Defaults to `1`. Learn more about emulating devices with device scale factor.

### isMobile
- `isMobile` <boolean>

Whether the `meta viewport` tag is taken into account and touch events are enabled. isMobile is a part of device, so you don't actually need to set it manually. Defaults to `false` and is not supported in Firefox.

### hasTouch
- `hasTouch` <boolean>

Specifies if viewport supports touch events. Defaults to false.

### javaScriptEnabled
- `javaScriptEnabled` <boolean>

Whether or not to enable JavaScript in the context. Defaults to `true`.

### timezoneId
- `timezoneId` <string>

Changes the timezone of the context. See ICU's metaZones.txt for a list of supported timezone IDs. Defaults to the system timezone.

### geolocation
- `geolocation` <Object>
  - `latitude` <float> Latitude between -90 and 90.
  - `longitude` <float> Longitude between -180 and 180.
  - `accuracy` ?<float> Non-negative accuracy value. Defaults to `0`.

### locale
- `locale` <string>

Specify user locale, for example `en-GB`, `de-DE`, etc. Locale will affect `navigator.language` value, `Accept-Language` request header value as well as number and date formatting rules. Defaults to the system default locale. Learn more about emulation in the emulation guide (locale & timezone).

### permissions
- `permissions` <Array<string>>

A list of permissions to grant to all pages in this context. See `browserContext.grantPermissions()` for more details. Defaults to none.

### extraHTTPHeaders
- `extraHTTPHeaders` <Object<string, string>>

An object containing additional HTTP headers to be sent with every request. Defaults to none.

### offline
- `offline` <boolean>

Whether to emulate network being offline. Defaults to `false`.

### httpCredentials
- `httpCredentials` <Object|Array<Object>>
  - `username` <string>
  - `password` <string>
  - `origin` ?<string> Restrain sending http credentials on specific origin (scheme://host:port).
  - `send` ?<HttpCredentialsSend<"unauthorized"|"always">> This option only applies to the requests sent from corresponding APIRequestContext and does not affect requests sent from the browser. `'always'` - `Authorization` header with basic authentication credentials will be sent with each API request. `'unauthorized'` - the credentials are only sent when 401 (Unauthorized) response with `WWW-Authenticate` header is received. Defaults to `'unauthorized'`.

Credentials for HTTP authentication. If no origin is specified, the username and password are sent to any servers upon unauthorized responses. Pass an array to use different credentials for different origins. The first entry that matches the request origin is used, and entries with no origin match any request.

### colorScheme
- JS/Java: `colorScheme` <null|ColorScheme<"light"|"dark"|"no-preference">>
- C#/Python: `colorScheme` <ColorScheme<"light"|"dark"|"no-preference"|"null">>

Emulates prefers-colors-scheme media feature, supported values are `'light'` and `'dark'`. See `page.emulateMedia()` for more details. Passing `null` resets emulation to system defaults. Defaults to `'light'`.

### reducedMotion
- JS/Java: `reducedMotion` <null|ReducedMotion<"reduce"|"no-preference">>
- C#/Python: `reducedMotion` <ReducedMotion<"reduce"|"no-preference"|"null">>

Emulates `'prefers-reduced-motion'` media feature, supported values are `'reduce'`, `'no-preference'`. See `page.emulateMedia()` for more details. Passing `null` resets emulation to system defaults. Defaults to `'no-preference'`.

### forcedColors
- JS/Java: `forcedColors` <null|ForcedColors<"active"|"none">>
- C#/Python: `forcedColors` <ForcedColors<"active"|"none"|"null">>

Emulates `'forced-colors'` media feature, supported values are `'active'`, `'none'`. Passing `null` resets emulation to system defaults. Defaults to `'none'`.

### contrast
- JS/Java: `contrast` <null|Contrast<"no-preference"|"more">>
- C#/Python: `contrast` <Contrast<"no-preference"|"more"|"null">>

Emulates `'prefers-contrast'` media feature, supported values are `'no-preference'`, `'more'`. Passing `null` resets emulation to system defaults. Defaults to `'no-preference'`.

### logger (deprecated)
- `logger` <Logger> (JS)

Logger sink for Playwright logging. Deprecated: the logs received by the logger are incomplete. Please use tracing instead.

### recordHar
- (JS) `recordHar` <Object>
  - `omitContent` ?<boolean> Optional setting to control whether to omit request content from the HAR. Defaults to `false`. Deprecated, use `content` policy instead.
  - `content` ?<HarContentPolicy<"omit"|"embed"|"attach">> Optional setting to control resource content management. If `omit` is specified, content is not persisted. If `attach` is specified, resources are persisted as separate files or entries in the ZIP archive. If `embed` is specified, content is stored inline the HAR file as per HAR specification. Defaults to `attach` for `.zip` output files and to `embed` for all other file extensions.
  - `path` <path> Path on the filesystem to write the HAR file to. If the file name ends with `.zip`, `content: 'attach'` is used by default.
  - `mode` ?<HarMode<"full"|"minimal">> When set to `minimal`, only record information necessary for routing from HAR. This omits sizes, timing, page, cookies, security and other types of HAR information that are not used when replaying from HAR. Defaults to `full`.
  - `urlFilter` ?<string|RegExp> A glob or regex pattern to filter requests that are stored in the HAR. When a `baseURL` via the context options was provided and the passed URL is a path, it gets merged via the `new URL()` constructor. Defaults to none.

Enables HAR recording for all pages into `recordHar.path` file. If not specified, the HAR is not recorded. Make sure to await `browserContext.close()` for the HAR to be saved.

(C#/Java/Python use flat options instead: `recordHarPath` <path>, `recordHarOmitContent` ?<boolean> (default `false`), `recordHarContent` ?<HarContentPolicy<"omit"|"embed"|"attach">> (default `embed`, note: differs from the JS default of `attach`-for-zip), `recordHarMode` ?<HarMode<"full"|"minimal">> (default `full`), `recordHarUrlFilter` ?<string|RegExp>.)

### recordVideo
- (JS) `recordVideo` <Object>
  - `dir` ?<path> Path to the directory to put videos into. If not specified, the videos will be stored in `artifactsDir` (see `browserType.launch()` options).
  - `size` ?<Object> Optional dimensions of the recorded videos. If not specified the size will be equal to `viewport` scaled down to fit into 800x800. If `viewport` is not configured explicitly the video size defaults to 800x450. Actual picture of each page will be scaled down if necessary to fit the specified size.
    - `width` <int> Video frame width.
    - `height` <int> Video frame height.
  - `showActions` ?<Object> If specified, enables visual annotations on interacted elements during video recording.
    - `duration` ?<float> How long each annotation is displayed in milliseconds. Defaults to `500`.
    - `position` ?<AnnotatePosition<"top-left"|"top"|"top-right"|"bottom-left"|"bottom"|"bottom-right">> Position of the action title overlay. Defaults to `"top-right"`.
    - `fontSize` ?<int> Font size of the action title in pixels. Defaults to `24`.
    - `cursor` ?<ScreencastCursor<"none"|"pointer">> Cursor decoration shown for pointer actions. `"pointer"` (the default) renders a mouse pointer that animates from the previous action point to the next one. `"none"` disables the cursor decoration.

Enables video recording for all pages into `recordVideo.dir` directory. If not specified videos are not recorded. Make sure to await `browserContext.close()` for videos to be saved.

(C#/Java/Python use flat options instead: `recordVideoDir` <path>, `recordVideoSize` <Object> with `width`/`height`: same default-size behavior as above.)

### storageState
- (JS/Python) `storageState` <path|Object>
  - `cookies` <Array<Object>> Cookies to set for context
    - `name` <string>
    - `value` <string>
    - `domain` <string> Domain and path are required. For the cookie to apply to all subdomains as well, prefix domain with a dot, like this: `.example.com`
    - `path` <string> Domain and path are required
    - `expires` <float> Unix time in seconds.
    - `httpOnly` <boolean>
    - `secure` <boolean>
    - `sameSite` <SameSiteAttribute<"Strict"|"Lax"|"None">> sameSite flag
  - `origins` <Array<Object>>
    - `origin` <string>
    - `localStorage` <Array<Object>> localStorage to set for context
      - `name` <string>
      - `value` <string>

Learn more about storage state and auth. Populates context with given storage state. This option can be used to initialize context with logged-in information obtained via `browserContext.storageState()`.

(C#/Java: `storageState` <string>: same purpose, JSON string form; plus `storageStatePath` <path> since v1.9: path to the file with saved storage state.)

### strictSelectors
- `strictSelectors` <boolean>

If set to true, enables strict selectors mode for this context. Defaults to `false`.

### proxy
- `proxy` <Object>: network proxy settings to use with this context. (See `browserType.launch()` `proxy` option for the shared shape: `server`, `bypass`, `username`, `password`.)

### clientCertificates
- since: 1.46
- `clientCertificates` <Array<Object>>: TLS client authentication configuration.

> When using WebKit on macOS, accessing `localhost` will not pick up client certificates. You can make it work by replacing `localhost` with `local.playwright`.

### serviceWorkers
- `serviceWorkers` <"allow"|"block">

Whether to allow sites to register Service workers. Defaults to `'allow'`.

---

## Summary table (as rendered on playwright.dev)

| Option | Type | Default | Notes |
|---|---|---|---|
| acceptDownloads | boolean | true | |
| baseURL | string | unset | affects goto/route/waitForURL/waitForRequest/waitForResponse |
| bypassCSP | boolean | false | |
| clientCertificates | Array<Object> |: | since 1.46 |
| colorScheme | null\|"light"\|"dark"\|"no-preference" | 'light' | |
| contrast | null\|"no-preference"\|"more" | 'no-preference' | |
| deviceScaleFactor | number | 1 | dpr |
| extraHTTPHeaders | Object<string,string> | none | |
| forcedColors | null\|"active"\|"none" | 'none' | |
| geolocation | Object |: | latitude/longitude/accuracy |
| hasTouch | boolean | false | not supported in Firefox |
| httpCredentials | Object\|Array<Object> |: | |
| ignoreHTTPSErrors | boolean | false | |
| isMobile | boolean | false | not supported in Firefox |
| javaScriptEnabled | boolean | true | |
| locale | string | system default | |
| offline | boolean | false | |
| permissions | Array<string> | none | |
| proxy | Object | none | |
| recordHar | Object |: | dir/path, mode, content, omitContent, urlFilter |
| recordVideo | Object |: | dir, size (width/height), showActions |
| reducedMotion | null\|"reduce"\|"no-preference" | 'no-preference' | |
| screen | Object |: | only used when viewport is set |
| serviceWorkers | "allow"\|"block" | 'allow' | |
| storageState | string\|Object |: | |
| strictSelectors | boolean | false | |
| timezoneId | string | system timezone | |
| userAgent | string |: | |
| viewport | null\|Object | 1280x720 | null disables consistent viewport emulation |
