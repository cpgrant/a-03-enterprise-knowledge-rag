from src.retrieval.cross_project import cross_project_search


def main():
    results = cross_project_search(
        a01_question=(
            "Why select LangGraph for agent orchestration?"
        ),
        a02_question=(
            "How is multi-agent orchestration implemented?"
        ),
    )

    expected = {
        (
            "AI-A01",
            "docs/adr/002-langgraph-orchestration.md",
        ),
        (
            "AI-A02",
            "docs/AI-A02-2-Orchestration-Guide.md",
        ),
    }

    found = {
        (result.source, result.file_path)
        for result in results
    }

    print("AI-A03 — Cross-Project Retrieval")
    print("=" * 65)

    for index, result in enumerate(results, 1):
        marker = " [EXPECTED]" if (
            result.source, result.file_path
        ) in expected else ""

        print(
            f"{index}. {result.source}/"
            f"{result.file_path}{marker}"
        )

    hits = len(expected & found)
    recall = hits / len(expected)

    print("\nQUESTION Q026")
    print(
        "How does A02 extend the agent-orchestration "
        "architecture described in A01?"
    )

    print(f"\nExpected documents found: {hits}/2")
    print(f"Recall@5: {recall:.2%}")

    assert len(results) <= 5
    assert len({r.source for r in results}) == 2
    assert expected <= found

    print("\nPASS: Balanced cross-project retrieval")


if __name__ == "__main__":
    main()
