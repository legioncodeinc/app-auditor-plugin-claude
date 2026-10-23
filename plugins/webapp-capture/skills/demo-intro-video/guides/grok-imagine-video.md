# xai/grok-imagine-video: character and scene guide

Tool: `replicate_grok_imagine_video`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/xai/grok-imagine-video), [archived card](../references/research/raw/xai--grok-imagine-video.md), [exact schema](../references/research/raw/xai--grok-imagine-video--schema.json).

## Choose the shot

Choose this for character animation from a still, a text scene with native sound, or a specific change to an existing short clip. The editing source must be <=8.7 seconds.

## Direct the scene

For image animation, give motion direction, a camera move, and an emotional beat. For text-only scenes, use subject + action + setting + camera + lighting. For edits, state the change and the composition/motion to preserve. Audio can be described in the prompt, but the endpoint has no toggle. Phrase direction positively; there is no negative_prompt field.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | See description | Text prompt for video generation |
| `image` | string | optional | See description | Input image to generate video from (image-to-video). Supports jpg, jpeg, png, webp. |
| `video` | string | optional | See description | Input video to edit (video editing mode). Must be a direct link, max 8.7 seconds. Supports mp4, mov, webm. |
| `duration` | integer | optional | 1 to 15; default 5 | Duration of the video in seconds (1-15). Ignored when editing a video. |
| `aspect_ratio` | string | optional | auto / 16:9 / 4:3 / 1:1 / 9:16 / 3:4 / 3:2 / 2:3; default "auto" | Aspect ratio of the video. For text-to-video, defaults to 16:9. For image-to-video, defaults to the input image's native aspect ratio. Ignored when editing a video. |
| `resolution` | string | optional | 720p / 480p; default "720p" | Resolution of the video. Ignored when editing a video. |

## Example tool arguments

```json
{
  "input": {
    "prompt": "Replace the clockwork bird in the clip with a small copper dragon. Keep the clockmaker, his burgundy waistcoat, hand motion, warm lamplight, and the original camera movement. The dragon opens its wings gently and chirps once.",
    "video": {
      "file_id": "video_scene_01"
    }
  },
  "request_key": "clockmaker_grok_edit01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- The example file ID is a placeholder; upload the source clip first.
- For editing, omit duration/aspect_ratio/resolution because the provider ignores them and preserves the input dimensions and duration.
- Choose image animation or video editing separately.
- New generation: 1-15 seconds, 480p/720p. Native sound has no generate_audio parameter.
- The README mentions Normal/Fun/Custom modes but the current schema provides no mode field. Do not invent one.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/xai--grok-imagine-video.md) and [schema](../references/research/raw/xai--grok-imagine-video--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
