from backend.app.indexing.indexer import index_repository


def test_index_repository(tmp_path):
    # Create two source files
    (tmp_path / "auth.py").write_text(
        "def login():\n    return True"
    )

    (tmp_path / "payment.py").write_text(
        "def pay():\n    return True"
    )

    chunks = index_repository(str(tmp_path))

    assert len(chunks) == 2

    symbols = {chunk.symbol_name for chunk in chunks}

    assert symbols == {"login", "pay"}


def test_skip_invalid_python(tmp_path):
    # Create valid and invalid Python files
    (tmp_path / "valid.py").write_text(
        "def login():\n    return True"
    )

    (tmp_path / "invalid.py").write_text(
        "def broken("
    )

    chunks = index_repository(str(tmp_path))

    assert len(chunks) == 1
    assert chunks[0].symbol_name == "login"