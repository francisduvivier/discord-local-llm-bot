import io
import os

import dotenv
from typing import Iterator, List
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema.messages import BaseMessageChunk, HumanMessage, SystemMessage, BaseMessage
from langchain.globals import set_debug
from discordbot import ollama_config as model_config

dotenv.load_dotenv()
VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') == 'True'
DEBUG_STREAMING = os.getenv('DEBUG_STREAMING') is not None
BOT_TITLE = os.getenv('BOT_TITLE') if os.getenv('BOT_TITLE') else 'MakerMate, The Maker Space LLM Discord Bot'

set_debug(VERBOSE_DEBUG)


def predict(question: str) -> str:
    # create stringbuffer
    string_buffer = io.StringIO()
    for chunk in stream(question):
        content = str(chunk.content)
        if VERBOSE_DEBUG and DEBUG_STREAMING: print(content, end='')
        string_buffer.write(content)
    print('\n Streaming finished.')
    return string_buffer.getvalue()


def stream(question: str, message_history: List[BaseMessage] = None) -> Iterator[BaseMessageChunk]:
    callbacks = None
    if VERBOSE_DEBUG:
        callbacks = [StreamingStdOutCallbackHandler()]
    llm = model_config.get_model(callbacks)

    messages = [
    ]
    if message_history is not None and len(message_history) > 0:
        messages.extend(message_history)
    messages.append(HumanMessage(content=question))
    return llm.stream(messages, verbose=VERBOSE_DEBUG)


if __name__ == '__main__':
    print('full result:', predict('Write 5 original short lines of text about a topic of your liking.'))
