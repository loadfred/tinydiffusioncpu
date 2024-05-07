# TinyDiffusionCPU
Stable Diffusion for CPU only, CLI only, uses [TCD](https://github.com/jabir-zheng/TCD), [LCM](https://github.com/luosiallen/latent-consistency-model), or neither, your choice

Uses [Diffusers](https://huggingface.co/docs/diffusers/tutorials/tutorial_overview) with Python

## Dependencies
- python 3.8 or greater
  - pip modules automatically installed with start.sh
- wget
  - used for downloading TCD/LCM safetensors with start.sh
 
## Install & Run
Currently Linux & FreeBSD only (just need a .bat file for Windows)

`git clone https://github.com/loadfred/tinydiffusioncpu.git`

Enter the directory and execute the start.sh script

`./start.sh`

This will install the python environment in tinydiffusioncpu/.env/, pip modules from requirements.txt, and then the TCD/LCM loras if you approve (1.4 G)

Then it will act as a start script once everything is setup

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
- Loras
  - Stable Diffusion 1.5 TCD/LCM loras supported (installed with start.sh script)
  - Place your .safetensors loras in the loras folder
  - Choose from loras with the cli (automatically detected) or enter full path
  - Enter lora weights, usually between 0.4 and 1.0
  - Able to enable/disable/edit loras in use in cli
- Embeddings (textual inversions)
  - Place .pt/.safetensors in embeddings folder
  - All embeddings automatically loaded, nothing else required
  - Use embedding by typing the filename in positive prompt or negative prompt
    - e.g. embeddings/FastNegativeV2.pt -> *NEGATIVE PROMPT:* ugly, malformed body, FastNegativeV2, interlocked fingers
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
```
[PROMPT]
positive = masterpiece, 8k, smiling+, (woman sitting)1.3 on chair, asian---, forest, (yellow dress)++, black shoes, (sunrise)+++
negative = FastNegativeV2+++,ugly, (bad face)++, small eyes, UnrealisticDream+++

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
model = /home/me/src/stable-diffusion/tinydiffusioncpu/models/dreamshaper_8.safetensors

[PATHS]
root = /home/me/src/stable-diffusion/tinydiffusioncpu
models = ${root}/models
loras = ${root}/loras
embeddings = ${root}/embeddings
saves = /home/me/Pictures/ai

[SPECIAL]
mode = 1
tcd = ${PATHS:loras}/special/tcd-sd15.safetensors
lcm = ${PATHS:loras}/special/lcm-sd15.safetensors
```
