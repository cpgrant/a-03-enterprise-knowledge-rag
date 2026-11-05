from __future__ import annotations

import networkx as nx

from src.storage.database import connect


def load_graph() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
                SELECT id, entity_key, entity_type, name
                FROM architecture_entities
                ORDER BY id
                """
        )

        for entity_id, key, entity_type, name in cur.fetchall():
            graph.add_node(
                key,
                id=entity_id,
                name=name,
                entity_type=entity_type,
            )

        cur.execute(
            """
                SELECT
                    r.id,
                    src.entity_key,
                    dst.entity_key,
                    r.relation_type,
                    r.properties->>'evidence_status',
                    r.properties->>'evidence_quote',
                    s.name,
                    d.file_path,
                    d.git_commit,
                    c.chunk_index
                FROM architecture_relations r
                JOIN architecture_entities src
                    ON src.id = r.source_entity_id
                JOIN architecture_entities dst
                    ON dst.id = r.target_entity_id
                LEFT JOIN documents d
                    ON d.id = r.evidence_document_id
                LEFT JOIN knowledge_sources s
                    ON s.id = d.source_id
                LEFT JOIN document_chunks c
                    ON c.id = r.evidence_chunk_id
                ORDER BY r.id
                """
        )

        for row in cur.fetchall():
            (
                relation_id,
                source_key,
                target_key,
                relation_type,
                status,
                quote,
                repository,
                file_path,
                git_commit,
                chunk_index,
            ) = row

            graph.add_edge(
                source_key,
                target_key,
                key=relation_id,
                relation_type=relation_type,
                evidence_status=status,
                evidence_quote=quote,
                repository=repository,
                file_path=file_path,
                git_commit=git_commit,
                chunk_index=chunk_index,
            )

    return graph


def outgoing_relations(
    graph: nx.MultiDiGraph,
    entity_key: str,
) -> list[dict]:
    if entity_key not in graph:
        return []

    results = []

    for _, target, _, data in graph.out_edges(
        entity_key, keys=True, data=True
    ):
        results.append({
            "target": graph.nodes[target]["name"],
            "target_key": target,
            **data,
        })

    return results
