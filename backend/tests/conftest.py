import pytest

from backend.app.indexing.models import CodeChunk
from backend.app.retrieval.models import SearchResult


@pytest.fixture
def make_result():

    def factory(
        chunk_id="chunk-1",
        file_path="calculator.py",
        symbol_name="add",
        start_line=1,
        end_line=2,
        code="def add(a, b):\n    return a + b",
        score=0.85
    ):

        # Construct a reusable search result
        chunk = CodeChunk(
            chunk_id=chunk_id,
            file_path=file_path,
            symbol_name=symbol_name,
            chunk_type="function",
            start_line=start_line,
            end_line=end_line,
            code=code,
            content_hash="test-hash"
        )

        return SearchResult(
            chunk=chunk,
            score=score
        )

    return factory