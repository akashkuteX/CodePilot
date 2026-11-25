import ast
import hashlib
import tokenize
from pathlib import Path

from .models import CodeChunk


class CodeChunker:

    def generate_hash(self, content: str) -> str:
        # Generate a SHA-256 hash
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def chunk_file(
        self, file_path: Path, repo_path: Path
    ) -> list[CodeChunk]:

        # Read source using its declared encoding
        with tokenize.open(file_path) as file:
            source = file.read()

        # Parse source code into an AST
        tree = ast.parse(source)

        relative_path = file_path.relative_to(repo_path).as_posix()
        chunks = []
        lines = source.splitlines(keepends=True)

        # Extract a meaningful code block
        def extract(node, symbol_name, chunk_type):

            start_line = min(
                [node.lineno]
                + [d.lineno for d in node.decorator_list]
            )
            end_line = node.end_lineno

            code = "".join(lines[start_line - 1:end_line])

            chunk_id = self.generate_hash(
                f"{relative_path}:{chunk_type}:{symbol_name}"
            )

            chunk = CodeChunk(
                chunk_id=chunk_id,
                file_path=relative_path,
                symbol_name=symbol_name,
                chunk_type=chunk_type,
                start_line=start_line,
                end_line=end_line,
                code=code,
                content_hash=self.generate_hash(code)
            )

            chunks.append(chunk)

        # Process top-level functions and classes
        for node in tree.body:

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                extract(node, node.name, "function")

            elif isinstance(node, ast.ClassDef):
                extract(node, node.name, "class")

                # Extract methods with qualified names
                for child in node.body:
                    if isinstance(
                        child, (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        extract(
                            child,
                            f"{node.name}.{child.name}",
                            "method"
                        )

        return chunks