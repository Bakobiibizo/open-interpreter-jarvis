import interpreter
from src.get_api_keys import get_api_keys

#set openai api keys
open_ai_api_key = get_api_keys()[1]

interpreter.api_key = open_ai_api_key
