import re


def keyword_coverage(
    answer: str,
    expected_facts: list[list[str]]
) -> float | None:

    if not expected_facts:
        return None

    answer = answer.casefold()
    matched = 0

    # Match at least one alternative per expected fact
    for alternatives in expected_facts:

        if any(
            re.search(
                rf"(?<!\w){re.escape(term.casefold())}(?!\w)",
                answer
            )
            for term in alternatives
        ):
            matched += 1

    return matched / len(expected_facts)


def context_precision(
    actual_symbols: list[str],
    expected_symbols: list[str]
) -> float | None:

    if not expected_symbols:
        return None

    if not actual_symbols:
        return 0.0

    expected = set(expected_symbols)

    # Count chunks matching labelled symbols
    relevant = sum(
        symbol in expected
        for symbol in actual_symbols
    )

    return relevant / len(actual_symbols)


def context_recall(
    actual_symbols: list[str],
    expected_symbols: list[str]
) -> float | None:

    if not expected_symbols:
        return None

    actual = set(actual_symbols)
    expected = set(expected_symbols)

    # Measure coverage of expected symbols
    return len(actual & expected) / len(expected)


def citation_validity(
    valid_citations: list[int],
    invalid_citations: list[int]
) -> float | None:

    total = len(valid_citations) + len(invalid_citations)

    if total == 0:
        return None

    return len(valid_citations) / total


def detects_abstention(answer: str) -> bool:

    answer = answer.casefold()

    # Detect common insufficient-context responses
    phrases = [
        "insufficient",
        "not enough information",
        "cannot determine",
        "not provided",
        "not mentioned",
        "not available in the",
        "does not provide information"
    ]

    return any(phrase in answer for phrase in phrases)