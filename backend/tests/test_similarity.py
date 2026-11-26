import pytest

from backend.app.embeddings.similarity import (
    cosine_similarity,
    dot_product
)


def test_identical_vectors():
    assert cosine_similarity([1, 0], [1, 0]) == 1


def test_orthogonal_vectors():
    assert cosine_similarity([1, 0], [0, 1]) == 0


def test_opposite_vectors():
    assert cosine_similarity([1, 0], [-1, 0]) == -1


def test_dimension_mismatch():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1, 2, 3])


def test_zero_vector():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 2])


def test_dot_product():
    assert dot_product([1, 2], [3, 4]) == 11


def test_normalized_vectors():
    a = [0.6, 0.8]
    b = [0.8, 0.6]

    assert cosine_similarity(a, b) == pytest.approx(
        dot_product(a, b)
    )