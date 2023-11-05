import io
import os
from typing import Iterator

import dotenv
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema.messages import BaseMessageChunk
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from discordbot import ollama_config as model_config

dotenv.load_dotenv()
VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') is not None
DEBUG_STREAMING = os.getenv('DEBUG_STREAMING') is not None
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT') if os.getenv(
    'SYSTEM_PROMPT') else 'You are a funny bot on an awesome Maker Space Discord guild.'


def predict(question: str) -> str:
    # create stringbuffer
    string_buffer = io.StringIO()
    for chunk in stream(question):
        content = str(chunk.content)
        if VERBOSE_DEBUG and DEBUG_STREAMING: print(content, end='')
        string_buffer.write(content)
    print('\n Streaming finished.')
    return string_buffer.getvalue()


def stream(question: str) -> Iterator[BaseMessageChunk]:
    callbacks = None
    if VERBOSE_DEBUG:
        callbacks = [StreamingStdOutCallbackHandler()]
    llm = model_config.get_model(callbacks)
    prompt = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}'),
    ])
    return llm.stream(prompt.format(input=question, history=[]))


if __name__ == '__main__':
    print('full result:', predict('Write 5 original short lines of text about a topic of your liking.'))
