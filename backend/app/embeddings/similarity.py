import math


def cosine_similarity(a, b):
    # Validate dimensions
    if len(a) != len(b):
        raise ValueError("Vector dimensions must match")

    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    # Reject zero vectors
    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Zero vectors are not supported")

    return dot_product / (magnitude_a * magnitude_b)


def dot_product(a, b):
    # Validate dimensions
    if len(a) != len(b):
        raise ValueError("Vector dimensions must match")

    return sum(x * y for x, y in zip(a, b))