import math

from ..retrieval.models import SearchResult
from .context_models import Source, BuiltContext


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

    def build(self, results: list[SearchResult]) -> BuiltContext:

        results = self.remove_redundant_chunks(results)

        sections = []
        sources = []

        for result in results:
            chunk = result.chunk
            source_id = len(sections) + 1

            # Format the source context
            section = (
                f"[Source {source_id}]\n"
                f"File: {chunk.file_path}\n"
                f"Symbol: {chunk.symbol_name}\n"
                f"Lines: {chunk.start_line}-{chunk.end_line}\n"
                f"Code:\n{chunk.code}"
            )

            candidate = "\n\n".join(sections + [section])

            # Enforce the estimated context budget
            if self.estimate_tokens(candidate) > self.max_context_tokens:
                continue

            sections.append(section)

            # Store trusted source metadata
            sources.append(
                Source(
                    source_id=source_id,
                    file_path=chunk.file_path,
                    symbol_name=chunk.symbol_name,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line
                )
            )

        return BuiltContext(
            text="\n\n".join(sections),
            sources=sources
        )