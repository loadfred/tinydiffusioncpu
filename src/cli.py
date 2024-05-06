from os import path, walk
from config import Config, write_config, read_config
import txt2img


def strict_input(
	value_type: type,
	value_default: any,
	msg: str
):
	try:
		value = input(msg)
		if value != "":
			value = value_type(value)
		else:
			value = value_type(value_default)
			print("Default chosen")
	except:
		value = value_type(value_default)
		print("Default chosen")
	return value


def cli():
	read_config()
	while True:
		match Config.mode:
			case 1:
				str_mode = "TCD: " + f"{path.splitext(path.split(Config.tcd)[1])[0]}"
			case 2:
				str_mode = "LCM: " + f"{path.splitext(path.split(Config.lcm)[1])[0]}"
			case _:
				str_mode = "None"
		print(
			"",
			"-0- GENERATE IMAGE",
			"-1- Prompt (pos/neg)",
				f"\tPos: {Config.pos_prompt[:40]}...",
				f"\tNeg: {Config.neg_prompt[:40]}...",
			"-2- Model",
				f"\t{path.splitext(path.split(Config.model)[1])[0]}",
			"-3- TCD/LCM (speed lora)",
				f"\t{str_mode}",
			"-4- Generation Options (steps/cfg/eta/seed)",
				f"\t({Config.steps}/{Config.cfg}/{Config.eta}/{Config.seed})",
			"-5- Image Size (width/height)",
				f"\t({Config.width}/{Config.height})",
			"-6- Image Save Directory",
				f"\t{Config.save_dir}",
			"-7- Config (save/reload)",
			"-8- Exit",
		sep="\n")
		while True:
			choice = strict_input(int, 0, "Number (0): ")
			match choice:
				case 0:
					# sd 1.5 pipeline
					try:
						txt2img.sd15()
						# FIX THIS, allow user to keep program open to generate another image
						print("Start again to generate another image")
						exit()
					except:
						print("Invalid model")
				case 1:
					print(f"\nCurrent Positive: {Config.pos_prompt}")
					print("[leave empty to keep current]")
					Config.pos_prompt = strict_input(
						str, Config.pos_prompt,
						"Positive Prompt: "
					)
					print(f"\nCurrent Negative: {Config.neg_prompt}")
					print("[leave empty to keep current]")
					Config.neg_prompt = strict_input(
						str, Config.neg_prompt,
						"Negative Prompt: "
					)
					break
				case 2:
					models = []
					for subdir, dirs, files in walk(Config.model_dir):
						for file in files:
							if path.splitext(file)[1] in (".safetensors", ".ckpt"):
								models.append(path.join(subdir, file))
					print("-0- Enter Model Path [.safetensors, .ckpt]")
					for i in range(1, len(models)+1):
						print(f"-{i}- {path.splitext(path.split(models[i-1])[1])[0]}")
					print(f"-{len(models)+1}- Back")
					while True:
						choice = strict_input(int, 0, "Model (0): ")
						if choice < len(models)+1 and choice > 0:
							Config.model = models[choice-1]
							break
						elif choice == 0:
							print(f"\nCurrent: {Config.model}")
							print("[leave empty to keep current]")
							Config.model = strict_input(
								str, Config.model,
								"Enter Model Path: "
							)
							break
						else:
							break
					break
				case 3:
					print(
						"-0- None [slow, 15-45 steps for quality]",
						"-1- TCD [fast, a bit faster than LCM, better lighting, 4-8 steps for quality]",
						"-2- LCM [fast, better faces, 4-8 steps for quality]",
					sep="\n")
					Config.mode = strict_input(
						int, Config.mode,
						f"Mode ({Config.mode}): "
					)
					break
				case 4:
					Config.steps = strict_input(
						int, Config.steps,
						f"Steps ({Config.steps}): "
					)
					Config.cfg = strict_input(
						float, Config.cfg,
						f"CFG [1.0-2.0 with TCD/LCM, >1.0 for negative prompt] ({Config.cfg}): "
					)
					Config.eta = strict_input(
						float, Config.eta,
						f"ETA ({Config.eta}): "
					)
					Config.seed = strict_input(
						int, Config.seed,
						f"Seed [-1 is random] ({Config.seed}): "
					)
					break
				case 5:
					Config.width = strict_input(
						int, Config.width,
						f"Width ({Config.width}): "
					)
					Config.height = strict_input(
						int, Config.height,
						f"Height ({Config.height}): "
					)
					break
				case 6:
					print(f"\nCurrent: {Config.save_dir}")
					print("[leave empty to keep current]")
					Config.save_dir = strict_input(
						str, Config.save_dir,
						"Image Save Directory: "
					)
					break
				case 7:
					print(
						"-0- Save Config [loads on start]",
						"-1- Reload Config",
						"-2- Back",
					sep="\n")
					choice = strict_input(int, 0, "Number (0): ")
					match choice:
						case 0:
							write_config()
						case 1:
							read_config()
						case _:
							pass
					break
				case 8:
					exit()
				case _:
					print("Invalid choice")


if __name__ == "__main__":
	cli()
