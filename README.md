# TinyDiffusionCPU
Stable Diffusion for CPU only, CLI only, uses [TCD](https://github.com/jabir-zheng/TCD), [LCM](https://github.com/luosiallen/latent-consistency-model), or neither, your choice

Uses [Diffusers](https://huggingface.co/docs/diffusers/tutorials/tutorial_overview) with Python

## Dependencies
- python 3.8 or greater
  - pip modules automatically installed with **start** script
- curl
  - used for downloading TCD/LCM safetensors with **start** script
- git
  - used to clone this repository
 
## Install & Run
Windows + Linux + FreeBSD support!

Open your terminal

`git clone https://github.com/loadfred/tinydiffusioncpu.git`

Enter the **tinydiffusioncpu** directory cloned

`cd tinydiffusioncpu`

Then execute the **start** script

### Windows

`start.bat`

### Linux & FreeBSD

`./start.sh`

If it's not running make sure it's executable (chmod +x ./start.sh)

This will install the python environment in tinydiffusioncpu/.env/, pip modules from requirements.txt, and then the TCD/LCM loras if you approve (1.4 Gi total)

Then it will act as a **start** script once everything is setup

You can delete the other **start** script for the OS you're not using

## Screenshot
![cli screenshot](https://github.com/loadfred/tinydiffusioncpu/blob/main/docs/images/cli.webp)

## Features
- Interactive command Line Interface (CLI) only
- Stable Diffusion 1.5 support only
- [Trajectory Consistency Distillation](https://github.com/jabir-zheng/TCD) (TCD) support
  - Faster than not having it
  - 4-8 steps for good quality
  - A bit faster than LCM (barely)
  - Better lighting
  - Less blurry than LCM when lower than 4 steps
- [Latent Consistency Model](https://github.com/luosiallen/latent-consistency-model) (LCM) support
  - Faster than not having it
  - 4-8 steps for good quality
  - Better faces than TCD
- Models
  - Place .safetensors/.ckpt in models folder
  - Choose from models in folder with the cli (it'll detect them) or enter full path
  - You can create subdirectories in the "models" folder and they'll still be searched through for model choosing
- Loras
  - Stable Diffusion 1.5 TCD/LCM loras supported (installed with **start** script)
  - Place your .safetensors loras in the loras folder
  - Choose from loras with the cli (automatically detected) or enter full path
  - Enter lora weights, usually between 0.4 and 1.0
  - Able to enable/disable/edit loras in use in cli
  - You can create subdirectories in the "loras" folder and they'll still be searched through for lora choosing
  - "special" directory is ignored, it contains the tcd/lcm loras
- Embeddings (textual inversions)
  - Place .pt/.safetensors in embeddings folder
  - All embeddings automatically loaded, nothing else required
  - Use embedding by typing the filename in positive prompt or negative prompt
    - e.g. embeddings/FastNegativeV2.pt -> *NEGATIVE PROMPT:* ugly, malformed body, FastNegativeV2, interlocked fingers
- VAEs
  - TAESD [(Tiny AutoEncoder for Stable Diffusion)](https://github.com/madebyollin/taesd)
    - less memory/cpu, worse images & faces
- Prompt Weighting
  - Uses [compel](https://github.com/damian0815/compel/blob/main/doc/syntax.md#weighting) + -
  - apple+ increases weight, sets weight to 1.1^n
  - apple- decreases weight, sets weight to 0.9^n
  - (apple)1.5 sets weight to 1.5
  - e.g. *PROMPT:* masterpiece, 8k, smiling+, (woman sitting)1.3 on chair, asian---, forest, (yellow dress)++, black shoes, (sunrise)+++
- Conjunction
  - Uses [compel](https://github.com/damian0815/compel/blob/main/doc/syntax.md#conjunction) conjunction
  - Keeps items/topics separate and a bit more distinguishable to the ai with commas
  - Used when you use commas in the prompt
- Generation Options
  - Inference steps
    - The higher, the better quality, the more time
    - Only 4-8 steps needed with TCD or LCM
    - 15-45 needed without TCD or LCM
  - CFG (guidance scale)
    - Keep greater than 1.0 for negative prompt to work
    - Best between 1.0 and 2.0 with TCD or LCM
    - Higher CFG = follows prompt better
  - [ETA](https://github.com/jabir-zheng/TCD?tab=readme-ov-file#text-to-image-generation) (gamma)
    - 0.3 is good with around 4 steps
    - Higher eta recommended for more steps
    - Controls stochasticity (predictability)
  - Seed
    - -1 is random
  - Image width / height
    - 256, 512, 768, 1024 sizes supported (width or height)
    - most SD 1.5 models work well with 512x512 or 512x768
  - Safety Checker
    - Choice, makes images safe for work
    - Downloads safety checker online if set to true
- Config
  - Automatically saved in configs folder when asked in CLI
  - .ini format
  - Ability to edit all options in the config file
  - Read on startup
  - Still able to edit options in CLI
- Image Save Directory
  - Directory to save images
  - Defaults to your "Pictures" directory

## configs/config.ini Example
(not a good lora combo or prompt, just a config example)

```
[PROMPT]
positive = (ghibli style)++,8k,bangs,cape,nature+,looking at viewer,necklace+,masterpiece,green eyes,3DMM+++
negative = FastNegativeV2++,easynegative+,ugly

[OPTIONS]
steps = 6
cfg = 1.4
eta = 0.3
seed = -1
width = 512
height = 768
safe = False
offline = False

[MODEL]
model = /home/me/src/stable-diffusion/tinydiffusioncpu/models/anime/AnythingXL_inkBase.safetensors

[PATHS]
root = /home/me/src/stable-diffusion/tinydiffusioncpu
models = ${root}/models
loras = ${root}/loras
embeddings = ${root}/embeddings
saves = /home/me/Pictures/ai

[LORAS]
files = /home/me/src/stable-diffusion/tinydiffusioncpu/loras/add_detail.safetensors
	/home/me/src/stable-diffusion/tinydiffusioncpu/loras/anime/ghibli_style_offset.safetensors
	/home/me/src/stable-diffusion/tinydiffusioncpu/loras/3DMM_V12.safetensors
weights = -1.5
	0.9
	1.0
default_weight = 0.8

[SPECIAL]
mode = 1
weight = 1.0
tcd = ${PATHS:loras}/special/tcd-sd15.safetensors
lcm = ${PATHS:loras}/special/lcm-sd15.safetensors

[VAE]
taesd = True
```

## Resource Usage
Most Stable Diffusion 1.5 models use around 5.7 Gi at 512x768 image width/height + 1.4 CFG + loras + embeddings

The time it takes to generate an image depends on your CPU, also the longer you use your CPU the slower it will get, allowing the CPU to relax helps speed up the next usage

Memory/CPU usage can be lowered by setting the CFG to 1.0 or lower, not using loras, not using embeddings, lower image size (512x512), by USING TCD or LCM at 4 steps, and ENABLE TAESD vae (less ram/cpu, worse images & faces)
