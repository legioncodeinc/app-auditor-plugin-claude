URL: https://replicate.com/runwayml/gen-4.5/llms.txt
Fetched: 2026-10-11T00:24:07.163908+00:00
Source type: official model card and schema

## Basic model info

Model name: runwayml/gen-4.5
Model description: State-of-the-art video motion quality, prompt adherence and visual fidelity


## Model inputs

- prompt (required): Text prompt for video generation (string)
- image (optional): Optional initial image for video generation (first frame). If not provided, video will be generated from text only. (string)
- aspect_ratio (optional): Video aspect ratio (string)
- duration (optional): Duration of the output video in seconds (integer)
- seed (optional): Random seed. Set for reproducible generation (integer)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/3w3dfb5wxdrmw0cwdt1v9ngfw0)

#### Input

```json
{
  "prompt": "A dense, verdant jungle world made up of small lego-like pieces. We see a rainbow chameleon running through the 3D world, the camera in and out of focus.",
  "duration": 10,
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/AlfC7qolTq1YXysS5Aak9WavhusB7WtrgUu6GEpZCoBIlWELA/tmp82ivy7af.mp4"
```


### Example (https://replicate.com/p/dvj6f7jd7xrmt0cwe59b2fm4xg)

#### Input

```json
{
  "prompt": "A raccoon in a plain room in zero gravity trying to steal the garbage from a silver trash can. The garbage floats out in zero gravity. Handheld documentary film style. Natural camera shake. Raw indie film aesthetic. Natural lighting. Unpolished, authentic look. Low budget realism. Observational feel.",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/yW6nHlIueOVEOKdj2yKfwpNuRxQxht7cFOfAre90Z1tfAFHxC/tmpnu5_sor8.mp4"
```


### Example (https://replicate.com/p/361ccda5wdrmy0cwe5ka3yv2j0)

#### Input

```json
{
  "prompt": "A scene in new york city where all the cars and cabs start floating up. We see a girl watching the scene from the back",
  "duration": 10,
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/sKeeGbf5VkE38JUpOy7E1zgZvXoCKhU53N1TUBICEJWu9xRsA/tmpa37inqbf.mp4"
```


### Example (https://replicate.com/p/jz724z76kxrmr0cwe5nabrh4zm)

#### Input

```json
{
  "prompt": "A scene in new york city where all the cars and cabs start floating up. We see a girl watching the scene from the back. indie aesthetic, daytime",
  "duration": 10,
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/ufGgt53erfVj2pCKXfyswhqCAWoFQT8fTSnjvb5dxGfj0QOiF/tmpogqc4fdt.mp4"
```


## Model readme

