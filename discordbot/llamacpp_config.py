import os
from typing import List

import dotenv

from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.llms.base import LLM
from langchain.llms import LlamaCpp

dotenv.load_dotenv()
MODELS_BASE_DIR = "/Users/fduvivier/.cache/lm-studio/models/"
model = "TheBloke/Yarn-Mistral-7B-64k-GGUF/yarn-mistral-7b-64k.Q8_0.gguf"
MODEL_PATH_FALLBACK = ("%s%s" % (MODELS_BASE_DIR, model))
MODEL_PATH = os.getenv('MODEL_PATH') if os.getenv(
    'MODEL_PATH') else MODEL_PATH_FALLBACK

VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') is not None


def get_model(callbacks: List[BaseCallbackHandler] | None = None) -> LLM:
    callback_manager = None
    if callbacks is not None:
        callback_manager = CallbackManager(callbacks)
    llm_model = LlamaCpp(
        model_path=MODEL_PATH,
        callback_manager=callback_manager,
        verbose=VERBOSE_DEBUG,
        streaming=True,
    )
    return llm_model


if __name__ == "__main__":
    from langchain.callbacks import StreamingStdOutCallbackHandler
    # TODO make this usable as a chat model
    import asyncio

    llama_cpp_model = get_model(callbacks=[StreamingStdOutCallbackHandler()])
    asyncio.run(llama_cpp_model.apredict('<HUMAN>Say hi\n<BOT>', temperature=0))
