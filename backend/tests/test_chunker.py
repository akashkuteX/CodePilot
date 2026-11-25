from backend.app.indexing.chunker import CodeChunker


def test_extract_function(tmp_path):
    source = "def add(a, b):\n    return a + b\n"

    file = tmp_path / "calculator.py"
    file.write_text(source)

    chunks = CodeChunker().chunk_file(file, tmp_path)

    assert len(chunks) == 1
    assert chunks[0].symbol_name == "add"
    assert chunks[0].chunk_type == "function"
    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 2
    assert chunks[0].code == source


def test_extract_class_and_method(tmp_path):
    source = """
class Calculator:
    def add(self, a, b):
        return a + b
"""

    file = tmp_path / "calculator.py"
    file.write_text(source)

    chunks = CodeChunker().chunk_file(file, tmp_path)

    assert len(chunks) == 2
    assert chunks[0].symbol_name == "Calculator"
    assert chunks[0].chunk_type == "class"
    assert chunks[1].symbol_name == "Calculator.add"
    assert chunks[1].chunk_type == "method"


def test_stable_chunk_id(tmp_path):
    file = tmp_path / "calculator.py"
    chunker = CodeChunker()

    file.write_text("def add(a, b):\n    return a + b")
    original = chunker.chunk_file(file, tmp_path)[0]

    # Modify the implementation
    file.write_text("def add(a, b):\n    return float(a + b)")
    modified = chunker.chunk_file(file, tmp_path)[0]

    assert original.chunk_id == modified.chunk_id
    assert original.content_hash != modified.content_hash


def test_async_function(tmp_path):
    file = tmp_path / "service.py"
    file.write_text("async def fetch():\n    return True")

    chunks = CodeChunker().chunk_file(file, tmp_path)

    assert len(chunks) == 1
    assert chunks[0].symbol_name == "fetch"


def test_decorated_function(tmp_path):
    file = tmp_path / "service.py"
    file.write_text("@cache\ndef fetch():\n    return True")

    chunks = CodeChunker().chunk_file(file, tmp_path)

    assert chunks[0].start_line == 1
    assert chunks[0].code.startswith("@cache")


def test_empty_file(tmp_path):
    file = tmp_path / "empty.py"
    file.write_text("")

    assert CodeChunker().chunk_file(file, tmp_path) == []