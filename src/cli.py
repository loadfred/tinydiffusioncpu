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
			"-3- Loras (enable/disable, edit weights)",
				f"\tEnabled: {', '.join([path.splitext(path.split(i)[1])[0] for i in Config.lora_files])}",
				f"\tWeights: {', '.join(map(str, Config.lora_weights))}",
			"-4- TCD/LCM (speed lora)",
				f"\t{str_mode}",
			"-5- Generation Options (steps/cfg/eta/seed)",
				f"\t({Config.steps}/{Config.cfg}/{Config.eta}/{Config.seed})",
			"-6- Image Size (width/height)",
				f"\t({Config.width}/{Config.height})",
			"-7- Image Save Directory",
				f"\t{Config.save_dir}",
			"-8- Config (save/reload)",
			"-9- Exit",
		sep="\n")
		while True:
			choice = strict_input(int, 0, "Number (0): ")
			match choice:
				case 0:
					if Config.model != "":
						try:
							# sd 1.5 pipeline
							txt2img.sd15()
							# FIX THIS, allow user to keep program open to generate another image
							print("Start again to generate another image")
						except:
							print("Invalid model")
						exit()
					else:
						print("Choose a model first")
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
					print("-0- Enter Model Path [.safetensors, .ckpt]")
					for subdir, dirs, files in walk(Config.model_dir):
						for file in files:
							if path.splitext(file)[1] in (".safetensors", ".ckpt"):
								models.append(path.join(subdir, file))
								print(f"-{len(models)}- {path.splitext(file)[0]}")
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
							# go back
							break
					break
				case 3:
					loras = []
					print("-0- Enter Lora Path [.safetensors]")
					for subdir, dirs, files in walk(Config.lora_dir):
						# ignore subdir "special" which holds tcd/lcm loras
						if subdir != path.join(Config.lora_dir, "special"):
							for file in files:
								if path.splitext(file)[1] == ".safetensors":
									loras.append(path.join(subdir, file))
									print(f"-{len(loras)}- {path.splitext(file)[0]}")
					print(f"-{len(loras)+1}- Back")
					while True:
						choice = strict_input(int, 0, "Lora (0): ")
						if choice < len(loras)+1 and choice > 0:
							lora_path = loras[choice-1]
						elif choice == 0:
							lora_path = strict_input(
								str, "",
								"Enter Lora Path: "
							)
							if lora_path == "":
								print("Empty input")
								continue
							elif not path.isfile(lora_path):
								print("Lora doesn't exist")
								continue
							elif path.splitext(lora_path)[1] != ".safetensors":
								print("Lora isn't .safetensors")
								continue
						else:
							# go back
							break
						if lora_path in Config.lora_files:
							print("Lora already in use")
							yn = strict_input(
								str, "n",
								"Disable Lora? (y/N): "
							)
							lora_index = Config.lora_files.index(lora_path)
							if yn.lower() in ("y", "yes", "certainly"):
								Config.lora_weights.pop(lora_index)
								Config.lora_files.pop(lora_index)
								print(f"{path.splitext(path.split(lora_path)[1])[0]} disabled")
								break
							weight = strict_input(
								float, Config.lora_weights[lora_index],
								f"Edit Lora Weight ({Config.lora_weights[lora_index]}): "
							)
							Config.lora_weights[lora_index] = weight
							break
						else:
							weight = strict_input(
								float, Config.lora_default_weight,
								f"Lora Weight ({Config.lora_default_weight}): "
							)
							Config.lora_files.append(lora_path)
							Config.lora_weights.append(weight)
							break
					break
				case 4:
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
				case 5:
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
				case 6:
					Config.width = strict_input(
						int, Config.width,
						f"Width ({Config.width}): "
					)
					Config.height = strict_input(
						int, Config.height,
						f"Height ({Config.height}): "
					)
					break
				case 7:
					print(f"\nCurrent: {Config.save_dir}")
					print("[leave empty to keep current]")
					Config.save_dir = strict_input(
						str, Config.save_dir,
						"Image Save Directory: "
					)
					break
				case 8:
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
				case 9:
					exit()
				case _:
					print("Invalid choice")


if __name__ == "__main__":
	cli()
