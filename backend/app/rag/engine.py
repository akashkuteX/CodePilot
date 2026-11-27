from time import perf_counter

from ..retrieval.persistent_search import PersistentSearchEngine
from ..llm.service import LLMService
from .context_builder import ContextBuilder
from .citation_validator import CitationValidator
from .prompts import SYSTEM_PROMPT, build_prompt
from .models import RAGResponse


class RAGEngine:

    def __init__(
        self,
        search_engine: PersistentSearchEngine,
        context_builder: ContextBuilder,
        llm_service: LLMService,
        min_similarity: float = 0.35
    ):
        self.search_engine = search_engine
        self.context_builder = context_builder
        self.llm_service = llm_service
        self.min_similarity = min_similarity
        self.citation_validator = CitationValidator()

    def ask(self, query: str, top_k: int = 5) -> RAGResponse:

        # Validate the question
        if not query.strip():
            raise ValueError("Query cannot be empty")

        start = perf_counter()

        # Retrieve candidate chunks
        retrieval_start = perf_counter()

        results = self.search_engine.search(query, top_k)

        retrieval_latency = perf_counter() - retrieval_start

        # Filter and construct context
        augmentation_start = perf_counter()

        relevant = [
            result for result in results
            if result.score >= self.min_similarity
        ]

        built_context = self.context_builder.build(relevant)

        context = built_context.text
        sources = built_context.sources

        estimated_tokens = (
            self.context_builder.estimate_tokens(context)
        )

        prompt = (
            build_prompt(query, context)
            if context.strip()
            else None
        )

        augmentation_latency = (
            perf_counter() - augmentation_start
        )

        # Generate only when context is available
        generation_latency = 0.0

        if prompt is None:
            answer = (
                "Insufficient repository context "
                "to answer this question."
            )
        else:
            generation_start = perf_counter()

            answer = self.llm_service.generate(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT
            )

            generation_latency = (
                perf_counter() - generation_start
            )

        # Validate generated citations
        validation_start = perf_counter()

        citations = self.citation_validator.validate(
            answer,
            sources
        )

        validation_latency = (
            perf_counter() - validation_start
        )

        # Return the complete response
        return RAGResponse(
            answer=answer,
            context=context,
            sources=sources,
            citations=citations,
            retrieved_chunks=len(results),
            relevant_chunks=len(relevant),
            estimated_context_tokens=estimated_tokens,
            retrieval_latency=retrieval_latency,
            augmentation_latency=augmentation_latency,
            generation_latency=generation_latency,
            validation_latency=validation_latency,
            total_latency=perf_counter() - start
        )