import subprocess
from alive_progress import alive_it
from typing import Dict, List


def run_logger(loguru):
    logger = loguru.logger
    logger.opt(lazy=True, exception=True, colors=True)
    return logger



def install_packages(to_install: str, subprocesses: Dict[str, List[List[str]]], loguru)-> None:
    """
    Installs the specified packages. Options available are no_cuda, cuda-wsl, cuda-ubuntu2004, and cuda-ubuntu2204. Select the appropriate cuda version for your operating system.

    Args:
        to_install (str): The name of the package to install.

    Returns:
        None
    """
    logger = run_logger(loguru)
    logger.info("installing_packages")
    subp = subprocesses[to_install]
    
    progress_bar = alive_it(subp)

    print("Installing", to_install)
    print("Please wait...")
    
    try:
        for item in progress_bar:
            progress_bar.text(f"\nrunning {item}")
            subprocess.run(item, check=True)
    except ProcessLookupError:
        logger.exception("ProcessError: Review stack trace and variable values and try again.")
def run_installer(selected_packages: str, subprocess_dict: Dict[str, List[List[str]]], loguru)-> None:
    """
    A function that installs packages based on the input argument. Options available are no_cuda, cuda-wsl, cuda-ubuntu2004, and cuda-ubuntu2204. Select the appropriate cuda version for your operating system. All CUDA types get no_cuda first and then the correct version of torch is applied after all other instiliations. It is important to run the cuda bash scripts after the main instillation due to the CUDA version packaged with other libraries not being compatible with the CUDA version required by your system.

    Parameters:
        selected_packages (str): The name of the packages to be installed.

    Returns:
        None
    """
    logger = run_logger(loguru)
    logger.info("running_installer")
    install_packages("no_cuda", subprocess_dict, loguru)
    #see logger message
    logger.info("The warning about openai-whisper's requirements is normal and not an error. this is corrected in the next step which installs the requirements individually to allow users to select their cuda version. You can safely ignore that warning.")
    if selected_packages == "no_cuda":
        return
    install_packages(selected_packages, subprocess_dict, loguru)
    return

if __name__ == "__main__":
    logger = run_logger(loguru)
    logger.info("running installer.py")
    def run_from_install():
        """
        Instructs the user to run the program from the install.py file in the root directory of the repository. Since this file requires alive-progress and loguru before installing the requirements it needs to be done in a seperate script. 

        :return: A string indicating that the program should be run from the install.py file in the root directory of the repository.
        """
        if logger:
            logger.warning("please run this program from install.py in the root directory of the repository")
        print("please run this program from install.py in the root directory of the repository")
        return "please run this program from install.py in the root directory of the repository"    
    run_from_install()