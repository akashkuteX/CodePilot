import pytest

from backend.app.rag.context_models import Source
from backend.app.rag.citation_validator import CitationValidator


@pytest.fixture
def sources():

    return [
        Source(1, "a.py", "add", 1, 10),
        Source(2, "b.py", "subtract", 1, 10)
    ]


def test_valid_citations(sources):

    validator = CitationValidator()

    report = validator.validate(
        "Addition [Source 1]. Subtraction [Source 2].",
        sources
    )

    assert report.valid_citations == [1, 2]
    assert report.invalid_citations == []
    assert report.has_citations is True


def test_invalid_citations(sources):

    validator = CitationValidator()

    report = validator.validate(
        "Addition [Source 1]. Multiplication [Source 99].",
        sources
    )

    assert report.valid_citations == [1]
    assert report.invalid_citations == [99]


def test_missing_citations(sources):

    validator = CitationValidator()

    report = validator.validate(
        "CodePilot uses Python.",
        sources
    )

    assert report.has_citations is False
    assert report.valid_citations == []
    assert report.invalid_citations == []


def test_duplicate_citations(sources):

    validator = CitationValidator()

    report = validator.validate(
        "Addition [Source 1] works [Source 1].",
        sources
    )

    assert report.valid_citations == [1]


def test_no_available_sources():

    validator = CitationValidator()

    report = validator.validate(
        "Some implementation [Source 1].",
        []
    )

    assert report.valid_citations == []
    assert report.invalid_citations == [1]