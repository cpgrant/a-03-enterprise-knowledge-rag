from __future__ import annotations

from itertools import pairwise

import networkx as nx

from src.knowledge_graph.traverse import load_graph


def find_evidence_path(
    start_key: str,
    end_key: str,
    max_hops: int = 3,
) -> list[dict]:
    graph = load_graph()

    if start_key not in graph or end_key not in graph:
        return []

    # Undirected traversal is used for discovering
    # connections. Original edge direction is retained.
    undirected = graph.to_undirected()

    try:
        path = nx.shortest_path(
            undirected, start_key, end_key
        )
    except nx.NetworkXNoPath:
        return []

    if len(path) - 1 > max_hops:
        return []

    evidence_path = []

    for source_key, target_key in pairwise(path):
        forward = graph.get_edge_data(source_key, target_key)
        reverse = graph.get_edge_data(target_key, source_key)

        if forward:
            edge = next(iter(forward.values()))
            actual_source = source_key
            actual_target = target_key
        elif reverse:
            edge = next(iter(reverse.values()))
            actual_source = target_key
            actual_target = source_key
        else:
            raise RuntimeError("Graph path contains missing edge")

        evidence_path.append({
            "source": graph.nodes[actual_source]["name"],
            "relation": edge["relation_type"],
            "target": graph.nodes[actual_target]["name"],
            "evidence_status": edge.get("evidence_status"),
            "repository": edge.get("repository"),
            "file_path": edge.get("file_path"),
            "git_commit": edge.get("git_commit"),
            "evidence_quote": edge.get("evidence_quote"),
        })

    return evidence_path
