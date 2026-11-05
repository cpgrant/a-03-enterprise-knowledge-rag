import argparse

from src.retrieval.graphrag import graphrag_search


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    passages, relationships = graphrag_search(
        args.query,
        limit=args.limit,
    )

    print("\nAI-A03 — Graph-Enhanced Retrieval")
    print("=" * 65)
    print("Question:", args.query)

    print("\nHYBRID RETRIEVAL")
    print("-" * 65)

    for rank, result in enumerate(passages, 1):
        print(
            f"{rank}. [{result.source}] {result.file_path}"
        )
        print(
            f"   RRF={result.rrf_score:.5f} "
            f"Methods={result.retrieval_methods}"
        )

    print("\nSOURCE-GROUNDED GRAPH RELATIONSHIPS")
    print("-" * 65)

    for relation in relationships:
        print(
            f"\n{relation.source_entity} "
            f"--{relation.relation_type}--> "
            f"{relation.target_entity}"
        )
        print(f"Status: {relation.evidence_status}")
        print(
            f"Evidence: {relation.repository}/"
            f"{relation.file_path}"
        )
        print(f"Git: {relation.git_commit[:12]}")
        print(f"Quote: {relation.evidence_quote}")

    print("\nSUMMARY")
    print(f"Retrieved passages: {len(passages)}")
    print(f"Graph relationships: {len(relationships)}")


if __name__ == "__main__":
    main()
