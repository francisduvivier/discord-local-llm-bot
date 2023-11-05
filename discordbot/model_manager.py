import io
import os

import dotenv
from langchain.callbacks import StreamingStdOutCallbackHandler

from discordbot import ollama_config as model_config

dotenv.load_dotenv()
VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') is not None
DEBUG_STREAMING = os.getenv('DEBUG_STREAMING') is not None


def predict(question):
    # create stringbuffer
    string_buffer = io.StringIO()
    for chunk in stream(question):
        content = str(chunk.content)
        if VERBOSE_DEBUG and DEBUG_STREAMING: print(content, end='')
        string_buffer.write(content)
    print('\n Streaming finished.')
    return string_buffer.getvalue()


def stream(question):
    callbacks = None
    if VERBOSE_DEBUG:
        callbacks = [StreamingStdOutCallbackHandler()]
    llm = model_config.get_model(callbacks)
    return llm.stream(question)


if __name__ == '__main__':
    print('full result:', predict('Write 5 original short lines of text about a topic of your liking.'))
