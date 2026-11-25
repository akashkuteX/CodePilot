from pathlib import Path

from .scanner import scan_repository
from .chunker import CodeChunker
from .models import CodeChunk


def index_repository(repo_path: str) -> list[CodeChunk]:

    root = Path(repo_path).resolve()
    files = scan_repository(str(root))
    chunker = CodeChunker()
    all_chunks = []

    # Process every discovered source file
    for file in files:
        try:
            chunks = chunker.chunk_file(file, root)
            all_chunks.extend(chunks)

        except (SyntaxError, OSError, UnicodeError) as error:
            print(f"Skipping {file}: {error}")

    return all_chunks


if __name__ == "__main__":

    chunks = index_repository(".")

    # Display extracted chunk metadata
    for chunk in chunks:
        print(f"File: {chunk.file_path}")
        print(f"Symbol: {chunk.symbol_name}")
        print(f"Type: {chunk.chunk_type}")
        print(f"Lines: {chunk.start_line}-{chunk.end_line}")
        print(f"Hash: {chunk.content_hash[:12]}")
        print("-" * 40)

    print(f"\nTotal chunks: {len(chunks)}")