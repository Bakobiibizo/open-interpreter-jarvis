import getpass
from typing import Tuple

def get_api_keys()-> Tuple[str, str]:
    

    
    #using this for debugging, if you uncomment it it will display your api keys so uncomment at your own risk.
    #logger.debug(f"\n{elevenlabs_api_key}\n{openai_api_key}")

    elevenlabs_api_key = getpass.getpass(prompt='Eleven Labs API Key: ', stream=None)
    
    openai_api_key = getpass.getpass(prompt='OpenAI API Key: ', stream=None)
    
    return elevenlabs_api_key, openai_api_key

