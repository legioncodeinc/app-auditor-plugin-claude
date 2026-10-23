URL: https://replicate.com/bytedance/seedance-2.0/llms.txt
Fetched: 2026-10-11T00:24:07.161068+00:00
Source type: official model card and schema

## Basic model info

Model name: bytedance/seedance-2.0
Model description: ByteDance's multimodal video generation model with native audio, multimodal reference inputs, and intelligent duration control.


## Model inputs

- prompt (required): Text prompt for video generation. Maximum 4000 characters. BytePlus recommends keeping prompts under 600 English words for best results. (string)
- image (optional): Input image for image-to-video generation (first frame). Cannot be combined with reference images. (string)
- last_frame_image (optional): Input image for last frame generation. Only works if a first frame image is also provided. Cannot be combined with reference images. (string)
- reference_images (optional): Reference images (up to 9) for character consistency, style guidance, and scene composition. Cannot be used together with first/last frame images. You can reference them in your prompt as [Image1], [Image2], etc. (array)
- reference_videos (optional): Reference videos (up to 3, total duration max 15s) for motion transfer, style reference, and editing. Reference them in your prompt as [Video1], [Video2], etc. (array)
- reference_audios (optional): Reference audio files (up to 3, total duration max 15s) for audio-driven generation and lip-sync. Requires at least one reference image or video. Reference them in your prompt as [Audio1], [Audio2], etc. (array)
- duration (optional): Video duration in seconds. Set to -1 for intelligent duration (model picks the best length). (integer)
- resolution (optional): Video resolution. 4K outputs 10-bit H.265/HEVC at high bitrate. (string)
- aspect_ratio (optional): Video aspect ratio. Set to 'adaptive' to let the model choose the best ratio based on inputs. (string)
- generate_audio (optional): Generate synchronized audio with the video, including dialogue (use double quotes in prompt), sound effects, and background music. (boolean)
- seed (optional): Random seed. Set for reproducible generation. (integer)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/cvmsf12b4drmr0cxdt08pxwybm)

#### Input

```json
{
  "seed": 99,
  "prompt": "A cozy cabin in a snowy forest at night, warm light glowing from the windows, gentle snowfall, camera slowly pushing in through the trees",
  "duration": 7,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/3Uc0eKT36R2dIiXkrse8tD822Mhne8AIAMV6ekMcDg8WnWkZB/tmp7_ephsht.mp4"
```


### Example (https://replicate.com/p/wckk6zjh01rmt0cxdt09fmsdzw)

#### Input

```json
{
  "seed": 42,
  "prompt": "A golden retriever puppy chasing butterflies through a sunlit meadow, soft bokeh background, cinematic camera slowly tracking the puppy",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/v41RJfGpFcQfRUBcwvlrcNjOUgFbwKE4YufY9MENWp2ZTLysA/tmps8w9y8mz.mp4"
```


### Example (https://replicate.com/p/8p1drjtj7nrmr0cxdt09t9mwmg)

#### Input

```json
{
  "seed": 123,
  "prompt": "A sushi chef carefully preparing an intricate sushi roll, close-up overhead shot, steam rising, warm restaurant lighting",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/bOn5X2Xyi9bfVi4ePS9OIdjEJIf5jwWKKp1Uei92WskaqWkZB/tmpmfghm4s5.mp4"
```


### Example (https://replicate.com/p/dsjpg4qhe1rmw0cxdt1bvr8scc)

#### Input

```json
{
  "seed": 77,
  "prompt": "A hot air balloon festival at sunrise, dozens of colorful balloons rising above misty green hills, camera tilts up slowly revealing the vast landscape",
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/gHdWD6Zs19YuLRRq2zl7Gd8l1FeD9JQUCcpX0CYMsHuS2iMLA/tmpasb8z2lb.mp4"
```


### Example (https://replicate.com/p/9szh2b2r8nrmr0cxdt0abdcbm8)

#### Input

```json
{
  "seed": 256,
  "prompt": "A woman in a flowing red dress walking along the edge of a cliff overlooking the sea, wind blowing her hair and dress, dramatic wide angle, golden sunset",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "9:16",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/qZ5dzPJqNJIMEZz2HosafMBze0CrC8oJSEsZAzIHHhi8pFZWA/tmpx4k1adge.mp4"
```


## Model readme

> # Seedance 2.0
> 
> Generate high-quality video from text, images, video clips, and audio — all in one pass with synchronized sound. Seedance 2.0 is ByteDance's next-generation video model, built on a unified multimodal architecture that accepts mixed inputs and produces coherent, audio-synced output.
> 
> ## What's new in 2.0
> 
> Seedance 2.0 is a significant upgrade from 1.5 Pro:
> 
> - **Multimodal reference inputs** — combine up to 9 images, 3 video clips, and 3 audio files in a single generation. Reference them in your prompt as [Image1], [Video1], [Audio1], etc.
> - **Better motion and physics** — more realistic rendering of complex interactions like sports, dancing, and object collisions.
> - **Video editing and extension** — modify existing videos or extend them by providing a reference video and describing what should happen next.
> - **Intelligent duration** — set duration to -1 and let the model pick the best length for the content.
> - **Adaptive aspect ratio** — set aspect ratio to "adaptive" and the model will choose the best fit based on your inputs.
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
> ## Supported resolutions
> 
> | Resolution | 16:9 | 4:3 | 1:1 | 3:4 | 9:16 | 21:9 |
> |---|---|---|---|---|---|---|
> | 480p | 864×496 | 752×560 | 640×640 | 560×752 | 496×864 | 992×432 |
> | 720p | 1280×720 | 1112×834 | 960×960 | 834×1112 | 720×1280 | 1470×630 |
> 
> ## Learn more
> 
> For technical details and architecture, see the [official Seedance 2.0 page](https://seed.bytedance.com/en/seedance2_0).
> 
> You can try this model on the [Replicate Playground](https://replicate.com/playground).

