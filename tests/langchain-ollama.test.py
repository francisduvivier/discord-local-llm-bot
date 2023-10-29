import pytest

def test_langchain_ollama_test_suite():
    async def get_answer(question):
        # Simulate the behavior of the getAnswer function
        return queryLLM(question)

    answer = pytest.mark.asyncio(get_answer)("Say hi?")

    assert isinstance(answer, str)
    assert "hi" in answer.lower()
