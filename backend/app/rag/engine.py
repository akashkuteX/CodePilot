from time import perf_counter

from ..retrieval.persistent_search import PersistentSearchEngine
from ..llm.service import LLMService
from .context_builder import ContextBuilder
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

    def ask(
        self,
        query: str,
        top_k: int = 5
    ) -> RAGResponse:

        # Validate the question
        if not query.strip():
            raise ValueError("Query cannot be empty")

        start = perf_counter()

        # Retrieve candidate chunks
        retrieval_start = perf_counter()

        results = self.search_engine.search(
            query,
            top_k
        )

        retrieval_latency = (
            perf_counter() - retrieval_start
        )

        # Filter and construct context
        augmentation_start = perf_counter()

        relevant = [
            result for result in results
            if result.score >= self.min_similarity
        ]

        context = self.context_builder.build(relevant)

        estimated_tokens = (
            self.context_builder.estimate_tokens(context)
        )

        # Avoid unsupported generation
        if not context.strip():
            return RAGResponse(
                answer="Insufficient repository context to answer this question.",
                context="",
                retrieved_chunks=len(results),
                relevant_chunks=len(relevant),
                estimated_context_tokens=0,
                retrieval_latency=retrieval_latency,
                augmentation_latency=(
                    perf_counter() - augmentation_start
                ),
                generation_latency=0.0,
                total_latency=perf_counter() - start
            )

        # Construct the augmented prompt
        prompt = build_prompt(query, context)

        augmentation_latency = (
            perf_counter() - augmentation_start
        )

        # Generate a grounded response
        generation_start = perf_counter()

        answer = self.llm_service.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT
        )

        generation_latency = (
            perf_counter() - generation_start
        )

        # Return answer and performance metrics
        return RAGResponse(
            answer=answer,
            context=context,
            retrieved_chunks=len(results),
            relevant_chunks=len(relevant),
            estimated_context_tokens=estimated_tokens,
            retrieval_latency=retrieval_latency,
            augmentation_latency=augmentation_latency,
            generation_latency=generation_latency,
            total_latency=perf_counter() - start
        )