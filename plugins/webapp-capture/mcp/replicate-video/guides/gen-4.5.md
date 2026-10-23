# runwayml/gen-4.5: character and scene guide

Tool: `replicate_runway_gen_4_5`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/runwayml/gen-4.5), [archived card](../references/research/raw/runwayml--gen-4.5.md), [exact schema](../references/research/raw/runwayml--gen-4.5--schema.json).

## Choose the shot

Choose this for expressive acting, clear physical motion, and a specific camera move. A first-frame image can anchor an illustrated or realistic character. Use a short acting beat before attempting a complex sequence.

## Direct the scene

Write natural visual sentences: shot size, identifiable subject, one main action, camera movement, then light and atmosphere. For image animation, emphasize motion rather than restating every visual detail. Describe anticipation, contact, and follow-through when a physical event matters. The current schema supports image even though the older README lists image-to-video as coming later.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | See description | Text prompt for video generation |
| `image` | string | optional | See description | Optional initial image for video generation (first frame). If not provided, video will be generated from text only. |
| `aspect_ratio` | string | optional | 16:9 / 9:16 / 4:3 / 3:4 / 1:1 / 21:9; default "16:9" | Video aspect ratio |
| `duration` | integer | optional | 5 / 10; default 5 | Duration of the output video in seconds |
| `seed` | integer | optional | See description | Random seed. Set for reproducible generation |

## Example tool arguments

```json
{
  "input": {
    "prompt": "A medium shot of a tired clockmaker in a burgundy waistcoat seated at a wooden workbench. He lifts a tiny mechanical bird, watches its wings open, and smiles with quiet relief. His hands move carefully and the bird remains between his fingers. A slow dolly in, warm lamplight, soft shadows, cinematic realism.",
    "duration": 5,
    "aspect_ratio": "16:9"
  },
  "request_key": "clockmaker_runway_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- Duration must be exactly 5 or 10 seconds.
- There is no resolution, negative_prompt, audio switch, ending frame, or reference-video field.
- Do not turn vendor benchmark language into a current independently tested ranking.
- Check the final clip for disappearing props, continuity errors, and effects preceding causes.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/runwayml--gen-4.5.md) and [schema](../references/research/raw/runwayml--gen-4.5--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
