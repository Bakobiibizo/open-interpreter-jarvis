import whisper as whisper

model = whisper.load_model("base")

def transcribe(audio):
    """
    Transcribes the given audio using a pre-trained model.
    
    Parameters:
        audio (str): The path to the audio file to be transcribed.
        
    Returns:
        str: The transcribed text from the audio.
    """
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

if __name__ == "__main__":
    print(transcribe("testing/test_file.wav"))