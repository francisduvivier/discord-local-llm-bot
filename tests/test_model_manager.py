import pytest
from langchain.schema import HumanMessage, AIMessage

from discordbot import model_manager


@pytest.mark.parametrize(
    ("input", "expected_output_part"),
    (
        ("Say the word 'hi'", "hi"),
        ("Say the word 'ok'", "ok")
    ),
)
def test_llm_responses(input: str, expected_output_part: str) -> None:
    """Test from values."""
    result = model_manager.predict(input)
    assert expected_output_part in result.lower()


@pytest.mark.parametrize(
    ("input", "expected_output_part"),
    (
        ("Say the word 'hi'", "hi"),
        ("Repeat the words 'ok then' one time.", "ok then")
    ),
)
def test_llm_responses_stream(input: str, expected_output_part: str) -> None:
    """Test from values."""
    result = []
    streaming = model_manager.stream(input)
    parts = 0
    for part in streaming:
        parts = parts + 1
        result.append(str(part.content))

    result_string = ''.join(result)
    assert parts >= 2
    assert expected_output_part in result_string.lower()


@pytest.mark.parametrize(
    ("repeat_word"),
    (
        ('hi'),
        ('elephant')
    ),
)
def test_llm_responses_stream_with_history(repeat_word: str) -> None:
    """Test from values."""
    result = []
    streaming = model_manager.stream('Ok be serious now and just answer now with the word I asked you to remember, nothing more.', [
        HumanMessage(content=f'Hi, please remember the word "{repeat_word}" for later reference.'),
        AIMessage(content=f'Ok, I will remember it.'),
    ])
    parts = 0
    for part in streaming:
        parts = parts + 1
        result.append(str(part.content))

    result_string = ''.join(result)
    assert parts >= 2
    assert repeat_word in result_string.lower()
