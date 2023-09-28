import os
import subprocess
import argparse
import loguru
from typing import List, Any

def chmod_files():
    """
    Set executable permissions on a list of files.

    This function takes no parameters.

    The files that need to have their permissions changed are specified in the `filenames` list.
    Each file in the list should be a string representing the relative path to the file, starting from the current working directory.

    This function does not return anything.

    If an error occurs while changing the permissions of a file, a `RuntimeError` exception is raised with a descriptive error message.

    Example usage:
    ```
    chmod_files()
    ```
    """
    filenames = [
        "install/cuda-ubuntu2004.sh",
        "install/cuda-ubuntu2204.sh",
        "install/cuda-wsl.sh",
        "install/environment.sh",
        "install/is_file.sh"
    ]
    cwd = os.getcwd()

    for filename in filenames:
        output = subprocess.run(["chmod", "+x", f"{cwd}/{filename}"], check=True)
        if output.returncode != 0:
            raise RuntimeError(f"Failed to chmod:\n{filename}")

chmod_files()        

#This has a return type of any because loguru is undefined until the function is called and would throw an error.
def init_logger() -> Any:
    """
    Initializes and configures a logger using the loguru library. We have to nest this inside of a function so we can install it before we use it.

    Returns:
        loguru._logger.Logger: The configured logger instance.
    """
    import loguru
    
    logger = loguru.logger
    logger.level("INFO")

    # logger options, lazy loading for stack trace with out performance hit, better exceptions, colors and setting the level
    logger.opt(lazy=True, exception=True, colors=True)

    return logger

# Installing loguru before we can use the logger
subprocess.run(["pip", "install", "loguru", "-q"], check=True)
logger = init_logger()


#This object's keys define the available packages to install. All packages get no_cuda first and then the correct version of torch is applied after all other instiliations. 
subprocesses ={
    "no_cuda": [
            
            ["sudo", "bash", "install/environment.sh"],
            ["sudo", "apt", "install", "build-essential", "-y", "-q"], 
            ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel", "-q"], 
            ["pip", "install", "ffmpeg", "-q"],
            ["pip", "install", "gradio", "-q"],
            ["pip", "install", "elevenlabs", "-q"], 
            ["pip", "install", "git+https://github.com/openai/whisper.git", "-q", "--no-deps"], 
            ["pip", "install", "git+https://github.com/Bakobiibizo/open-interpreter-jarvis.git@models", "q"],
            ["pip", "install", "-r", "requirements-whisper.txt", "-q", "--no-deps"],
            ["pip", "install", "-r", "requirements.txt", "-q"]
        ],
    "cuda-ubuntu2004":[
            ["sudo", "bash", "install/environment.sh"],
            ["sudo", "bash", "install/cuda-ubuntu2004.sh"],
        ],
    "cuda-ubuntu2204":[
            ["sudo", "bash", "install/environment.sh"],
            ["sudo", "bash", "install/cuda-ubuntu2204.sh"],
        ],
    "cuda-wsl": [
            ["sudo", "bash", "install/environment.sh"],
            ["sudo", "bash", "install/cuda-wsl.sh"],
        ],
    "cuda-windows": [
        ["choco install ffmpeg"],
        ["curl", "--proto", "'=https'", "--tlsv1.2", "-sSf", "https://sh.rustup.rs", "|", "sh"],
        []
    ]

}

logger.debug(f"\nsubprocesses - {subprocesses}\n")



@logger.catch
def main(selected_choice: str)-> None:
    """
    Runs the installer for the program.

    This function executes a series of subprocess commands to install and activate
    the environment, install a package, and run a Python script.

    Parameters:
        choice (str): The name of the package to install.

    Returns:
        None
    """

    subprocess.run(["sudo", "bash", "install/environment.sh"], check=True)

    
    subprocess.run(["pip", "install", "alive-progress", "-q"], check=True)
    from install.installer import run_installer
    
    # We send along the subprocesses dictionary for use in the installer
    run_installer(selected_choice, subprocesses, loguru)


def parseargs(options: List[str])-> argparse.Namespace:
    """
    Parses the command line arguments and returns the parsed arguments. Options available are no_cuda, cuda-wsl, cuda-ubuntu2004, and cuda-ubuntu2204. Select the appropriate cuda version for your operating system.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", choices=options, help="select what set of subprocess to run for instillation")
    return parser.parse_args()

if __name__ == "__main__":
    
    logger = init_logger()
    #Iterate through the keys of the subprocesses dictionary to get options for packages to install.
    selection_options = list(subprocesses.keys())
    
    args = parseargs(selection_options)
    choice = args.install
    
    if not choice:
        #Display the list of options with the index +1 for easy selection
        for i, selection_option in enumerate(selection_options):
            print(f"{i+1}: {selection_option}")

        #Its important that users select the correct CUDA option since rogue instillations of torch can break the installation.
        choice = input(f"Select what CUDA version you want to install 1-{len(selection_options)}: ")
        logger.debug(f"\nchoice - {choice}\n")
        choice = selection_options[int(choice)-1]
        logger.debug(f"selection_options - {selection_options}\nchoice - {choice}\n")
    main(choice)