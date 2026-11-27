from dataclasses import dataclass


@dataclass
class RAGResponse:
    answer: str
    context: str
    retrieved_chunks: int
    relevant_chunks: int
    estimated_context_tokens: int
    retrieval_latency: float
    augmentation_latency: float
    generation_latency: float
    total_latency: float