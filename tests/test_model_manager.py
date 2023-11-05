import pytest
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

    resultString = ''.join(result)
    assert parts >= 2
    assert expected_output_part in resultString.lower()
