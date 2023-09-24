@echo off

REM This is for windows 11 and cuda 12.2 if you want to use another os then select another option or go here if your option is not available.
REM https://developer.nvidia.com/cuda-downloads
REM This also assumes you're running this with install.py
@echo off
REM This script is for Windows and assumes you're running it with administrative privileges

REM Activate the virtual environment
call venv\Scripts\activate
echo Activated virtual environment

REM Install requirements
call install\environments.bat

REM Install nvidia tools
python -m pip install nvidia-pyindex

REM Check for CUDA download and downloading if not
if not exist "cuda_installer.exe" (
    curl -o cuda_installer.exe https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda_12.2.2_537.13_windows.exe
)

REM Install CUDA
start /wait cuda_installer.exe

REM Install torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -q

REM Check CUDA
python -c "import torch; print(torch.cuda.is_available())"
if errorlevel 1 (
    echo CUDA is not available. Installation failed
) else (
    echo CUDA is successfully installed
)

REM Remove the local installer
if exist "cuda_installer.exe" (
    del cuda_installer.exe
)
