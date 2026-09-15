# Create speech - OpenAI API Reference (Audio / Text-to-Speech)

- URL: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create (mirrors https://platform.openai.com/docs/api-reference/audio/createSpeech)
- Fetched: 2026-09-15
- Source type: vendor docs
- Last updated (if shown): unknown (live API reference page, no date shown)

## Endpoint

- **HTTP Method**: POST
- **URL path**: `/v1/audio/speech` (full URL `https://api.openai.com/v1/audio/speech`)

## Authentication

Bearer token via `Authorization` header:
```
Authorization: Bearer $OPENAI_API_KEY
```

## Request body parameters

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `input` | string (required) | - | "The text to generate audio for. The maximum length is 4096 characters." |
| `model` | string (required) | - | Options: `tts-1`, `tts-1-hd`, `gpt-4o-mini-tts`, `gpt-4o-mini-tts-2025-12-15` |
| `voice` | string (required) | - | Built-in voices: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse, marin, cedar. Also accepts custom voice objects with an `id` property. |
| `instructions` | string (optional) | - | "Control the voice of your generated audio with additional instructions." Not compatible with `tts-1`/`tts-1-hd`. |
| `response_format` | string (optional) | `mp3` | Supported: mp3, opus, aac, flac, wav, pcm |
| `speed` | number (optional) | `1.0` | Range: 0.25 to 4.0 |

## Response

Audio file content, or a stream of audio events; format determined by the `response_format` parameter.

## Supported output formats

- **MP3** (default)
- **Opus** (low latency streaming)
- **AAC** (YouTube, Android, iOS)
- **FLAC** (lossless)
- **WAV** (uncompressed, low-latency)
- **PCM** (raw 24kHz samples)

## Example request (curl, verbatim pattern from docs)

```bash
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "Today is a wonderful day to build something people love!",
    "voice": "coral",
    "instructions": "Speak in a cheerful and positive tone."
  }' \
  --output speech.mp3
```

## Notes for a narration pipeline

- The `speed` parameter (0.25-4.0, default 1.0) can pace narration to match a target video duration directly at generation time, as an alternative or complement to ffmpeg's `atempo` audio filter (see `demo--ffmpeg-speed-setpts-atempo.md` in this archive).
- `input` has a hard 4096-character limit per request, so a long demo-video narration script may need to be chunked into multiple `createSpeech` calls and concatenated (see `demo--ffmpeg-concat-demuxer.md` for the concat approach on the resulting audio/video segments).
- `response_format: wav` or `pcm` avoids a lossy re-encode step if the output will immediately be muxed into a video with ffmpeg.
