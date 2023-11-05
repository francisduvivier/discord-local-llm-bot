import os
from typing import List

import dotenv
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chat_models import ChatOllama

dotenv.load_dotenv()
MODEL_FALLBACK = 'mistral'
MODEL = os.getenv('MODEL') if os.getenv(
    'MODEL') else MODEL_FALLBACK

VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') is not None


def get_model(callbacks: List[BaseCallbackHandler] | None = None):
    callback_manager = None
    if callbacks is not None:
        callback_manager = CallbackManager(callbacks)
    chat_model = ChatOllama(
        model=MODEL,
        callback_manager=callback_manager,
        verbose=VERBOSE_DEBUG,
        streaming=True,
        stop=['[INST]']
    )
    return chat_model


if __name__ == "__main__":
    result = get_model(
    ).stream('Say hi')
    for chunk in result:
        print('chunk: ' + str(chunk.content))
