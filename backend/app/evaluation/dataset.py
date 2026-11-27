from dataclasses import dataclass, field


@dataclass
class EvaluationCase:

    case_id: str
    question: str
    expected_facts: list[list[str]] = field(default_factory=list)
    expected_symbols: list[str] = field(default_factory=list)
    should_abstain: bool = False


GOLDEN_DATASET = [

    EvaluationCase(
        case_id="eval-001",
        question="Which embedding model does CodePilot use?",
        expected_facts=[
            ["all-MiniLM-L6-v2"]
        ],
        expected_symbols=[
            "EmbeddingService.__init__"
        ]
    ),

    EvaluationCase(
        case_id="eval-002",
        question="How does CodePilot generate embeddings in batches?",
        expected_facts=[
            ["32"],
            ["normalize", "normalization", "normalized"]
        ],
        expected_symbols=[
            "EmbeddingService.embed_batch"
        ]
    ),

    EvaluationCase(
        case_id="eval-003",
        question="How does CodePilot remove redundant chunks?",
        expected_facts=[
            ["overlap", "overlapping"],
            ["file path", "file_path", "same file"],
            ["score", "rank", "similarity"]
        ],
        expected_symbols=[
            "ContextBuilder.remove_redundant_chunks"
        ]
    ),

    EvaluationCase(
        case_id="eval-004",
        question="How does CodePilot validate source citations?",
        expected_facts=[
            ["source id", "source identifier", "source number", "source_id"],
            ["invalid"],
            ["valid"]
        ],
        expected_symbols=[
            "CitationValidator.validate"
        ]
    ),

    EvaluationCase(
        case_id="eval-005",
        question="What happens when no relevant context is retrieved?",
        expected_facts=[
            ["insufficient"],
            ["skip", "not call", "does not call", "without calling"]
        ],
        expected_symbols=[
            "RAGEngine.ask"
        ]
    ),

    EvaluationCase(
        case_id="eval-006",
        question="Which payment gateway does CodePilot use?",
        should_abstain=True
    ),

    EvaluationCase(
        case_id="eval-007",
        question="How does CodePilot process cryptocurrency transactions?",
        should_abstain=True
    )
]