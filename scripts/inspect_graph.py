from src.knowledge_graph.traverse import (
    load_graph,
    outgoing_relations,
)


def main():
    graph = load_graph()

    print("AI-A03 Architectural Knowledge Graph")
    print("=" * 60)

    print(f"Entities: {graph.number_of_nodes()}")
    print(f"Relationships: {graph.number_of_edges()}")

    print("\nAI-A02 architecture relationships")
    print("-" * 60)

    relations = outgoing_relations(graph, "project:AI-A02")

    for relation in relations:
        print(
            f"\nAI-A02 --{relation['relation_type']}--> "
            f"{relation['target']}"
        )

        print(f"Status: {relation['evidence_status']}")
        print(
            "Evidence: "
            f"{relation['repository']}/"
            f"{relation['file_path']}"
        )
        print(f"Quote: {relation['evidence_quote']}")

        if relation["git_commit"]:
            print(f"Git: {relation['git_commit'][:12]}")

    assert graph.number_of_nodes() == 6
    assert graph.number_of_edges() == 5
    assert len(relations) == 5

    print("\nGraph traversal validation passed.")


if __name__ == "__main__":
    main()
