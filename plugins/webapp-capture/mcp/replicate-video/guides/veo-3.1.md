# google/veo-3.1: character and scene guide

Tool: `replicate_veo_3_1`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/google/veo-3.1), [archived card](../references/research/raw/google--veo-3.1.md), [exact schema](../references/research/raw/google--veo-3.1--schema.json).

## Choose the shot

Choose this for dialogue, ambient sound, and a scene that needs consistent subject references. Use the first/last frame path for a visual transition; use reference_images for subject appearance.

## Direct the scene

Identify each speaker, keep dialogue short enough to finish in the selected duration, and put exact spoken words in quotes. Describe the performance, camera, and sound separately. For subject references, assign one clear identity or visual role to each file and describe where that subject appears. Keep frames and reference collections in separate calls.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | See description | Text prompt for video generation |
| `aspect_ratio` | string | optional | 16:9 / 9:16; default "16:9" | Video aspect ratio |
| `duration` | integer | optional | 4 / 6 / 8; default 8 | Video duration in seconds |
| `image` | string | optional | See description | Input image to start generating from. Ideal images are 16:9 or 9:16 and 1280x720 or 720x1280, depending on the aspect ratio you choose. |
| `last_frame` | string | optional | See description | Ending image for interpolation. When provided with an input image, creates a transition between the two images. |
| `reference_images` | array | optional | default [] | 1 to 3 reference images for subject-consistent generation (reference-to-video, or R2V). Reference images only work with 16:9 aspect ratio and 8-second duration. Last frame is ignored if reference images are provided. |
| `negative_prompt` | string | optional | See description | Description of what to exclude from the generated video |
| `resolution` | string | optional | 720p / 1080p; default "1080p" | Resolution of the generated video |
| `generate_audio` | boolean | optional | default true | Generate audio with the video |
| `seed` | integer | optional | See description | Random seed. Omit for random generations |

## Example tool arguments

```json
{
  "input": {
    "prompt": "Medium close-up of an adult lighthouse keeper in a dark wool coat on the lantern-room balcony at dusk. She turns toward the camera, looks relieved, and softly says, \"The light is still with us.\" A slow push-in. Wind moves a few strands of hair. AUDIO: gentle coastal wind, distant surf, her clear voice; no background score.",
    "duration": 8,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "generate_audio": true
  },
  "request_key": "lighthouse_veo_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- reference_images accepts 1-3 images; nonempty references require 16:9 and duration=8.
- last_frame requires image. The wrapper rejects reference_images mixed with image or last_frame because direction can be ignored.
- Generation durations are 4, 6, or 8 seconds.
- Judge lip timing and the exact spoken words in the output; prompt adherence is not guaranteed.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/google--veo-3.1.md) and [schema](../references/research/raw/google--veo-3.1--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
