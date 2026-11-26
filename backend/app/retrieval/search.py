from ..indexing.indexer import index_repository
from ..embeddings.service import EmbeddingService
from ..embeddings.similarity import dot_product
from .models import EmbeddedChunk, SearchResult


class SemanticSearchEngine:

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.embedded_chunks: list[EmbeddedChunk] = []

    def index(self, repo_path: str) -> int:
        # Extract code chunks
        chunks = index_repository(repo_path)

        # Generate embeddings in batches
        embeddings = self.embedding_service.embed_batch(
            [chunk.code for chunk in chunks]
        )

        # Associate chunks with their embeddings
        self.embedded_chunks = [
            EmbeddedChunk(chunk, embedding)
            for chunk, embedding in zip(chunks, embeddings)
        ]

        return len(self.embedded_chunks)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        if not query.strip():
            raise ValueError("Query cannot be empty")

        if not self.embedded_chunks:
            return []

        # Generate query embedding
        query_embedding = self.embedding_service.embed(query)

        results = []

        # Compare against stored embeddings
        for item in self.embedded_chunks:

            score = dot_product(
                query_embedding,
                item.embedding
            )

            results.append(
                SearchResult(item.chunk, score)
            )

        # Rank results by similarity
        results.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return results[:top_k]