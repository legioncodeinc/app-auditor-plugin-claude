URL: https://replicate.com/bytedance/seedance-2.5/llms.txt
Fetched: 2026-10-11T00:24:07.150102+00:00
Source type: official model card and schema

## Basic model info

Model name: bytedance/seedance-2.5
Model description: ByteDance's flagship multimodal video model with native audio, native 30-second generation, and large multimodal reference sets.


## Model inputs

- prompt (optional): Text prompt for video generation. Optional when a media input (image, reference images/videos/audios) is supplied. Seedance 2.5 works best with detailed, structured 'production brief' style prompts. (string)
- image (optional): First-frame image for image-to-video or first/last-frame generation. Cannot be combined with reference images, videos, or audios. (string)
- last_frame_image (optional): Last-frame image. Requires a first-frame image. Cannot be combined with reference images, videos, or audios. (string)
- reference_images (optional): Reference images (up to 30) for character consistency, style guidance, and scene composition. Cannot be combined with first/last frame images. Reference them in your prompt as [Image1], [Image2], etc. (array)
- reference_videos (optional): Reference videos (up to 10, combined duration max 30s) for motion transfer, style reference, editing, and extension. Reference them in your prompt as [Video1], [Video2], etc. (array)
- reference_audios (optional): Reference audio files (up to 10, combined duration max 30s) for audio-driven generation and lip-sync. Requires at least one reference image or video. Reference them in your prompt as [Audio1], [Audio2], etc. (array)
- duration (optional): Video duration in seconds. Set to -1 for intelligent duration (the model picks the best length). Editing mode requires -1. (integer)
- resolution (optional): Video resolution. (string)
- aspect_ratio (optional): Video aspect ratio. Set to 'adaptive' to let the model choose the best ratio based on inputs. First/last-frame, editing, and extension modes require 'adaptive'. (string)
- generate_audio (optional): Generate synchronized audio with the video, including dialogue (use double quotes in prompt), sound effects, and background music. (boolean)
- watermark (optional): Add a watermark to the generated video. (boolean)
- output_format (optional): Output video container format. (string)
- seed (optional): Random seed. Set for reproducible generation. Reproducibility is not guaranteed. (integer)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/5zy1qx4ysnrmw0czvht82q4sc4)

#### Input

```json
{
  "seed": 42,
  "prompt": "a golden retriever puppy running across a green meadow toward the camera, slow motion, warm afternoon light",
  "duration": 5,
  "resolution": "720p"
}
```

#### Output

```json
"https://replicate.delivery/xezq/3wyRfILDMs00CCsuqQk8A3xukwFvHjBH7bejjdBFU0eVayBuA/tmpxo_kp6e0.mp4"
```


## Model readme

> # Seedance 2.5
> 
> Generate high-quality video from text, images, video clips, and audio — all in one pass with synchronized sound. Seedance 2.5 is ByteDance's flagship video model, built on a unified multimodal architecture that accepts mixed inputs and produces coherent, audio-synced output up to 30 seconds long in a single generation.
> 
> ## What's new in 2.5
> 
> Seedance 2.5 builds on 2.0 with a focus on production work:
> 
> - **Native 30-second generation** — create a full 30-second clip in one pass, no stitching required. Set duration anywhere from 4 to 30 seconds, or use -1 for intelligent duration.
> - **Larger reference sets** — combine up to 30 images, 10 video clips, and 10 audio files in a single generation. Reference them in your prompt as [Image1], [Video1], [Audio1], etc.
> - **Stronger instruction following** — better handling of complex, multi-subject shots and reference-heavy creative direction.
> - **Multilingual prompts** — write prompts in a range of languages.
> - **Adaptive aspect ratio** — set aspect ratio to "adaptive" and the model chooses the best fit based on your inputs.
> 
> ## What you can create
> 
> **Text to video**
> 
> Describe a scene in natural language and get a video with matching audio. The model understands multi-subject interactions, camera movements, and emotional tone. For dialogue, put speech in double quotes in your prompt — the model generates matching lip movements and voice.
> 
> **Image to video**
> 
> Animate a still image by providing it as the first frame. You can also specify a last frame image to control where the video ends up. The model preserves the look and style of your input image while adding natural motion.
> 
> **Multimodal reference**
> 
> Combine images, videos, and audio as references. For example, provide a reference video for motion style, reference images for character appearance, and reference audio for rhythm — then describe how to combine them. This is powerful for outfit-change videos, product showcases, and music-synced content.
> 
> **Video editing**
> 
> Provide a reference video and describe changes — replace an object, change a background, or alter the style. The model preserves the original motion and camera work while making your edits.
> 
> **Video extension**
> 
> Provide a reference video and describe what should happen next. The model continues the scene with consistent characters, environment, and style.
> 
> ## Key features
> 
> **Native audio generation**
> 
> Audio and video are generated together, not separately. This means dialogue, sound effects, and background music are all synchronized with the visuals from the start. You can turn audio off if you just want silent video.
> 
> **Character consistency**
> 
> When using reference images, the model maintains facial features, clothing, and style across the generated video. This makes it possible to create multi-shot narratives with consistent characters.
> 
> **Precise prompt following**
> 
> The model handles complex prompts with multiple subjects, specific actions, and detailed camera movements. It understands spatial relationships and sequential actions.
> 
> ## Tips for good results
> 
> - Be specific in your prompts — describe camera movements, lighting, mood, and specific actions.
> - For dialogue, put the spoken words in double quotes: `The man stopped and said: "Remember this moment."`
> - When using reference inputs, label them in your prompt: "The character from [Image1] performs the dance from [Video1]."
> - For video editing, describe what to change and what to keep: "Replace the perfume in [Video1] with the face cream from [Image1], keeping all original motion."
> - Start with shorter durations (5 seconds) while experimenting, then increase once you're happy with the style.
> 
> ## Learn more
> 
> For technical details and architecture, see the [official Seedance page](https://seed.bytedance.com/en/seedance2_0).
> 
> You can try this model on the [Replicate Playground](https://replicate.com/playground).

