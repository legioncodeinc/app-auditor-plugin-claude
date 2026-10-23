URL: https://replicate.com/kwaivgi/kling-v3-video/llms.txt
Fetched: 2026-10-11T00:24:07.174312+00:00
Source type: official model card and schema

## Basic model info

Model name: kwaivgi/kling-v3-video
Model description: Kling Video 3.0: Generate cinematic videos up to 15 seconds with multi-shot control, native audio, and improved consistency


## Model inputs

- prompt (required): Text prompt for video generation. Max 2500 characters. (string)
- negative_prompt (optional): Things you do not want to see in the video. Max 2500 characters. (string)
- start_image (optional): First frame image. Supports .jpg/.jpeg/.png, max 10MB, min 300px, aspect ratio 1:2.5 to 2.5:1. (string)
- end_image (optional): Last frame image. Requires start_image. Supports .jpg/.jpeg/.png, max 10MB, min 300px. (string)
- mode (optional): 'standard' generates 720p, 'pro' generates 1080p, '4k' generates 4K. (string)
- aspect_ratio (optional): Aspect ratio. Ignored when start_image is provided. (string)
- duration (optional): Video duration in seconds. (integer)
- generate_audio (optional): Generate native audio for the video. (boolean)
- multi_prompt (optional): JSON array of shot definitions for multi-shot mode. Each shot: {"prompt": "...", "duration": N}. Max 6 shots, min 1s per shot, total must equal duration. (string)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/ty6ca28mv1rmr0cwd0hswwavdc)

#### Input

```json
{
  "mode": "pro",
  "prompt": "First-person POV of a roller coaster plunging into the mouth of an erupting volcano. The track spirals down through rivers of glowing orange lava, sparks and embers flying past the camera. The coaster banks hard around a pillar of molten rock, then launches upward through a vent, bursting out of the volcano's crater into a dazzling sunset sky above the clouds. Wind roaring, riders screaming with excitement, the deep rumble of the volcano.",
  "duration": 15,
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/0SqqHf1j2PTdXyYCEQto2dw18YM5mUe1Xpsn7fGHLLcOOmQsA/tmplcozmpnh.mp4"
```


### Example (https://replicate.com/p/4rnefer92srmr0cwd0htbqqn84)

#### Input

```json
{
  "mode": "pro",
  "prompt": "A massive alien spaceship, miles long and covered in glowing blue circuits, slowly rises from the East River in Manhattan. Water cascades off its hull as it ascends past the Brooklyn Bridge. Helicopters scatter, car alarms blare across the city. The camera captures this from a rooftop in DUMBO, showing the ship dwarfing the entire skyline as golden sunset light reflects off its surface. Thunderous rumbling, water crashing, distant sirens.",
  "duration": 15,
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/eKYlrlYgUWURc6wHCGke17ZUdExpb4mWIMak4exeG9d6aMhYB/tmpbdhdcmtk.mp4"
```


### Example (https://replicate.com/p/x7hmch1vk5rmy0cwd0htx2bkjc)

#### Input

```json
{
  "mode": "pro",
  "prompt": "A multi-shot short film.",
  "duration": 15,
  "aspect_ratio": "16:9",
  "multi_prompt": "[{\"prompt\": \"An astronaut floats alone in deep space, Earth glowing blue behind them, camera slowly rotating around their helmet reflecting the stars\", \"duration\": 5}, {\"prompt\": \"The astronaut turns to see a massive golden nebula forming into the shape of a human hand reaching toward them, light particles swirling\", \"duration\": 5}, {\"prompt\": \"The astronaut reaches out and touches the nebula hand, which explodes into a billion stars that rush past the camera in every direction\", \"duration\": 5}]",
  "generate_audio": false
}
```

#### Output

```json
"https://replicate.delivery/xezq/jfGxCg26tmQqeExw5E79MG9ukbmwjUUSovmHCPPFCfhdQmQsA/tmp2henp9i6.mp4"
```


### Example (https://replicate.com/p/zg1j4vxb8hrmy0cwd0q8atbs7m)

#### Input

```json
{
  "mode": "pro",
  "prompt": "Bamse, the world's strongest bear, a cartoon brown bear wearing blue overalls and a blue knit cap, lifts an enormous boulder over his head and hurls it across a sunny Swedish meadow. Wildflowers scatter in the wind. His friends, a small rabbit and a turtle with a shell full of gadgets, cheer from behind a wooden fence. Bright, colorful 2D animation style with thick outlines. Cheerful music, a triumphant fanfare, birds chirping.",
  "duration": 10,
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/hve9nDn2celJm0S1pVZfF7t2AmUCRmJ87SkCANVOs1YqeMhYB/tmpyyrnjeop.mp4"
```


### Example (https://replicate.com/p/13fgyzchc1rmr0cwd0q90kmqhr)

