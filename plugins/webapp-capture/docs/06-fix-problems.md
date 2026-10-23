# 6. Fix problems

**[Home](../../../README.md)** · [All guides](README.md) · [Previous: 5. Make money with it](05-make-money.md)

Find what you see in the left column, then do what the right column says. Most fixes are one sentence you type to Claude.

**First rule:** when something breaks, type `/webapp-capture doctor` (in Claude) or "check the Replicate video connection without generating anything" (in ChatGPT). Both list the problem and the fix.

## Installing

| What you see | What to do |
| --- | --- |
| No **Code** tab in the app | Update the Claude desktop app and check that your plan includes Claude Code (Pro, Max, Team or Enterprise). |
| `command not found: claude` in the Terminal panel | Close the panel, open it again, and retry. Still broken? Ask in the Code tab: "why can't the terminal panel find the claude command?" |
| `/webapp-capture` does nothing or is unknown | The plugin is not installed or not loaded. Redo [1. Install everything, step 3](01-install-everything.md#step-3-install-this-plugin), then start a new session. Plugins do not load in cloud or WSL sessions. |
| The doctor says **no Chromium** | Type: "install the browser the doctor asked for". Claude runs `npx playwright install chromium`. |
| The doctor says **ffmpeg not found** | Type: "install ffmpeg for me". Then start a new session and run the doctor again. |
| The doctor says **origin unreachable** | Your app is not running, or the address is wrong. Open the address in your normal browser to check. |

## Logging in

| What you see | What to do |
| --- | --- |
| The login window closed or **timed out** | Type: "run the login step again". Log in within the time shown and do not close the window yourself. |
| Every page errors with **session expired** | Your login ran out. Type: "run the login step again". |
| The doctor shows an early cookie expiry | Usually fine. Many apps renew your login quietly. Only log in again if pages start failing. |
| Pictures show the login page instead of the app | Your app keeps you logged in only while the browser is open. Ask Claude to "test one page before the full run". |

## Demo videos

| What you see | What to do |
| --- | --- |
| Claude will not record | The plan is not approved yet. Read it and type "yes, approved". |
| **Refusing to rerun: writes would repeat** | An earlier take already changed your data. Reset your test data (or let Claude pick new free slots), then type "Retake the demo". |
| A scene says **mismatch** | The change did not happen the way the plan said. Open `findings.md` and the screenshot in `failures/`. Tell Claude what you see. It is either the app, the test data, or the plan. |
| A scene says **refusing destructive-looking demo control** | The plan tried to click something like Delete or Log out. That is blocked on purpose. Change the plan to avoid that button. |
| The demo hangs on a page | The page keeps loading forever (live updates). Ask Claude to "wait for the element instead of the page load". |
| **OVERRUN** in the narration fit | A line is too long for its scene. Type: "Shorten the narration in scene 2 and rebuild the captions". |
| Private info shows in the contact sheets | Tell Claude what to hide (for example "mask the email column"), then retake. |
| `make-video.sh` **refused** | The final files already exist. Ask Claude to "make the video in a fresh copy of the folder". |

## ChatGPT, voice and intro

| What you see | What to do |
| --- | --- |
| **The handoff refuses**: run review-demo first | Run the privacy review ([guide 2, step 9](02-your-first-demo-video.md#step-9-check-the-privacy-review)), check the pictures, then run `/webapp-capture handoff` again. |
| **Missing narration/audio/...** | A voice clip was not saved. Ask ChatGPT to make the missing line again. |
| A voice clip **is too long** for its line | Ask ChatGPT to shorten that line and make it again. |
| The doctor says **no Replicate token** | Follow [Get your Replicate token](04-finish-in-chatgpt.md#get-your-replicate-token-about-3-minutes). Restart the app after saving it. |
| Replicate says payment or billing is needed | Set up billing at [replicate.com/account/billing](https://replicate.com/account/billing). |
| The intro has warped hands, melted objects or fake text | Do not use it. Ask for a new render with a simpler prompt, or use free stock B-roll instead. |
| `finished/` already exists | The script never overwrites. Rename the old `finished` folder, then run it again. |

## Files and folders

| What you see | What to do |
| --- | --- |
| Files ended up in `library/design/library/design` | The output path in `capture.config.json` repeated the folder name. Use the short path the doctor suggests. |
| Can't find the video | Look in `library/design/demo/<title>/demo.mp4`, or ask Claude "where is the demo video?" |

## Still stuck?

- Set `WEBAPP_CAPTURE_DEBUG=1` before a script to see the full error.
- Read [SUPPORT.md](../../../SUPPORT.md) for how to report a bug. Include what you typed, what you saw, and the doctor output. Never include tokens, passwords or customer data.

**[Home](../../../README.md)** · [All guides](README.md) · [Previous: 5. Make money with it](05-make-money.md)
