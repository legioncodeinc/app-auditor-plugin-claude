# alibaba/wan-3: character and scene guide

Tool: `replicate_wan_3`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/alibaba/wan-3), [archived card](../references/research/raw/alibaba--wan-3.md), [exact schema](../references/research/raw/alibaba--wan-3--schema.json).

## Choose the shot

Choose this for a continuous character action or a longer environmental reveal. Use image-to-video when the opening composition and character design matter. The endpoint has no native audio control; plan sound separately if needed.

## Direct the scene

With a starting frame, describe what changes: action, camera, environment motion. With text only, establish the character, setting, lighting, and starting pose before the action. Keep each action causally ordered. Use negative_prompt only for specific defects you actually see, and consider disabling prompt expansion when an exact production brief is already written.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | See description | Text prompt for video generation |
| `image` | string | optional | See description | Optional first-frame image to animate into a video (jpg/png/bmp/webp, ≤10MB). When provided, the video is generated from this image guided by the prompt. |
| `negative_prompt` | string | optional | default "" | Negative prompt ; describes content that should not appear in the video |
| `resolution` | string | optional | 480p / 720p / 1080p; default "1080p" | Output video resolution |
| `aspect_ratio` | string | optional | adaptive / 16:9 / 9:16 / 1:1 / 4:3 / 3:4; default "adaptive" | Aspect ratio of the generated video. 'adaptive' lets the model choose the best ratio for the prompt. Ignored when an image is provided (the input image's aspect ratio is used). |
| `duration` | integer | optional | 2 to 30; default 5 | Duration of the generated video in seconds |
| `enable_prompt_expansion` | boolean | optional | default true | Automatically expand and optimize the prompt for better results. Improves quality for short prompts but increases latency. |
| `seed` | integer | optional | See description | Random seed for reproducible generation. Range: 0-2147483647 |

## Example tool arguments

```json
{
  "input": {
    "prompt": "A small copper automaton in a weathered blue coat stands at the entrance to an overgrown observatory. It raises one hand and slowly opens its brass fingers, releasing a glowing firefly. The camera tracks forward from a medium shot to a close-up. Moonlight catches scratched copper while distant vines stir gently. One continuous shot.",
    "duration": 8,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "enable_prompt_expansion": false
  },
  "request_key": "observatory_wan_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- A supplied image determines framing, so do not rely on aspect_ratio to crop it.
- First-frame images must be <=10MB; the uploader additionally verifies the content.
- There is no reference-video or last-frame field on this endpoint.
- Seed repeatability is a control, not a promise of identical characters across unrelated shots.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/alibaba--wan-3.md) and [schema](../references/research/raw/alibaba--wan-3--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
