import pytest

from backend.app.indexing.scanner import scan_repository


def test_scan_python_files(tmp_path):
    # Create supported and unsupported files
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "README.md").write_text("Documentation")

    files = scan_repository(str(tmp_path))

    assert len(files) == 1
    assert files[0].name == "main.py"


def test_ignore_directories(tmp_path):
    # Create an ignored directory
    ignored = tmp_path / ".venv"
    ignored.mkdir()

    (ignored / "dependency.py").write_text("pass")
    (tmp_path / "main.py").write_text("pass")

    files = scan_repository(str(tmp_path))

    assert len(files) == 1
    assert files[0].name == "main.py"


def test_nested_directories(tmp_path):
    # Create a nested source file
    nested = tmp_path / "services"
    nested.mkdir()

    (nested / "auth.py").write_text("pass")

    files = scan_repository(str(tmp_path))

    assert len(files) == 1
    assert files[0].name == "auth.py"


def test_invalid_repository(tmp_path):
    # Reject a nonexistent repository
    with pytest.raises(ValueError):
        scan_repository(str(tmp_path / "missing"))


def test_empty_repository(tmp_path):
    assert scan_repository(str(tmp_path)) == []