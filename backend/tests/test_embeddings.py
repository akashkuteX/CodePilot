import math
import pytest

from backend.app.embeddings.service import EmbeddingService


@pytest.fixture(scope="module")
def service():
    # Load the model once for all tests
    return EmbeddingService()


def test_embedding_dimensions(service):
    embedding = service.embed("Hello world")

    assert len(embedding) == 384


def test_normalized_embedding(service):
    embedding = service.embed("Hello world")

    magnitude = math.sqrt(
        sum(x * x for x in embedding)
    )

    assert magnitude == pytest.approx(1.0, abs=1e-6)


def test_batch_embeddings(service):
    embeddings = service.embed_batch(
        ["Authentication", "Database", "Payment"]
    )

    assert len(embeddings) == 3
    assert all(len(e) == 384 for e in embeddings)


def test_empty_batch(service):
    assert service.embed_batch([]) == []