import os
import loguru
from elevenlabs import set_api_key
from src.get_api_keys import get_api_keys

logger = loguru.logger

elevenlabs_api_key: str = os.environ["ELEVEN_LABS_API_KEY"]
def get_elevenlabs_api_key() -> str:
    eleven_labs_api_key = elevenlabs_api_key
    if not eleven_labs_api_key:
        logger.info("Eleven Labs API Key not set. Trying manual")

    #set elevenlabs api key
    if eleven_labs_api_key == "":
        eleven_labs_api_key = get_api_keys()[0]
    
    set_api_key(api_key=elevenlabs_api_key)
    
    if not elevenlabs_api_key:
       logger.exception("Eleven Labs API key was not set")
       
    return elevenlabs_api_key