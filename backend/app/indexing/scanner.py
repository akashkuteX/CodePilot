from pathlib import Path


SUPPORTED_EXTENSIONS = {".py"}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build"
}


def scan_repository(repo_path: str) -> list[Path]:
    root = Path(repo_path).resolve()
    files = []

    # Validate repository path
    if not root.is_dir():
        raise ValueError("Invalid repository path")

    # Traverse repository files
    for path in root.rglob("*"):

        # Skip ignored directories and their contents
        if any(
            part in IGNORED_DIRECTORIES
            for part in path.relative_to(root).parts
        ):
            continue

        # Collect supported source files
        if path.is_file() and not path.is_symlink():
            if path.suffix in SUPPORTED_EXTENSIONS:
                files.append(path)

    return sorted(files)


if __name__ == "__main__":
    files = scan_repository(".")

    for file in files:
        print(file)

    print(f"\nTotal files: {len(files)}")