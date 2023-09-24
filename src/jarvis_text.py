import gradio as gr
import interpreter

from src.get_api_keys import get_api_keys


def jarvis_text()-> None:
    """
    This function initializes a chatbot using the Jarvis library and launches a demo interface for interacting with the chatbot.
    
    Parameters:
    None
    
    Returns:
    None
    """
    
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):

        user_message = history[-1][0]
        history[-1][1] = ""
        active_block_type = ""

        for chunk in interpreter.chat(user_message, stream=True, display=False):

            # Message
            if "message" in chunk:
              if active_block_type != "message":
                active_block_type = "message"
              history[-1][1] += chunk["message"]
              yield history

            # Code
            if "language" in chunk:
              language = chunk["language"]
            if "code" in chunk:
              if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}\n"
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
            if "end_of_execution" in chunk:
              history[-1][1] = history[-1][1].strip()
              history[-1][1] += "\n```\n"
              yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

demo.queue()
demo.launch(debug=True)