#### Input

```json
{
  "mode": "pro",
  "prompt": "Cinematic drone footage of a dragon made of living fire soaring over a frozen Nordic fjord at twilight. Its wings trail streams of flame that melt the ice below, creating swirling clouds of steam. The dragon banks sharply and breathes a column of fire across the mountainside, igniting the snow in brilliant orange and gold. Northern lights shimmer green and purple in the sky above. Thunderous wingbeats, crackling fire, hissing steam, a deep otherworldly growl.",
  "duration": 15,
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/WKfrPS0sWO2epkf9tyRyIMQEg8ChzQgwCS3dEO9r06j8kmQsA/tmpjbp9fboz.mp4"
```


### Example (https://replicate.com/p/tnbmcr3p7srmr0cwd0pahppvkr)

#### Input

```json
{
  "mode": "pro",
  "prompt": "The construction workers come to life. One man passes a sandwich to his neighbor, another lights a cigarette. They chat and laugh casually, legs swinging over the edge of the beam. Wind blows their hair and clothes. Camera slowly zooms out to reveal the dizzying height, the streets of 1930s New York City far below, tiny cars and pedestrians visible. The sound of wind at altitude, distant city noise, men talking and laughing.",
  "duration": 10,
  "start_image": "https://petapixel.com/assets/uploads/2012/09/skyscraper1.jpg",
  "generate_audio": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/iONMaxvzQb5IJ1N9QnwqqIBArvfjgkElvqNr6z1toAYmsJELA/tmp1coxpu41.mp4"
```


## Model readme

> # Kling Video 3.0
> 
> Generate cinematic videos up to 15 seconds long from text prompts or images. Kling Video 3.0 improves on previous versions with longer output, stronger consistency across shots, and native audio generation including lip-synced dialogue.
> 
> ## What it does
> 
> Kling Video 3.0 turns text descriptions or still images into video clips at up to 1080p resolution. The model generates videos between 3 and 15 seconds—a significant jump from the 10-second limit of earlier versions. It handles realistic scenes, stylized content, and complex multi-step actions within a single generation.
> 
> You can also generate native audio alongside the video, including dialogue with lip sync, sound effects, and ambient sound—all in one pass.
> 
> ## How to use it
> 
> The model supports two main input modes:
> 
> **Text to video**: Describe what you want to see. The model generates visuals (and optionally audio) from your description.
> 
> **Image to video**: Upload a starting image and describe the motion you want. You can also provide an end image to guide where the video should land.
> 
> ### Multi-shot mode
> 
> For videos with multiple scenes, use the `multi_prompt` parameter. Pass a JSON array of shot definitions, each with a prompt and duration. You can define up to 6 shots, with a minimum of 1 second per shot. The total duration of all shots must equal the `duration` parameter.
> 
> ```json
> [
>   {"prompt": "A woman walks through a sunlit forest", "duration": 5},
>   {"prompt": "She stops and looks up at the canopy", "duration": 3},
>   {"prompt": "Sunlight breaks through the leaves", "duration": 2}
> ]
> ```
> 
> ### Writing effective prompts
> 
> Structure your prompts to cover:
> 
> - **Scene setting**: Where and when the action happens, lighting conditions
> - **Subject details**: What characters or objects appear, how they look
> - **Motion**: What happens, how things move, camera behavior
> - **Audio** (if enabled): Dialogue in quotation marks, ambient sounds, sound effects
> 
> Example: `A chef in a busy kitchen plates a dish with careful precision, steam rising from the food. Camera slowly pushes in on the plate. Sizzling sounds, kitchen chatter in the background, the chef says "Perfect."`
> 
> ### Parameters
> 
> - **mode**: `standard` (720p) or `pro` (1080p)
> - **duration**: 3 to 15 seconds
> - **aspect_ratio**: 16:9, 9:16, or 1:1 (ignored when using a start image)
> - **generate_audio**: Toggle native audio on or off
> - **negative_prompt**: Describe what to exclude from the generation
> 
> ## What it's good for
> 
> - Marketing and advertising videos
> - Social media content with dialogue
> - Multi-scene narratives and short stories
> - Product demonstrations
> - Cinematic sequences with synchronized audio
> 
> ## Limitations
> 
> - Maximum 15 seconds per generation
> - Audio works best in English and Chinese
> - Character appearance can vary across separate generations
> - Complex physics interactions may not look fully natural
> - For longer videos, generate multiple clips and stitch them together
> 
> ## Privacy policy
> 
> https://app.klingai.com/global/dev/document-api/protocols/privacyPolicy
> 
> ## API terms
> 
> https://app.klingai.com/global/dev/document-api/protocols/paidServiceProtocol
> 
> ## Service level agreement
> 
> https://app.klingai.com/global/dev/document-api/protocols/paidLevelProtocol

