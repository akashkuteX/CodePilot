import pytest
from unittest.mock import Mock

from backend.app.rag.engine import RAGEngine
from backend.app.rag.context_builder import ContextBuilder


@pytest.fixture
def rag_setup():

    # Mock external dependencies
    search_engine = Mock()
    llm_service = Mock()

    engine = RAGEngine(
        search_engine=search_engine,
        context_builder=ContextBuilder(),
        llm_service=llm_service,
        min_similarity=0.35
    )

    return engine, search_engine, llm_service


def test_successful_rag_response(rag_setup, make_result):

    engine, search, llm = rag_setup

    search.search.return_value = [make_result()]
    llm.generate.return_value = "Addition works [Source 1]."

    response = engine.ask("How does addition work?")

    assert response.answer == "Addition works [Source 1]."
    assert response.retrieved_chunks == 1
    assert response.relevant_chunks == 1
    assert len(response.sources) == 1
    assert response.citations.valid_citations == [1]

    search.search.assert_called_once_with(
        "How does addition work?", 5
    )

    llm.generate.assert_called_once()


def test_empty_retrieval(rag_setup):

    engine, search, llm = rag_setup

    search.search.return_value = []

    response = engine.ask("How does payment work?")

    assert "Insufficient" in response.answer
    assert response.sources == []
    assert response.generation_latency == 0.0

    # Verify unnecessary inference is avoided
    llm.generate.assert_not_called()


def test_relevance_filtering(rag_setup, make_result):

    engine, search, llm = rag_setup

    search.search.return_value = [
        make_result(file_path="a.py", score=0.85),
        make_result(file_path="b.py", score=0.20)
    ]

    llm.generate.return_value = "Answer [Source 1]."

    response = engine.ask("How does addition work?")

    assert response.retrieved_chunks == 2
    assert response.relevant_chunks == 1
    assert len(response.sources) == 1
    assert response.sources[0].file_path == "a.py"


def test_all_chunks_irrelevant(rag_setup, make_result):

    engine, search, llm = rag_setup

    search.search.return_value = [
        make_result(score=0.10)
    ]

    response = engine.ask("Unrelated question")

    assert response.relevant_chunks == 0
    assert "Insufficient" in response.answer

    llm.generate.assert_not_called()


def test_invalid_citation(rag_setup, make_result):

    engine, search, llm = rag_setup

    search.search.return_value = [make_result()]

    llm.generate.return_value = (
        "Answer [Source 1] and [Source 99]."
    )

    response = engine.ask("How does addition work?")

    assert response.citations.valid_citations == [1]
    assert response.citations.invalid_citations == [99]


def test_empty_query(rag_setup):

    engine, search, llm = rag_setup

    with pytest.raises(ValueError):
        engine.ask("   ")

    search.search.assert_not_called()
    llm.generate.assert_not_called()