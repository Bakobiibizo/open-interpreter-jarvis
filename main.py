import argparse
import subprocess
from src.JARVIS import jarvis
from src.JARVIS_text_only import jarvis_text


def main(arguments: str)-> None:
    """
    A function that takes in an argument of type str and does something based on its value.
    
    Parameters:
        arguments (str): The argument passed to the function.
        
    Returns:
        None: This function does not return anything.
    """
    subprocess.run(["sudo", "bash", "install/activate-environment.sh"], check=True)
    if arguments == "text":
        jarvis_text()
    else:
        jarvis()
        
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
        