from src.knowledge_graph.multihop import find_evidence_path


def main():
    start = "protocol:A2A"
    end = "component:PythonPolicyEngine"

    path = find_evidence_path(start, end, max_hops=3)

    print("AI-A03 — Multi-Hop Architecture Graph")
    print("=" * 65)

    print("Question:")
    print("How are A2A and the policy engine connected?")

    print(f"\nGraph hops: {len(path)}")

    for index, step in enumerate(path, 1):
        print(f"\nHOP {index}")
        print(
            f"{step['source']} "
            f"--{step['relation']}--> "
            f"{step['target']}"
        )
        print(f"Status: {step['evidence_status']}")
        print(
            f"Evidence: {step['repository']}/"
            f"{step['file_path']}"
        )
        print(f"Quote: {step['evidence_quote']}")

    assert len(path) == 2

    evidence_files = {
        step["file_path"] for step in path
    }

    assert "docs/adr/ADR-003-a2a.md" in evidence_files
    assert "docs/adr/ADR-006-governance-policy.md" in evidence_files

    print("\nMulti-hop graph traversal passed.")


if __name__ == "__main__":
    main()
