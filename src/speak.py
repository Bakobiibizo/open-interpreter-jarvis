import time
from elevenlabs import generate, play
from typing import List
from src.get_audio_length import get_audio_length
def speak(text: str):
    """
    A function that speaks the given text using a specified voice.

    Parameters:
    - text (str): The text to be spoken.

    Returns:
    - None
    """
    speaking = True
    audio = generate(
      text=text,
      voice="Bella"
    )
    play(audio, notebook=True)

    audio_length = get_audio_length(audio_bytes=audio)
    time.sleep(audio_length)

if __name__ =="__main__":
    speak("Hello World")