import time
import loguru
from typing import List
from elevenlabs import generate, play

from src.get_audio_length import get_audio_length



logger = loguru.logger

def speak(text: str)-> None:
    """
    A function that speaks the given text using a specified voice.

    Parameters:
        - text (str): The text to be spoken.

    Returns:
    - None
    """
    logger.info("speaking")
    audio = generate(
      text=text,
      voice="Bella"
    )
    play(audio, notebook=True)

    audio_length = get_audio_length(audio_bytes=audio)
    
    logger.debug(audio_length)
    
    time.sleep(audio_length)

if __name__ =="__main__":
    speak("Hello World")