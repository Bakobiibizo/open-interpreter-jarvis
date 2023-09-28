eleven_labs_api_key = "<your_api_key>"
open_ai_api_key = "<your_api_key>"
import gradio as gr
import time
import interpreter

interpreter.api_key = open_ai_api_key
interpreter.auto_run = True
from elevenlabs import generate, play, set_api_key

set_api_key(eleven_labs_api_key)

import io
from pydub import AudioSegment

def get_audio_length(audio_bytes):
  # Create a BytesIO object from the byte array
  byte_io = io.BytesIO(audio_bytes)

  # Load the audio data with PyDub
  audio = AudioSegment.from_mp3(byte_io)

  # Get the length of the audio in milliseconds
  length_ms = len(audio)

  return length_ms / 1000.0

import whisper
model = whisper.load_model("base")

def speak(text):
  speaking = True
  audio = generate(
      text=text,
      voice="Bella"
  )
  play(audio, notebook=True)

  audio_length = get_audio_length(audio)
  time.sleep(audio_length)
  
  last_sentence = ""

with gr.Blocks() as demo:

    chatbot = gr.Chatbot()
    audio_input = gr.inputs.Audio(source="microphone", type="filepath")
    btn = gr.Button("Submit")

    def transcribe(audio):
      audio = whisper.load_audio(audio)
      audio = whisper.pad_or_trim(audio)
      mel = whisper.log_mel_spectrogram(audio).to(model.device)
      _, probs = model.detect_language(mel)
      options = whisper.DecodingOptions()
      result = whisper.decode(model, mel, options)
      return result.text

    def add_user_message(audio, history):
        user_message = transcribe(audio)
        return history + [[user_message, None]]

    def bot(history):
        global last_sentence

        user_message = history[-1][0]
        history[-1][1] = ""
        active_block_type = ""
        language = "" get_interpreter()
        for chunk in interpreter.chat(user_message, stream=True, display=False):

            # Message
            if "message" in chunk:
              if active_block_type != "message":
                active_block_type = "message"
              history[-1][1] += chunk["message"]

              last_sentence += chunk["message"]
              if any([punct in last_sentence for punct in ".?!\n"]):
                yield history
                speak(last_sentence)
                last_sentence = ""
              else:
                yield history

            # Code
            if "language" in chunk:
              language = chunk["language"]
            if "code" in chunk:
              if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}"
              history[-1][1] += chunk["code"]
              yield history

            # Output
            if "executing" in chunk:
              history[-1][1] += "\n```\n\n```text\n"
              yield history
            if "output" in chunk:
              if chunk["output"] != "KeyboardInterrupt":
                history[-1][1] += chunk["output"] + "\n"
                yield history
            if "active_line" in chunk and chunk["active_line"] == None:
              history[-1][1] = history[-1][1].strip()
              history[-1][1] += "\n```\n"
              yield history

        if last_sentence:
          speak(last_sentence)

    btn.click(add_user_message, [audio_input, chatbot], [chatbot]).then(
        bot, chatbot, chatbot
    )

demo.queue()
demo.launch(debug=True)