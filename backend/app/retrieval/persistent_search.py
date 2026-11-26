from ..indexing.indexer import index_repository
from ..embeddings.service import EmbeddingService
from ..storage.vector_repository import VectorRepository
from .models import EmbeddedChunk, SearchResult


class PersistentSearchEngine:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        repository: VectorRepository
    ):
        self.embedding_service = embedding_service
        self.repository = repository

    def index(self, repo_path: str) -> int:

        # Extract code chunks
        chunks = index_repository(repo_path)

        # Generate embeddings
        embeddings = self.embedding_service.embed_batch(
            [chunk.code for chunk in chunks]
        )

        # Associate chunks with embeddings
        embedded_chunks = [
            EmbeddedChunk(chunk, embedding)
            for chunk, embedding in zip(chunks, embeddings)
        ]

        # Persist chunks in PostgreSQL
        return self.repository.save_chunks(embedded_chunks)

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[SearchResult]:

        if not query.strip():
            raise ValueError("Query cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        # Generate query embedding
        query_embedding = self.embedding_service.embed(query)

        # Retrieve relevant chunks from PostgreSQL
        return self.repository.search(query_embedding, top_k)