> # 🎬 Runway Gen-4.5
> 
> **Runway Gen-4.5** is the world’s top-rated video generation model, delivering unprecedented visual fidelity, cinematic realism, and precise creative control. It empowers creators and organizations to produce highly dynamic, controllable, and visually stunning video content at scale.
> 
> ---
> 
> ## 🚀 Overview
> 
> Two years ago, **Gen-1** introduced the first publicly available video generation model, creating an entirely new category of creative tools. Since then, Runway has led the industry in advancing controllable and high-performance video models.
> 
> **Gen-4.5** represents the next major leap in video generation — improving both:
> 
> - **Pre-training data efficiency**
> - **Post-training optimization techniques**
> - **Dynamic action generation**
> - **Temporal consistency**
> - **Precise controllability**
> 
> With **1,247 Elo points**, Gen-4.5 holds the **#1 position** in the Artificial Analysis Text-to-Video Benchmark (as of November 30, 2025).
> 
> Gen-4.5 maintains the speed and efficiency of Gen-4 while delivering breakthrough quality — all at comparable pricing across subscription plans.
> 
> ---
> 
> ## 🏆 Benchmark Leadership
> 
> - **#1 Ranked** in Artificial Analysis Text-to-Video Leaderboard  
> - **1,247 Elo Score**
> - Surpasses all competing video generation models
> 
> ---
> 
> ## ✨ Core Capabilities
> 
> ### 🎯 Precise Prompt Adherence
> 
> Gen-4.5 achieves unprecedented physical accuracy and visual precision:
> 
> - Realistic weight, momentum, and force in object motion  
> - Accurate liquid dynamics  
> - High-fidelity surface rendering  
> - Coherent fine details (hair strands, fabric weave, textures) across motion  
> 
> ---
> 
> ### 🎬 Complex Scene Generation
> 
> #### 🧩 Intricate Multi-Element Scenes
> Highly detailed environments rendered with precision and consistency.
> 
> #### 🖼 Detailed Compositions
> Precise placement and fluid motion for characters and objects.
> 
> #### ⚙️ Physical Accuracy
> Believable collisions, natural motion, and consistent physics.
> 
> #### 🎭 Expressive Characters
> Nuanced facial expressions, realistic gestures, and lifelike emotional depth.
> 
> ---
> 
> ## 🎨 Stylistic Control & Visual Consistency
> 
> Gen-4.5 supports a broad range of aesthetics while maintaining coherent visual language across frames.
> 
> ### 📸 Photorealistic
> Visuals indistinguishable from real-world footage.
> 
> ### 🎨 Non-Photorealistic
> Stylized and expressive animation unconstrained by realism.
> 
> ### 🏡 Slice of Life
> Authentic everyday environments with true-to-life detail.
> 
> ### 🎥 Cinematic
> Emotionally powerful visuals with striking depth and polish.
> 
> ---
> 
> ## ⚡ Performance & Deployment
> 
> ### 🖥 High-Performance Infrastructure
> 
> Gen-4.5 was developed entirely on **NVIDIA GPUs**, spanning:
> 
> - Initial research & development  
> - Pre-training  
> - Post-training  
> - Inference  
> 
> Inference runs on:
> - **NVIDIA Hopper GPUs**
> - **NVIDIA Blackwell GPUs**
> 
> Through deep collaboration with NVIDIA, Runway has optimized:
> 
> - Training efficiency  
> - Diffusion model optimization  
> - Inference speed  
> 
> All without compromising quality.
> 
> > “This is an incredibly exciting time for video and world models.  
> > We’re proud that Runway built their groundbreaking video and world model on NVIDIA GPUs…”  
> > — Jensen Huang, President & CEO of NVIDIA
> 
> ---
> 
> ## 🏢 Early Access Enterprise Partners
> 
> Gen-4.5 is already in use across multiple industries:
> 
> - Retail & E-commerce  
> - Marketing & Advertising  
> - Gaming  
> 
> ---
> 
> ## 🧰 Supported Control Modes
> 
> Coming to Gen-4.5:
> 
> - Image-to-Video  
> - Keyframes  
> - Video-to-Video  
> - Additional advanced control modes  
> 
> ---
> 
> ## ⚠️ Known Limitations
> 
> Despite significant advances, Gen-4.5 shares some limitations common to video generation systems:
> 
> ### 🔄 Causal Reasoning
> Effects may sometimes precede causes  
> (e.g., a door opening before the handle is pressed).
> 
> ### 🫥 Object Permanence
> Objects may disappear or reappear unexpectedly across frames.
> 
> ### 🎯 Success Bias
> Actions may succeed disproportionately  
> (e.g., a poorly aimed kick still scoring a goal).
> 
> These challenges are especially relevant to world model research, where accurate representation of action outcomes is critical. Ongoing research aims to address these limitations.
> 
> ---
> 
> ## 🌍 Built for the Future of Video
> 
> Gen-4.5 pushes the frontier of video generation by combining:
> 
> - State-of-the-art realism  
> - Fine-grained controllability  
> - High-performance deployment  
> - Broad accessibility  
> 
> It makes world-class video generation available to creators and enterprises at every scale.

