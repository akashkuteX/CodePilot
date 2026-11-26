import argparse

from backend.app.embeddings.service import EmbeddingService
from backend.app.storage.vector_repository import VectorRepository
from backend.app.retrieval.persistent_search import PersistentSearchEngine


def main():

    # Configure command-line arguments
    parser = argparse.ArgumentParser(description="CodePilot")

    parser.add_argument(
        "command",
        choices=["index", "search", "count"]
    )

    parser.add_argument("--path", default=".")
    parser.add_argument("--query")
    parser.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args()

    repository = VectorRepository()

    # Count chunks without loading the model
    if args.command == "count":
        print("Stored chunks:", repository.count())
        return

    if args.command == "search" and not args.query:
        parser.error("--query is required for search")

    service = EmbeddingService()
    engine = PersistentSearchEngine(service, repository)

    if args.command == "index":
        count = engine.index(args.path)
        print(f"Processed {count} chunks")

    elif args.command == "search":

        results = engine.search(args.query, args.top_k)

        for result in results:
            print("-" * 50)
            print("Symbol:", result.chunk.symbol_name)
            print("File:", result.chunk.file_path)
            print("Score:", round(result.score, 4))
            print("Code:\n", result.chunk.code)


if __name__ == "__main__":
    main()