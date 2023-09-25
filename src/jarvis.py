import gradio as gr
import whisper as whisper
from src.open_interpreter_api import get_interpreter
from src.speak import speak


interpreter = get_interpreter()

with gr.Blocks() as demo:
    interpreter = get_interpreter()
    model = whisper.load_model("base")
    chatbot = gr.Chatbot()
    audio_input = gr.components.Audio(source="microphone", type="filepath")
    btn = gr.Button("Submit")

    def transcribe(audio):
      audio = whisper.load_audio(audio)
      audio = whisper.pad_or_trim(audio)
      mel = whisper.log_mel_spectrogram(audio).to(model.device)
      #TODO impliment automatic language detection
      #_, probs = model.detect_language(mel)
      options = whisper.DecodingOptions()
      result = whisper.decode(model, mel, options)
      return result.text

    def add_user_message(audio, history):
        user_message = transcribe(audio)
        return history + [[user_message, None]]

    def bot(history):
        user_message = history[-1][0]
        history[-1][1] = ""
        active_block_type = ""
        language = ""
        last_sentence = ""
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

def jarvis()-> None:
    demo.queue()
    demo.launch(debug=True)

    
if __name__ == '__main__':
    jarvis()