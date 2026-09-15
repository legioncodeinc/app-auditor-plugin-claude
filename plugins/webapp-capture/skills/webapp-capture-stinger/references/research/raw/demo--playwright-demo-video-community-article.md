# "I Was Tired of Re-Recording Product Demos Every Sprint. So I Built a Tool That Turns Playwright Tests Into Videos." (dev.to)

- URL: https://dev.to/thepatriczek/i-was-tired-of-re-recording-product-demos-every-sprint-so-i-built-a-tool-that-turns-playwright-21od
- Fetched: 2026-09-15
- Source type: community article
- Last updated (if shown): date shown on page rendered as March 26, 2024; treat with caution given the tool it describes (playwright-recast, see below) appears to be actively maintained into 2026 - could not independently confirm which date is accurate at fetch time.

## Context

Companion OSS tool referenced: `playwright-recast` (https://github.com/ThePatriczek/playwright-recast) - "Fluent pipeline library for processing Playwright traces into polished demo videos with TTS voiceover, subtitles, speed control, and zoom."

## Core technique

The tool extracts data from Playwright trace files (ZIP archives containing click events, network requests, screenshots, timestamps, and DOM snapshots) and reconstructs them as polished videos.

## Speed control

The pipeline classifies trace moments into categories and applies differential speed-up:

```javascript
.speedUp({
  duringIdle: 4.0,
  duringUserAction: 1.0,
  duringNetworkWait: 2.0,
})
```

This compresses loading/idle states while maintaining real-time interaction visibility - i.e. don't just apply one global speed multiplier to a demo recording; slow parts (idle/network wait) get sped up more than the parts where the viewer needs to see a user action happen.

## Subtitles and narration

Two methods are supported:

```javascript
.subtitlesFromSrt('./narration.srt')
.voiceover(ElevenLabsProvider({ voiceId: 'daniel' }))
```

The voiceover processor handles timing synchronization, silence padding, and audio concatenation with video.

## Content filtering

Unwanted sequences (like login flows) are removed:

```javascript
.hideSteps(s => s.text?.includes('logged in'))
```

## Zoom transitions

Listed (per the article) as a future/planned feature for animated emphasis on UI elements - not yet implemented at time of writing.

## Cursor handling

The article mentions "cursor positions" are extracted from traces but does not detail click-highlighting implementation specifics in the portion of content retrieved.

## Architecture note

The pipeline is immutable and lazy - methods return new instances until `.toFile()` executes the full rendering chain (a fluent/builder pattern over ffmpeg-style post-processing of Playwright trace data).
