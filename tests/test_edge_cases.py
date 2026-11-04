"""Robustness: odd inputs must never crash and must return non-empty text."""
import pytest
from bot.bot import answer

INPUTS = {
    "empty": "",
    "whitespace": "   \n\t ",
    "very_long": "library " * 1500,
    "hindi": "पुस्तकालय कब खुलता है?",
    "emoji": "📚📚📚 hours???",
    "sql_like": "'; DROP TABLE books; --",
    "html_script": "<script>alert(1)</script> late fee?",
}


@pytest.mark.parametrize("name", INPUTS)
def test_edge_input_is_handled(name):
    reply = answer(INPUTS[name])
    assert isinstance(reply, str) and reply.strip(), "Empty or non-string reply"


def test_empty_input_asks_for_question():
    assert "question" in answer("").lower()
