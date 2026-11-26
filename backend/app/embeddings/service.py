from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load the embedding model
        self.model = SentenceTransformer(model_name)

        self.dimensions = self.model.get_embedding_dimension()

    def embed(self, text: str) -> list[float]:
        # Generate a single normalized embedding
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # Handle empty input
        if not texts:
            return []

        # Generate embeddings in batches
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True
        )

        return embeddings.tolist()