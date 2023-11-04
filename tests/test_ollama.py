import pytest
import discordbot
@pytest.mark.parametrize(
    ("input", "expected_output_part"),
    (
        ("Say the word 'hi'", "hi"),
        ("Say the word 'ok'", "ok")
    ),
)
def test_llm_responses(input: str, expected_output_part: str) -> None:
    """Test from values."""
    assert expected_output_part in discordbot.get_answer(input, 0).lower()
