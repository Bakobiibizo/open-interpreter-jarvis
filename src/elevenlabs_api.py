from elevenlabs import set_api_key
from src.get_api_keys import get_api_keys

#set elevenlabs api key
elevenlabs_api_key = get_api_keys()[0]
set_api_key(elevenlabs_api_key)