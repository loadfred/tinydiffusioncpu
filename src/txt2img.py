import torch
from diffusers import StableDiffusionPipeline
from compel import Compel, DiffusersTextualInversionManager
from os import path, walk
from config import Config, set_save


lora_names = []
lora_weights = []


def load_lora(pipe, file, weight):
		wn = path.split(file)[1]
		an = path.splitext(wn)[0]
		pipe.load_lora_weights(
			file,
			weight_name = wn,
			adapter_name = an,
			local_files_only = Config.offline,
		)
		lora_names.append(an)
		lora_weights.append(weight)
		print(f"Loaded lora: {an} {weight}")


def sd15():

	pipe_args = {
		# "pretrained_model_or_path": Config.model, # AutoPipeline
		# "pretrained_model_name_or_path": Config.model, # from_pretrained
		"pretrained_model_link_or_path": Config.model, # from_single_file
		"torch_dtype": torch.float32,
		"local_files_only": Config.offline,
	}
	if not Config.is_safe:
		pipe_args.update({"safety_checker": None}) 
	# pipe = AutoPipelineForText2Image.from_pretrained(**pipe_args)
	# pipe = StableDiffusionPipeline.from_pretrained(**pipe_args)
	pipe = StableDiffusionPipeline.from_single_file(**pipe_args)

	if Config.vae_taesd == True:
		from diffusers import AutoencoderTiny
		pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd", torch_dtype=torch.float32)
		print("Set VAE: TAESD")
	elif Config.vae != "":
		from diffusers import AutoencoderKL
		pipe.vae = AutoencoderKL.from_single_file(Config.vae, torch_dtype=torch.float32)
		print(f"Set VAE: {path.splitext(path.split(Config.vae)[1])[0]}")

	# said to decrease memory usage
	pipe.unet.to(memory_format=torch.channels_last)
	pipe.vae.to(memory_format=torch.channels_last)
	pipe.text_encoder.to(memory_format=torch.channels_last)
	if Config.is_safe:
		pipe.safety_checker.to(memory_format=torch.channels_last)

	if Config.mode > 0:
		match Config.mode:
			case 1:
				from diffusers import TCDScheduler
				pipe.scheduler = TCDScheduler.from_config(pipe.scheduler.config)
				special_lora = Config.tcd
			case 2:
				from diffusers import LCMScheduler
				pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
				special_lora = Config.lcm
			case _:
				print("Invalid mode")
				exit()
		load_lora(pipe, special_lora, Config.special_weight)

	if len(Config.lora_files) > 0:
		for i in range(0, len(Config.lora_files)):
			load_lora(pipe, Config.lora_files[i], Config.lora_weights[i])

	if len(lora_weights) > 0:
		pipe.set_adapters(lora_names, adapter_weights=lora_weights)
		pipe.fuse_lora(adapter_names=lora_names, lora_scale=1.0)
		pipe.unload_lora_weights()
		print("Fused loras")

	# freeu: said to improve looks w/ no extra cpu/ram
	pipe.enable_freeu(s1=0.9, s2=0.2, b1=1.5, b2=1.6)

	# load ALL embeddings
	for subdir, dirs, files in walk(Config.embed_dir):
		for file in files:
			if path.splitext(file)[1] in (".safetensors", ".pt"):
				# token = filename, call embedding in prompt w/ filename
				pipe.load_textual_inversion(path.join(subdir, file), token=path.splitext(file)[0])
				print(f"Loaded embedding: {path.splitext(file)[0]}")

	# compel weights in prompts: ()++ ()-- ()1.5
	# conjunction to prompts: make use of commas
	# textual inversion: FastNegative, easynegative, etc.
	compel_proc = Compel(
		tokenizer = pipe.tokenizer,
		text_encoder = pipe.text_encoder,
		textual_inversion_manager = DiffusersTextualInversionManager(pipe),
	)
	pos_prompt = compel_proc(str(Config.pos_prompt.split(",")) + ".and()")
	neg_prompt = compel_proc(str(Config.neg_prompt.split(",")) + ".and()")

	image_args = {
		"prompt_embeds": pos_prompt,
		"negative_prompt_embeds": neg_prompt,
		"guidance_scale": Config.cfg,
		"width": Config.width,
		"height": Config.height,
		"num_inference_steps": Config.steps,
		"eta": Config.eta,
	}
	if Config.seed > -1:
		image_args.update({"generator": torch.manual_seed(Config.seed)})
	image = pipe(**image_args).images[0]

	set_save() # update model name + date in image name (Config.save variable)
	image.save(Config.save)
	print(f"Saved image -> {Config.save}")
