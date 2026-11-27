import math

from ..retrieval.models import SearchResult


class ContextBuilder:

    def __init__(self, max_context_tokens: int = 2800):
        if max_context_tokens <= 0:
            raise ValueError("Context budget must be positive")

        self.max_context_tokens = max_context_tokens

    def estimate_tokens(self, text: str) -> int:
        # Estimate token consumption conservatively
        return math.ceil(len(text) / 3)

    def remove_redundant_chunks(
        self,
        results: list[SearchResult]
    ) -> list[SearchResult]:

        selected = []

        # Prioritize higher similarity scores
        ranked = sorted(
            results,
            key=lambda result: result.score,
            reverse=True
        )

        for result in ranked:
            chunk = result.chunk

            # Detect overlapping source ranges
            overlaps = any(
                existing.chunk.file_path == chunk.file_path
                and existing.chunk.start_line <= chunk.end_line
                and chunk.start_line <= existing.chunk.end_line
                for existing in selected
            )

            if not overlaps:
                selected.append(result)

        return selected

    def build(
        self,
        results: list[SearchResult]
    ) -> str:

        results = self.remove_redundant_chunks(results)

        sections = []

        for result in results:
            chunk = result.chunk

            # Include source metadata for citations
            section = (
                f"[Source {len(sections) + 1}]\n"
                f"File: {chunk.file_path}\n"
                f"Symbol: {chunk.symbol_name}\n"
                f"Lines: {chunk.start_line}-{chunk.end_line}\n"
                f"Code:\n{chunk.code}"
            )

            # Check the context budget
            candidate = "\n\n".join(sections + [section])

            if self.estimate_tokens(candidate) > self.max_context_tokens:
                continue

            sections.append(section)

        return "\n\n".join(sections)