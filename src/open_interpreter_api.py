import loguru
from dotenv import load_dotenv
from interpreter.core.open_interpreter import OpenInterpreter


load_dotenv()

logger = loguru.logger
        
interpreter = OpenInterpreter()

def get_interpreter() -> OpenInterpreter:
    return interpreter


if __name__ == "__main__":
    get_interpreter()