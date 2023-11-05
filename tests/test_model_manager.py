import pytest
import discordbot


@pytest.mark.parametrize(
    ("input", "expected_output_part"),
    (
        ("Say the word 'hi'", "hi"),
        ("Say the word 'ok'", "ok")
    ),
)
@pytest.mark.asyncio
async def test_llm_responses(input: str, expected_output_part: str) -> None:
    """Test from values."""
    result = await discordbot.predict(input, 0)
    assert expected_output_part in result.lower()


@pytest.mark.parametrize(
    ("input", "expected_output_part"),
    (
        ("Say the word 'hi'", "hi"),
        ("Repeat the words 'ok then'", "ok then")
    ),
)
@pytest.mark.asyncio
async def test_llm_responses_stream(input: str, expected_output_part: str) -> None:
    """Test from values."""
    result = []
    streaming = discordbot.predict_streaming(input)
    parts = 0
    async for part in streaming:
        parts = parts + 1
        result.append(part)

    resultString = ''.join(result)
    assert parts >= 2
    assert expected_output_part in resultString.lower()
