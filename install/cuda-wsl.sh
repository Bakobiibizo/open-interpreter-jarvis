# This is for ubuntu 22.04 running in a WSL environment if you want to use another os or version of ubuntu go here:
# https://developer.nvidia.com/cuda-downloads?
# Do not install any other version of torch or install this after installing other programs that install torch as their dependencies 
# Also this assumes you've run the install.sh script first

# Activate the virtual environment
source venv/bin/activate
echo Activated virtual environment

# Install CUDA-wsl

# setup env
sudo bash install/environment.sh

# check pin
if sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/7fa2af80.pub
then
    sudo apt-key del 7fa2af80
fi

# Download and install pin
sudo bash install/is_file.sh /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600


# Install CUDA

# Check if the local installer is already downloaded if not download it
sudo bash install/is_file.sh cuda-repo-wsl-ubuntu-12-2-local_12.2.1-1_amd64.deb https://developer.download.nvidia.com/compute/cuda/12.2.1/local_installers/cuda-repo-wsl-ubuntu-12-2-local_12.2.1-1_amd64.deb

# Unpack and install
sudo dpkg -i cuda-repo-wsl-ubuntu-12-2-local_12.2.1-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu -q

# Check if CUDA is available
if python -c "import torch; print(torch.cuda.is_available())" ; then
    nvidia-smi
    echo "CUDA is available"
else
    echo "CUDA is not available. Instillation failed"
fi

