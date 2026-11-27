from backend.app.rag.context_builder import ContextBuilder


def test_empty_context():

    builder = ContextBuilder()
    result = builder.build([])

    assert result.text == ""
    assert result.sources == []


def test_token_estimation():

    builder = ContextBuilder()

    assert builder.estimate_tokens("abcdef") == 2
    assert builder.estimate_tokens("abcd") == 2
    assert builder.estimate_tokens("") == 0


def test_overlapping_chunks(make_result):

    builder = ContextBuilder()

    first = make_result(
        chunk_id="1",
        start_line=1,
        end_line=10,
        score=0.90
    )

    second = make_result(
        chunk_id="2",
        start_line=5,
        end_line=8,
        score=0.70
    )

    # Keep the higher-ranked overlapping chunk
    results = builder.remove_redundant_chunks(
        [second, first]
    )

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "1"


def test_different_files(make_result):

    builder = ContextBuilder()

    first = make_result(file_path="a.py")
    second = make_result(file_path="b.py")

    results = builder.remove_redundant_chunks(
        [first, second]
    )

    assert len(results) == 2


def test_context_budget(make_result):

    builder = ContextBuilder(max_context_tokens=100)

    result = make_result(code="x" * 1000)

    context = builder.build([result])

    assert context.text == ""
    assert context.sources == []


def test_source_metadata(make_result):

    builder = ContextBuilder()

    context = builder.build([make_result()])

    assert len(context.sources) == 1
    assert context.sources[0].source_id == 1
    assert context.sources[0].file_path == "calculator.py"
    assert "[Source 1]" in context.text


def test_skip_oversized_chunk(make_result):

    builder = ContextBuilder(max_context_tokens=100)

    large = make_result(
        file_path="large.py",
        code="x" * 1000,
        score=0.95
    )

    small = make_result(
        file_path="small.py",
        score=0.80
    )

    # Accept smaller chunks after oversized ones
    context = builder.build([large, small])

    assert len(context.sources) == 1
    assert context.sources[0].file_path == "small.py"
    assert context.sources[0].source_id == 1
    assert builder.estimate_tokens(context.text) <= 100