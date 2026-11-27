from dataclasses import dataclass

from .context_models import Source
from .citation_validator import CitationReport


@dataclass
class RAGResponse:
    answer: str
    context: str
    sources: list[Source]
    citations: CitationReport
    retrieved_chunks: int
    relevant_chunks: int
    estimated_context_tokens: int
    retrieval_latency: float
    augmentation_latency: float
    generation_latency: float
    validation_latency: float
    total_latency: float