#! /bin/bash/
# This is for ubuntu 22.04 if you want to use another os go here 
# https://developer.nvidia.com/cuda-downloads?
# Also this assumes you've run the install.sh script first

# Activate the virtual environment
source venv/bin/activate
echo Activated virtual environment

# Install requirements

sudo bash install/environments.sh

# Delete key
sudo apt-key del -7fa2af80


# Download and install pin
sudo bash install/is_file.sh /etc/apt/preferences.d/cuda-ubuntu2204.pin cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600

# Checking for cuda download and downloading if not
if command -v nvcc &> /dev/null
    then
        sudo bash install/is_file.sh cuda-repo-ubuntu2204-12-2-local_12.2.2-535.104.05-1_amd64.deb https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda-repo-ubuntu2204-12-2-local_12.2.2-535.104.05-1_amd64.deb
fi

# Unpack and install
sudo dpkg -i cuda-repo-ubuntu2204-12-2-local_12.2.2-535.104.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda


# Install torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -q

# Check CUDA
if python -c "import torch; print(torch.cuda.is_available())"; 
    then
        nvidia-smi
    else
        echo "CUDA is not available. Instillation failed"
fi

# Remove the local installer
if cuda-repo-ubuntu2204-12-2-local_12.2.2-535.104.05-1_amd64.deb
    then
        sudo rm cuda-repo-ubuntu2204-12-2-local_12.2.2-535.104.05-1_amd64.deb
fi