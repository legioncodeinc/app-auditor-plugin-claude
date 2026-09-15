# Create speech - ElevenLabs Documentation (Text to Speech API)

- URL: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- Fetched: 2026-09-15
- Source type: vendor docs
- Last updated (if shown): unknown (live API reference page, no date shown)

## Endpoint

- **HTTP Method**: POST
- **URL**: `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- **Authentication**: header `xi-api-key` with API key value

## Path parameters

- `voice_id` (string, required) - "ID of the voice to be used"

## Request body (application/json)

**Required:**
- `text` (string) - "The text that will get converted into speech"

**Optional:**
- `model_id` (string, default: `eleven_multilingual_v2`)
- `output_format` (enum, default: `mp3_44100_128`)
- `language_code` (string, nullable)
- `voice_settings` (object, nullable):
  - `stability` (double, default: 0.5)
  - `similarity_boost` (double, default: 0.75)
  - `use_speaker_boost` (boolean, default: true)
  - `style` (double, default: 0)
  - `speed` (double, default: 1)
- `seed` (integer, nullable, range: 0-4294967295)
- `apply_text_normalization` (enum, default: `auto`)
- `pronunciation_dictionary_locators` (list of objects, max 3)
- Additional continuity parameters: `previous_text`, `next_text`, `previous_request_ids`, `next_request_ids`

## Response

- **Status 200**: "The generated audio file" (binary audio data in the requested `output_format`)
- **Status 422**: Validation error with a `detail` array containing `loc`, `msg`, `type`

## Notes for a narration pipeline

- `output_format` controls the audio container/bitrate (default `mp3_44100_128` = MP3 at 44.1kHz/128kbps); other formats include PCM and mu-law variants per ElevenLabs' broader docs.
- `voice_settings.speed` (default 1) can be used to slow/speed the generated narration independent of ffmpeg's `atempo` filter (see `demo--ffmpeg-speed-setpts-atempo.md` in this archive) if fine timing alignment to a fixed video duration is needed.
- The `previous_text`/`next_text`/`previous_request_ids`/`next_request_ids` fields exist to preserve prosody continuity when generating a long narration script in multiple chunked API calls (relevant for multi-scene demo videos).
