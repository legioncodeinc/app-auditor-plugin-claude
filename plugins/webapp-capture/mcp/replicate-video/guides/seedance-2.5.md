# bytedance/seedance-2.5: character and scene guide

Tool: `replicate_seedance_2_5`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/bytedance/seedance-2.5), [archived card](../references/research/raw/bytedance--seedance-2.5.md), [exact schema](../references/research/raw/bytedance--seedance-2.5--schema.json).

## Choose the shot

Choose this for a longer character scene, a larger visual cast, or a structured production brief with several media roles. This endpoint supports 30 images, 10 videos, and 10 audios.

## Direct the scene

Use a production brief: CAST, SCENE, ACTION TIMELINE, CAMERA, LIGHTING, AUDIO, and CONTINUITY. Bind every supplied reference by its indexed token, then describe interactions and causality. For editing, say what changes and which motion/composition should remain. For extension, say where the existing action ends and what follows. Set workflow explicitly for edit or extend so the wrapper can validate mode-specific requirements.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | optional | default "" | Text prompt for video generation. Optional when a media input (image, reference images/videos/audios) is supplied. Seedance 2.5 works best with detailed, structured 'production brief' style prompts. |
| `image` | string | optional | See description | First-frame image for image-to-video or first/last-frame generation. Cannot be combined with reference images, videos, or audios. |
| `last_frame_image` | string | optional | See description | Last-frame image. Requires a first-frame image. Cannot be combined with reference images, videos, or audios. |
| `reference_images` | array | optional | default [] | Reference images (up to 30) for character consistency, style guidance, and scene composition. Cannot be combined with first/last frame images. Reference them in your prompt as [Image1], [Image2], etc. |
| `reference_videos` | array | optional | default [] | Reference videos (up to 10, combined duration max 30s) for motion transfer, style reference, editing, and extension. Reference them in your prompt as [Video1], [Video2], etc. |
| `reference_audios` | array | optional | default [] | Reference audio files (up to 10, combined duration max 30s) for audio-driven generation and lip-sync. Requires at least one reference image or video. Reference them in your prompt as [Audio1], [Audio2], etc. |
| `duration` | integer | optional | -1 to 30; default 5 | Video duration in seconds. Set to -1 for intelligent duration (the model picks the best length). Editing mode requires -1. |
| `resolution` | string | optional | 480p / 720p; default "720p" | Video resolution. |
| `aspect_ratio` | string | optional | 16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9 / adaptive; default "16:9" | Video aspect ratio. Set to 'adaptive' to let the model choose the best ratio based on inputs. First/last-frame, editing, and extension modes require 'adaptive'. |
| `generate_audio` | boolean | optional | default true | Generate synchronized audio with the video, including dialogue (use double quotes in prompt), sound effects, and background music. |
| `watermark` | boolean | optional | default false | Add a watermark to the generated video. |
| `output_format` | string | optional | mp4 / mov; default "mp4" | Output video container format. |
| `seed` | integer | optional | See description | Random seed. Set for reproducible generation. Reproducibility is not guaranteed. |

## Example tool arguments

```json
{
  "input": {
    "prompt": "CAST: [Image1] is the copper automaton; preserve its glass eyes and blue coat. SCENE: the ivy-covered observatory from [Image2], moonlight through the dome. ACTION: 0-5s it enters and pauses; 5-10s it opens the telescope cover; 10-15s it leans toward the eyepiece and smiles. CAMERA: begin wide, track beside it, then settle into a medium profile. AUDIO: footsteps, a quiet hinge creak, soft night wind. CONTINUITY: the telescope stays fixed beside the same window throughout.",
    "reference_images": [
      {
        "file_id": "image_character_01"
      },
      {
        "file_id": "image_scene_01"
      }
    ],
    "duration": 15,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "generate_audio": true,
    "output_format": "mp4"
  },
  "workflow": "generate",
  "request_key": "observatory_seedance25_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- The example file IDs are placeholders; replace them with actual upload IDs.
- Duration is 4-30s or -1. The endpoint only exposes 480p/720p, even though 2.0 exposes higher resolution enums.
- Frames cannot mix with any reference collection; last_frame_image requires image.
- Frames, edit and extend require aspect_ratio=adaptive. Editing additionally needs duration=-1 and reference_videos.
- Video totals <=30s and audio totals separately <=30s. Audio references need image/video references.
- Prompt can be omitted when usable visual media is supplied, but a production brief gives clearer intent. Seed reproducibility is explicitly not guaranteed.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/bytedance--seedance-2.5.md) and [schema](../references/research/raw/bytedance--seedance-2.5--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
