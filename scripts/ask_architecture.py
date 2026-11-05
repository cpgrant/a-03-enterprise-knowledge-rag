import argparse

from src.generation.answer import answer_architecture


def main():
    parser = argparse.ArgumentParser(
        description="Ask questions about enterprise AI architecture"
    )
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=4)

    args = parser.parse_args()

    result = answer_architecture(
        args.question,
        limit=args.limit,
    )

    print("\nAI-A03 — Architecture Intelligence")
    print("=" * 65)

    print("\nQUESTION")
    print(result.question)

    print("\nANSWER")
    print(result.answer)

    print("\nSOURCES")
    for source in result.sources:
        print(
            f"[{source['id']}] "
            f"{source['repository']}/"
            f"{source['file_path']}"
        )
        print(f"     Git: {source['git_commit'][:12]}")

    print("\nVALIDATION")
    print(f"Retrieved documents: {len(result.sources)}")
    print(f"Graph relationships: {result.graph_relationships}")
    print(f"Citation IDs valid: {result.citation_ids_valid}")
    print(f"Generation completed: {result.done_reason}")

    if not result.citation_ids_valid:
        print("WARNING: Missing or unknown citation identifiers.")

    if result.done_reason not in ("stop", "no_evidence"):
        print("WARNING: Answer may be incomplete.")


if __name__ == "__main__":
    main()
