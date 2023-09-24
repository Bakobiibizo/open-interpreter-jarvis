import loguru
import os
from dotenv import load_dotenv
from interpreter import Interpreter
from src.get_api_keys import get_api_keys


load_dotenv()

logger = loguru.logger

api_key = os.environ["OPENAI_API_KEY"]

if not api_key:
    api_key = get_api_keys()[1]

class OpenInterpreter(Interpreter):
    api_key: str
    def __init__(self):
        super().__init__()
        self.api_key = api_key
        
interpreter = OpenInterpreter()

def get_interpreter():
    return interpreter


if __name__ == "__main__":
    get_interpreter()