# kwaivgi/kling-v3-video: character and scene guide

Tool: `replicate_kling_v3`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/kwaivgi/kling-v3-video), [archived card](../references/research/raw/kwaivgi--kling-v3-video.md), [exact schema](../references/research/raw/kwaivgi--kling-v3-video--schema.json).

## Choose the shot

Choose this for a timed sequence of character shots with an exact shot-duration budget. Use start/end frames when opening and ending compositions matter. Use pro or 4k intentionally; longer or higher-resolution jobs affect spending.

## Direct the scene

Write a short overall premise in prompt, then place each shot description and integer duration in multi_prompt. Repeat the distinguishing character details in every shot. State how each shot begins and ends, keep dialogue brief, and budget time for the action. multi_prompt must be a JSON string, not an array in the tool arguments.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | See description | Text prompt for video generation. Max 2500 characters. |
| `negative_prompt` | string | optional | default "" | Things you do not want to see in the video. Max 2500 characters. |
| `start_image` | string | optional | See description | First frame image. Supports .jpg/.jpeg/.png, max 10MB, min 300px, aspect ratio 1:2.5 to 2.5:1. |
| `end_image` | string | optional | See description | Last frame image. Requires start_image. Supports .jpg/.jpeg/.png, max 10MB, min 300px. |
| `mode` | string | optional | standard / pro / 4k; default "pro" | 'standard' generates 720p, 'pro' generates 1080p, '4k' generates 4K. |
| `aspect_ratio` | string | optional | 16:9 / 9:16 / 1:1; default "16:9" | Aspect ratio. Ignored when start_image is provided. |
| `duration` | integer | optional | 3 to 15; default 5 | Video duration in seconds. |
| `generate_audio` | boolean | optional | default false | Generate native audio for the video. |
| `multi_prompt` | string | optional | See description | JSON array of shot definitions for multi-shot mode. Each shot: {"prompt": "...", "duration": N}. Max 6 shots, min 1s per shot, total must equal duration. |

## Example tool arguments

```json
{
  "input": {
    "prompt": "A short cinematic sequence about a copper automaton discovering the night sky.",
    "duration": 10,
    "mode": "pro",
    "aspect_ratio": "16:9",
    "generate_audio": true,
    "multi_prompt": "[{\"prompt\": \"Wide shot: a copper automaton with glass eyes and a weathered blue coat enters an ivy-covered observatory. Moonlight crosses the floor; camera tracks beside it.\", \"duration\": 4}, {\"prompt\": \"Medium close-up: the same copper automaton in the same blue coat looks through the brass telescope, then lifts its head in wonder. A slow push-in; soft mechanical clicks and night wind.\", \"duration\": 6}]"
  },
  "request_key": "observatory_kling_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- Generation duration 3-15s; up to 6 shots, minimum 1s each, exact sum equals duration.
- mode standard=720p, pro=1080p, 4k=4K. There is no resolution field.
- Start/end frames must be JPEG/PNG <=10MB and each dimension >=300px; first-frame ratio 0.4-2.5. End requires start.
- A start image determines framing, so the aspect_ratio control is ignored.
- Prompt and negative_prompt each have a 2500-character limit.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/kwaivgi--kling-v3-video.md) and [schema](../references/research/raw/kwaivgi--kling-v3-video--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
