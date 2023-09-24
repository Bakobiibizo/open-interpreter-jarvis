import io
from pydub import AudioSegment

def get_audio_length(audio_bytes: bytes) -> float:
    """
    Calculate the length of an audio file.

    Parameters:
    - audio_bytes (bytes): A byte array containing the audio data.

    Returns:
    - length_s (float): The length of the audio file in seconds.
    """
    # Create a BytesIO object from the byte array
    byte_io = io.BytesIO(audio_bytes)

    # Load the audio data with PyDub
    audio: AudioSegment = AudioSegment.from_mp3(byte_io)

    # Get the length of the audio in milliseconds
    length_ms: int = len(audio)

    # Optionally convert to seconds
    length_s: float = length_ms / 1000.0

    return length_s
