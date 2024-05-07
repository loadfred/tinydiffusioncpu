from os import path, rename
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation


class Config:
	root_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), ".."))
	# dirs only provided here in case paths from config.ini are deleted
	model_dir = path.join(root_dir, "models")
	lora_dir = path.join(root_dir, "loras") # ONLY USED FOR TCD/LCM, NO OTHER LORA SUPPORT
	embed_dir = path.join(root_dir, "embeddings")

	save_dir = path.join(path.expanduser("~"), "Pictures")
	save_name = ""
	save = ""

	pos_prompt = ""
	neg_prompt = ""

	steps = 6
	cfg = 1.4
	eta = 0.3
	seed = -1 # -1 is random
	width = 512
	height = 512
	is_safe = False # True = sfw guaranteed, downloads safety checker if online
	# can only go offline once 
	# config.json, tokenizer_config.json, vocab.json, merges.txt, special_tokens_map.json, tokenizer.json
	# downloaded from https://huggingface.co/openai/clip-vit-large-patch14/tree/main
	# (after you generate your first image)
	offline = False

	model = ""

	lora_files = [] # strings
	lora_weights = [] # floats
	lora_default_weight = 0.8

	# version = 1 # UNUSED 1=1.5, 2=2.1, 3=xl
	mode = 1 # 0=none, 1=tcd, 2=lcm
	special_weight = 1.0
	tcd = path.join(lora_dir, "special", "tcd-sd15.safetensors")
	lcm = path.join(lora_dir, "special", "lcm-sd15.safetensors")


def set_save():
	# call when saving image
	Config.save_name = path.splitext(path.split(Config.model)[1])[0] + datetime.now().strftime("-%Y%m%d-%H%M%S-%f") + ".png"
	Config.save = path.join(Config.save_dir, Config.save_name)


def write_config():
	# write to config.ini
	# called when option chosen
	config_file = path.join(Config.root_dir, "configs", "config.ini")
	config = ConfigParser()

	config["PROMPT"] = {
		"positive": Config.pos_prompt,
		"negative": Config.neg_prompt,
	}
	config["OPTIONS"] = {
		"steps": Config.steps,
		"cfg": Config.cfg,
		"eta": Config.eta,
		"seed": Config.seed,
		"width": Config.width,
		"height": Config.height,
		"safe": Config.is_safe,
		"offline": Config.offline,
	}
	config["MODEL"] = {
		"model": Config.model,
	}
	config["PATHS"] = {
		"root": Config.root_dir,
		"models": path.join("${root}", "models"),
		"loras": path.join("${root}", "loras"),
		"embeddings": path.join("${root}", "embeddings"),
		"saves": Config.save_dir,
	}
	config["LORAS"] = {
		"files": "\n".join(Config.lora_files),
		"weights": "\n".join(map(str, Config.lora_weights)),
		"default_weight": Config.lora_default_weight,
	}
	config["SPECIAL"] = {
		"mode": Config.mode,
		"weight": Config.special_weight,
		"tcd": path.join("${PATHS:loras}", "special", "tcd-sd15.safetensors"),
		"lcm": path.join("${PATHS:loras}", "special", "lcm-sd15.safetensors"),
	}

	if path.isfile(config_file):
		rename(config_file, path.join(Config.root_dir, "configs", "config.ini.bak"))
	with open(config_file, "w") as file:
		config.write(file)
		print(f"Saved config -> {config_file}")


def read_config():
	# read from config.ini
	# set variables in class Config
	# called on start

	def bad_config(msg):	
		print(
			msg,
			"Fix config or resave it",
		sep="\n")
		choice = input("Load and save default config? (Y/n): ")
		if choice.lower() in ("", "y"):
			write_config()
			return
		else:
			exit()

	config_file = path.join(Config.root_dir, "configs", "config.ini")
	config = ConfigParser(interpolation=ExtendedInterpolation())

	# config doesn't exist
	if not path.isfile(config_file):
		write_config()
		return

	try:
		config.read(config_file)
	except:
		bad_config("Can't read config.ini, bad formatting")
		return
	try:
		Config.pos_prompt = config.get("PROMPT", "positive", fallback=Config.pos_prompt)
		Config.neg_prompt = config.get("PROMPT", "negative", fallback=Config.neg_prompt)

		Config.steps = config.getint("OPTIONS", "steps", fallback=Config.steps)
		Config.cfg = config.getfloat("OPTIONS", "cfg", fallback=Config.cfg)
		Config.eta = config.getfloat("OPTIONS", "eta", fallback=Config.eta)
		Config.seed = config.getint("OPTIONS", "seed", fallback=Config.seed)
		Config.width = config.getint("OPTIONS", "width", fallback=Config.width)
		Config.height = config.getint("OPTIONS", "height", fallback=Config.height)
		Config.is_safe = config.getboolean("OPTIONS", "safe", fallback=Config.is_safe)
		Config.offline = config.getboolean("OPTIONS", "offline", fallback=Config.offline)

		Config.model = config.get("MODEL", "model", fallback=Config.model)

		Config.root_dir = config.get("PATHS", "root", fallback=Config.root_dir)
		Config.model_dir = config.get("PATHS", "models", fallback=Config.model_dir)
		Config.lora_dir = config.get("PATHS", "loras", fallback=Config.lora_dir)
		Config.embed_dir = config.get("PATHS", "embeddings", fallback=Config.embed_dir)
		Config.save_dir = config.get("PATHS", "saves", fallback=Config.save_dir)

		Config.lora_default_weight = config.getfloat("LORAS", "default_weight", fallback=Config.lora_default_weight)
		if config.get("LORAS", "files") != "":
			save_me = False
			# allow use of commas and quotes in LORAS files/weights config.ini list (they won't change anything)
			Config.lora_files = config.get("LORAS", "files").replace(",", "").replace('"', "").replace("'", "").split("\n")
			if config.get("LORAS", "weights") != "":
				Config.lora_weights = [float(i) for i in config.get("LORAS", "weights").replace(",", "").replace('"', "").replace("'", "").split("\n")]
			while len(Config.lora_files) > len(Config.lora_weights):
				save_me = True
				Config.lora_weights.append(Config.lora_default_weight)
				print("More lora files than lora weights in config.ini, setting",
					f"{path.splitext(path.split(Config.lora_files[len(Config.lora_weights)-1])[1])[0]}",
					f"to {Config.lora_default_weight} weight")
			if save_me:
				# save config if default weight automatically added for lora
				write_config()

		Config.mode = config.getint("SPECIAL", "mode", fallback=Config.mode)
		Config.special_weight = config.getfloat("SPECIAL", "weight", fallback=Config.special_weight)
		Config.tcd = config.get("SPECIAL", "tcd", fallback=Config.tcd)
		Config.lcm = config.get("SPECIAL", "lcm", fallback=Config.lcm)
	except:
		bad_config("Missing [SECTION], unknown ${key}, or using a string where a number is expected in config.ini")
		return
