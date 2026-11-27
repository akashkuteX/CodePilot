import pytest

from backend.app.rag.prompts import build_prompt


def test_prompt_format():

    query = "How does add work?"
    context = "def add(a, b): return a + b"

    prompt = build_prompt(query, context)

    assert query in prompt
    assert context in prompt
    assert "<retrieved_context>" in prompt
    assert "</retrieved_context>" in prompt
    assert "<user_question>" in prompt
    assert "</user_question>" in prompt


def test_empty_query():

    with pytest.raises(ValueError):
        build_prompt("", "Some source code")


def test_empty_context():

    with pytest.raises(ValueError):
        build_prompt("How does it work?", "")