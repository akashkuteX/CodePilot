import argparse

from backend.app.embeddings.service import EmbeddingService
from backend.app.storage.vector_repository import VectorRepository
from backend.app.retrieval.persistent_search import PersistentSearchEngine
from backend.app.rag.context_builder import ContextBuilder
from backend.app.rag.engine import RAGEngine
from backend.app.llm.service import LLMService


def display_response(response, show_metrics=False):

    # Display the generated answer
    print("\nCodePilot:")
    print(response.answer)

    # Display cited source locations
    cited_ids = set(response.citations.valid_citations)

    if cited_ids:
        print("\nSources:")

        for source in response.sources:
            if source.source_id in cited_ids:
                print(
                    f"[Source {source.source_id}] "
                    f"{source.file_path}:"
                    f"{source.start_line}-{source.end_line}"
                    f" ({source.symbol_name})"
                )

    # Warn about citation issues
    if response.citations.invalid_citations:
        print(
            "\nWARNING: Invalid citations:",
            response.citations.invalid_citations
        )

    elif response.sources and not response.citations.has_citations:
        print("\nNOTICE: Answer contains no citations.")

    # Display optional performance metrics
    if show_metrics:
        print("\nPerformance:")
        print("Retrieved:", response.retrieved_chunks)
        print("Relevant:", response.relevant_chunks)
        print("Included sources:", len(response.sources))
        print("Estimated tokens:", response.estimated_context_tokens)

        print(f"Retrieval: {response.retrieval_latency:.3f}s")
        print(f"Augmentation: {response.augmentation_latency:.3f}s")
        print(f"Generation: {response.generation_latency:.3f}s")
        print(f"Validation: {response.validation_latency:.6f}s")
        print(f"Total: {response.total_latency:.3f}s")


def interactive_chat(engine, top_k, show_metrics):

    print("\nCodePilot — Local AI Coding Assistant")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            # Read the next question
            query = input("You: ").strip()

            if query.lower() in {"exit", "quit"}:
                break

            if not query:
                continue

            # Execute the RAG pipeline
            response = engine.ask(query, top_k)

            display_response(response, show_metrics)

            print()

        except (KeyboardInterrupt, EOFError):
            break

        except RuntimeError as exc:
            print(f"\nError: {exc}\n")

    print("\nCodePilot session ended.")


def main():

    parser = argparse.ArgumentParser(
        description="CodePilot"
    )

    parser.add_argument(
        "command",
        choices=["index", "search", "count", "chat"]
    )

    parser.add_argument("--path", default=".")
    parser.add_argument("--query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--metrics", action="store_true")

    args = parser.parse_args()

    # Validate retrieval parameters
    if args.top_k <= 0:
        parser.error("--top-k must be positive")

    if args.command == "search" and not args.query:
        parser.error("--query is required for search")

    repository = VectorRepository()

    # Count without loading the embedding model
    if args.command == "count":
        print("Stored chunks:", repository.count())
        return

    # Initialize the retrieval pipeline
    embedding_service = EmbeddingService()

    search_engine = PersistentSearchEngine(
        embedding_service,
        repository
    )

    if args.command == "index":

        count = search_engine.index(args.path)
        print(f"Processed {count} chunks")

    elif args.command == "search":

        results = search_engine.search(
            args.query,
            args.top_k
        )

        for result in results:
            print("-" * 50)
            print("Symbol:", result.chunk.symbol_name)
            print("File:", result.chunk.file_path)
            print("Score:", round(result.score, 4))
            print("Code:\n", result.chunk.code)

    elif args.command == "chat":

        # Initialize the RAG pipeline
        engine = RAGEngine(
            search_engine,
            ContextBuilder(),
            LLMService()
        )

        if args.query:
            response = engine.ask(
                args.query,
                args.top_k
            )

            display_response(response, args.metrics)

        else:
            interactive_chat(
                engine,
                args.top_k,
                args.metrics
            )


if __name__ == "__main__":
    main()