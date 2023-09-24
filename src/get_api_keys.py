import os
import getpass
from dotenv import load_dotenv

load_dotenv()


def get_api_keys():
    """
    Retrieves the API keys required for accessing external services.

    This function retrieves the API keys required for accessing the Eleven Labs and OpenAI services. 
    It first checks if the environment variables 'ELEVENLABS_API_KEY' and 'OPENAI_API_KEY' are set. 
    If either of the keys is not set, the function prompts the user to enter the key manually. 

    Returns:
        - elevenlabs_api_key (str): The API key for Eleven Labs service.
        - openai_api_key (str): The API key for OpenAI service.
    """
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if elevenlabs_api_key is None:
        elevenlabs_api_key = getpass.getpass(prompt='Eleven Labs API Key: ', stream=None)
    
    if openai_api_key is None:
        openai_api_key = getpass.getpass(prompt='OpenAI API Key: ', stream=None)
    
    return elevenlabs_api_key, openai_api_key

