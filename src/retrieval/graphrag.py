from __future__ import annotations

from dataclasses import dataclass

from src.knowledge_graph.traverse import load_graph
from src.retrieval.hybrid import hybrid_search


@dataclass(frozen=True)
class GraphEvidence:
    source_entity: str
    relation_type: str
    target_entity: str
    evidence_status: str
    repository: str
    file_path: str
    git_commit: str
    evidence_quote: str


def graphrag_search(query: str, limit: int = 5):
    # Stage 1: retrieve relevant documents.
    passages = hybrid_search(query, limit=limit)

    # Stage 2: load architecture relationships.
    graph = load_graph()

    # Link the retrieved documents to graph evidence.
    retrieved_sources = {
        (p.source, p.file_path, p.git_commit)
        for p in passages
    }

    relationships = []

    for source_key, target_key, data in graph.edges(data=True):
        evidence_key = (
            data.get("repository"),
            data.get("file_path"),
            data.get("git_commit"),
        )

        if evidence_key not in retrieved_sources:
            continue

        relationships.append(
            GraphEvidence(
                source_entity=graph.nodes[source_key]["name"],
                relation_type=data["relation_type"],
                target_entity=graph.nodes[target_key]["name"],
                evidence_status=data.get("evidence_status") or "",
                repository=data.get("repository") or "",
                file_path=data.get("file_path") or "",
                git_commit=data.get("git_commit") or "",
                evidence_quote=data.get("evidence_quote") or "",
            )
        )

    relationships.sort(
        key=lambda r: (
            r.file_path,
            r.relation_type,
            r.target_entity,
        )
    )

    return passages, relationships
