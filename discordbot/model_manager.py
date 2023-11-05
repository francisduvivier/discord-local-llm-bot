import asyncio
import io
import os

import dotenv
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.callbacks import StreamingStdOutCallbackHandler

from discordbot import ollama_config as model_config

dotenv.load_dotenv()
VERBOSE_DEBUG = os.getenv('VERBOSE_DEBUG') is not None


async def predict(question):
    # create stringbuffer
    string_buffer = io.StringIO()
    async for token in predict_streaming(question):
        if VERBOSE_DEBUG: print('predicted token: ' + token)
        string_buffer.write(token)
    return string_buffer.getvalue()


async def apredict_with_errorlog(llm, question):
    print('apredict_with_errorlog call received')
    try:
        await llm.apredict(question)
    except Exception as e:
        print('EXCEPTION in predict')
        print(e)
    pass


def predict_streaming(question):
    print('predict_streaming called with question: ' + question)
    async_iterator = AsyncIteratorCallbackHandler()
    llm = model_config.get_model([
        StreamingStdOutCallbackHandler(),
        async_iterator,
    ])
    asyncio.create_task(apredict_with_errorlog(llm, question))
    return async_iterator.aiter()


if __name__ == '__main__':
    asyncio.run(predict('Answer with "Hello world"'))
