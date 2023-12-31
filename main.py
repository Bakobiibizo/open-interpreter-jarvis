import argparse
import subprocess
import loguru
from src.jarvis import jarvis
from src.jarvis_text import jarvis_text

logger = loguru.logger

def main(arguments: str)-> None:
    """
    A function that takes in an argument of type str and does something based on its value.
    
    Parameters:
        arguments (str): The argument passed to the function.
        
    Returns:
        None: This function does not return anything.
    """
    logger.info("Starting Jarvis")
    logger.debug(f"\narguments - {arguments}\n")
    subprocess.run(["sudo", "bash", "install/activate-environment.sh"], check=True)
    #if arguments == "text":
    #    jarvis_text()
    #else:
    try:
        jarvis()
    except RuntimeError as error:
        logger.exception(f"There was an error durring the runtime of Jarvis{error}")
        
def parseargs()-> argparse.Namespace:
    """
    Parse the command-line arguments and return the parsed arguments as a `argparse.Namespace` object.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    args = argparse.ArgumentParser()
    args.add_argument(
        "-m", "--mode", choices=["text", None], default=None, help="Select the mode jarvis operates in. Defaults to None for audio. If you want text only use 'text'.", required=False
    )
    
    return args.parse_args()

if __name__ == "__main__":
    parsed_args = parseargs()
    choice = parsed_args.mode
    main(choice)
        