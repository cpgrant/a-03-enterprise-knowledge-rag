import argparse

from src.retrieval.vector import vector_search


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Architecture question")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    results = vector_search(args.query, args.limit)

    if not results:
        print("No indexed knowledge found.")
        return

    print(f"\nQuestion: {args.query}")
    print("=" * 65)

    for rank, result in enumerate(results, 1):
        print(f"\nRESULT {rank}")
        print(f"Source: {result.source}")
        print(f"File: {result.file_path}")
        print(f"Git: {result.git_commit[:12]}")
        print(f"Chunk: {result.chunk_index}")
        print(f"Cosine distance: {result.distance:.4f}")
        print()
        print(result.content[:900])
        print("-" * 65)


if __name__ == "__main__":
    main()
