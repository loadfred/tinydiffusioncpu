@echo off
set "BASEDIR=%~dp0"
set PYTHON=py
REM DIFFUSERS OPTIONS
REM set HF_HUB_OFFLINE=True
set DISABLE_TELEMETRY=YES

if exist "%BASEDIR%.env" (
	%PYTHON% -m venv "%BASEDIR%.env"
	"%BASEDIR%.env\Scripts\activate"
	%PYTHON% -m pip install -r "%BASEDIR%requirements.txt"

	echo Installed python environment

	if exist "%BASEDIR%loras\special\tcd-sd15.safetensors" (
		echo TCD: TCD is like LCM, fast results, a bit faster than LCM, 4-8 steps, better lighting, worse faces than LCM, less blurry than LCM below 4 steps
		set choice=
		set /p choice=Download TCD lora? (135MB) (Y/n): 
		if not '%choice%'=='' set choice=%choice:~0,1%
		if '%choice%'=='N' goto notcd
		if '%choice%'=='n' goto notcd
		curl.exe -o "%BASEDIR%loras\special\tcd-sd15.safetensors" -L https://huggingface.co/h1t/TCD-SD15-LoRA/resolve/main/pytorch_lora_weights.safetensors?download=true
		:notcd
	)

	if exist "%BASEDIR%loras\special\lcm-sd15.safetensors" (
		echo LCM: Fast results, 4-8 steps, better faces than TCD
		set choice=
		set /p choice=Download LCM lora? (135MB) (Y/n): 
		if not '%choice%'=='' set choice=%choice:~0,1%
		if '%choice%'=='N' goto nolcm
		if '%choice%'=='n' goto nolcm
		curl.exe -o "%BASEDIR%loras\special\lcm-sd15.safetensors" -L https://huggingface.co/latent-consistency/lcm-lora-sdv1-5/resolve/main/pytorch_lora_weights.safetensors?download=true
		:nolcm
	)
) else (
	"%BASEDIR%.env\Scripts\activate"
)

%PYTHON% "%BASEDIR%src\cli.py"
pause
