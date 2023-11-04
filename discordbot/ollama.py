from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

chat_model = ChatOllama(
    model="mistral",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)


def get_answer(question, temperature=0.8):
    try:
        result = chat_model.predict(question, temperature=temperature)
        return result
    finally:
        pass
