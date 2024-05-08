#!/bin/sh
BASEDIR=$(dirname "$0")
PYTHON=python3
# DIFFUSERS OPTIONS
HF_HUB_OFFLINE=True
DISABLE_TELEMETRY=YES

if [ ! -d "$BASEDIR/.env" ] ; then
	$PYTHON -m venv "$BASEDIR/.env"
	. "$BASEDIR/.env/bin/activate"
	$PYTHON -m pip install -r "$BASEDIR/requirements.txt"

	echo "Installed python environment"

	if [ ! -f "$BASEDIR/loras/special/tcd-sd15.safetensors" ] ; then
		echo "TCD: TCD is like LCM, fast results, a bit faster than LCM, 4-8 steps, better lighting, worse faces than LCM, less blurry than LCM below 4 steps"
		read -p "Download TCD lora? (135MB) (Y/n): " yn
		case $yn in
			[nN])
				break;;
			*)
				curl -o "$BASEDIR/loras/special/tcd-sd15.safetensors" -L https://huggingface.co/h1t/TCD-SD15-LoRA/resolve/main/pytorch_lora_weights.safetensors?download=true
		esac
	fi

	if [ ! -f "$BASEDIR/loras/special/lcm-sd15.safetensors" ] ; then
		echo "LCM: Fast results, 4-8 steps, better faces than TCD"
		read -p "Download LCM lora? (135MB) (Y/n): " yn
		case $yn in
			[nN])
				break;;
			*)
				curl -o "$BASEDIR/loras/special/lcm-sd15.safetensors" -L https://huggingface.co/latent-consistency/lcm-lora-sdv1-5/resolve/main/pytorch_lora_weights.safetensors?download=true
		esac
	fi

else
	. "$BASEDIR/.env/bin/activate"
fi

$PYTHON "$BASEDIR/src/cli.py"
