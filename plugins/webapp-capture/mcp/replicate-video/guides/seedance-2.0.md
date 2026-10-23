# bytedance/seedance-2.0: character and scene guide

Tool: `replicate_seedance_2_0`. Source snapshot: 2026-10-10 America/New_York. [Model card](https://replicate.com/bytedance/seedance-2.0), [archived card](../references/research/raw/bytedance--seedance-2.0.md), [exact schema](../references/research/raw/bytedance--seedance-2.0--schema.json).

## Choose the shot

Choose this for a character performance guided by image identity, video choreography, or audio rhythm. This is the smaller reference-set endpoint: 9 images, 3 videos, and 3 audios.

## Direct the scene

Assign references before writing the prompt. [Image1] can define the character, [Image2] the setting, [Video1] the movement, and [Audio1] the rhythm or voice. State each role explicitly and distinguish appearance from motion. Use a compact shot timeline and quote short dialogue. Reuse the same character reference and visual description across shots; assess continuity in the outputs.

These are creative recommendations, not measured guarantees. Start with one clear acting beat. Assign character identity, wardrobe, setting, camera, and sound consistently across the shot list. Check anatomy, props, eyelines, dialogue and continuity after generation before accepting a take.

## Exact published fields

This table is generated from the archived official input schema, not inferred from marketing copy. File-valued fields use this server's `{"path":"/allowed/reference.png"}` or `{"file_id":"actual_upload_id"}` wrapper instead of a raw provider URL. Arrays contain those wrappers. The shared uploader converts them to provider URLs. Controls not listed here are rejected.

| Field | Provider type | Required | Defaults and bounds | Provider description |
|---|---|---|---|---|
| `prompt` | string | required | max 4000 characters | Text prompt for video generation. Maximum 4000 characters. BytePlus recommends keeping prompts under 600 English words for best results. |
| `image` | string | optional | See description | Input image for image-to-video generation (first frame). Cannot be combined with reference images. |
| `last_frame_image` | string | optional | See description | Input image for last frame generation. Only works if a first frame image is also provided. Cannot be combined with reference images. |
| `reference_images` | array | optional | default [] | Reference images (up to 9) for character consistency, style guidance, and scene composition. Cannot be used together with first/last frame images. You can reference them in your prompt as [Image1], [Image2], etc. |
| `reference_videos` | array | optional | default [] | Reference videos (up to 3, total duration max 15s) for motion transfer, style reference, and editing. Reference them in your prompt as [Video1], [Video2], etc. |
| `reference_audios` | array | optional | default [] | Reference audio files (up to 3, total duration max 15s) for audio-driven generation and lip-sync. Requires at least one reference image or video. Reference them in your prompt as [Audio1], [Audio2], etc. |
| `duration` | integer | optional | -1 to 15; default 5 | Video duration in seconds. Set to -1 for intelligent duration (model picks the best length). |
| `resolution` | string | optional | 480p / 720p / 1080p / 4k; default "720p" | Video resolution. 4K outputs 10-bit H.265/HEVC at high bitrate. |
| `aspect_ratio` | string | optional | 16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9 / 9:21 / adaptive; default "16:9" | Video aspect ratio. Set to 'adaptive' to let the model choose the best ratio based on inputs. |
| `generate_audio` | boolean | optional | default true | Generate synchronized audio with the video, including dialogue (use double quotes in prompt), sound effects, and background music. |
| `seed` | integer | optional | See description | Random seed. Set for reproducible generation. |

## Example tool arguments

```json
{
  "input": {
    "prompt": "The copper automaton from [Image1] performs the deliberate three-step turn from [Video1] in the moonlit observatory shown in [Image2]. Preserve its round glass eyes, narrow brass fingers, and weathered blue coat. Begin in a full-body shot; as it stops, slowly push toward its face. Its coat settles after the turn. Soft mechanical clicks and distant night wind.",
    "reference_images": [
      {
        "file_id": "image_character_01"
      },
      {
        "file_id": "image_scene_01"
      }
    ],
    "reference_videos": [
      {
        "file_id": "video_motion_01"
      }
    ],
    "duration": 8,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "generate_audio": true
  },
  "request_key": "automaton_seedance20_take01"
}
```

Before using media examples, run `replicate_upload_file` for each real reference, then replace placeholder IDs. Alternatively use a local `path` wrapper and this tool calls the same upload endpoint automatically. Read-only `replicate_model_schema` can inspect the full wrapper contract. The upload root defaults to the server's working folder; each media file must be below 100MB and combined references below 250MB per generation.

A call creates a paid asynchronous prediction. Reuse the same request_key and identical arguments after an uncertain response. Poll the returned prediction_id at the suggested interval; do not call the generation tool to check progress. Native video quality and dialogue timing must be judged from the resulting media.

## Avoid these mistakes

- The example file IDs are placeholders; replace them with values returned by replicate_upload_file.
- Prompt maximum is 4000 characters; the card recommends staying under 600 English words.
- Video-reference duration totals <=15s; audio-reference totals separately <=15s.
- Audio references require image or video references. First/last frames conflict with reference_images.
- The schema allows resolution 480p/720p/1080p/4k; the README only tabulates the smaller two. The schema governs this wrapper.
- The coarse schema bounds duration from -1 to 15. It does not clearly explain every small duration; use an ordinary 5-15s clip or -1.

## Evidence and limitations

The capabilities, field names, enums and documented constraints above derive from the [archived model card](../references/research/raw/bytedance--seedance-2.0.md) and [schema](../references/research/raw/bytedance--seedance-2.0--schema.json). Cross-source conflicts and wrapper restrictions are recorded in the [research distillation](../references/research/distilled-replicate-video.md). This build tested contracts and local behavior with mocked Replicate responses; it did not run a paid quality benchmark.
