import whisper as whisper
import loguru
from whisper import DecodingResult

logger = loguru.logger

model = whisper.load_model("base")
logger.info("Model loaded.")

def transcribe(audio:str) -> str:
    """
    Transcribes the given audio using a pre-trained model.
    
    Parameters:
        audio (str): The path to the audio file to be transcribed.
        
    Returns:
        str: The transcribed text from the audio.
    """
    logger.info("Transcribing audio")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)

    logger.debug(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()

    result: DecodingResult = whisper.decode(model, mel, options)

    transcription: str = result.text

    logger.debug(f"\naudio - {audio}\nmel - {mel}\nprobs - {probs}\noptions - {options}\nresult - {result}\ntranscription - {transcription}")

    if not transcription:
        logger.exception(f"Could not transcribe audio: {audio}")

    return transcription

if __name__ == "__main__":
    print(transcribe("testing/test_file.wav"))