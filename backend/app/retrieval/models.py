from dataclasses import dataclass
from ..indexing.models import CodeChunk


@dataclass
class EmbeddedChunk:
    chunk: CodeChunk
    embedding: list[float]


@dataclass
class SearchResult:
    chunk: CodeChunk
    score: float