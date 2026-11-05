from dataclasses import dataclass

from psycopg.types.json import Jsonb

from src.storage.database import connect


@dataclass(frozen=True)
class GraphFact:
    file_path: str
    target_key: str
    target_name: str
    target_type: str
    relation_type: str
    evidence: str
    evidence_status: str


FACTS = [
    GraphFact(
        "docs/adr/ADR-003-a2a.md",
        "protocol:A2A", "A2A", "protocol",
        "SELECTS_PROTOCOL",
        "Use the A2A protocol across the remote agent boundary.",
        "accepted_decision",
    ),
    GraphFact(
        "docs/adr/ADR-003-a2a.md",
        "framework:LangGraph", "LangGraph", "framework",
        "SELECTS_FRAMEWORK",
        "Use native LangGraph calls for local specialist agents.",
        "accepted_decision",
    ),
    GraphFact(
        "docs/adr/ADR-006-governance-policy.md",
        "component:PythonPolicyEngine", "Python Policy Engine",
        "component", "IMPLEMENTS",
        "Implement an in-process Python policy engine integrated",
        "implementation_reported_in_adr",
    ),
    GraphFact(
        "docs/adr/ADR-005-implemented-state-observability.md",
        "component:JSONLogging", "JSON Logging",
        "component", "IMPLEMENTS",
        "Python standard-library JSON logging",
        "implementation_reported_in_adr",
    ),
    GraphFact(
        "docs/adr/ADR-005-implemented-state-observability.md",
        "component:InMemoryHistory", "In-Memory Execution History",
        "component", "IMPLEMENTS",
        "in-memory execution history",
        "implementation_reported_in_adr",
    ),
]


def upsert_entity(cur, key, name, entity_type):
    cur.execute(
        """
        INSERT INTO architecture_entities
            (entity_key, entity_type, name)
        VALUES (%s, %s, %s)
        ON CONFLICT (entity_key) DO UPDATE SET
            entity_type = EXCLUDED.entity_type,
            name = EXCLUDED.name
        RETURNING id
        """,
        (key, entity_type, name),
    )
    return cur.fetchone()[0]


def build():
    inserted = 0
    existing = 0

    with connect() as conn:
        with conn.cursor() as cur:
            for fact in FACTS:
                cur.execute(
                    """
                    SELECT d.id, c.id, c.content
                    FROM documents d
                    JOIN knowledge_sources s ON s.id = d.source_id
                    JOIN document_chunks c ON c.document_id = d.id
                    WHERE s.name = 'AI-A02'
                      AND d.file_path = %s
                    ORDER BY c.chunk_index
                    """,
                    (fact.file_path,),
                )

                match = next(
                    (
                        (doc_id, chunk_id)
                        for doc_id, chunk_id, content in cur.fetchall()
                        if fact.evidence in content
                    ),
                    None,
                )

                if match is None:
                    raise RuntimeError(
                        f"Evidence not found: {fact.file_path}: "
                        f"{fact.evidence}"
                    )

                document_id, chunk_id = match

                source_id = upsert_entity(
                    cur, "project:AI-A02", "AI-A02", "project"
                )
                target_id = upsert_entity(
                    cur, fact.target_key,
                    fact.target_name, fact.target_type
                )

                cur.execute(
                    """
                    SELECT id FROM architecture_relations
                    WHERE source_entity_id = %s
                      AND target_entity_id = %s
                      AND relation_type = %s
                      AND evidence_document_id = %s
                      AND evidence_chunk_id = %s
                    """,
                    (
                        source_id, target_id, fact.relation_type,
                        document_id, chunk_id,
                    ),
                )

                if cur.fetchone():
                    existing += 1
                    continue

                cur.execute(
                    """
                    INSERT INTO architecture_relations
                        (source_entity_id, target_entity_id,
                         relation_type, evidence_document_id,
                         evidence_chunk_id, properties)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        source_id,
                        target_id,
                        fact.relation_type,
                        document_id,
                        chunk_id,
                        Jsonb({
                            "evidence_quote": fact.evidence,
                            "evidence_status": fact.evidence_status,
                            "extraction_method": "deterministic_v1",
                        }),
                    ),
                )
                inserted += 1

        conn.commit()

    print(f"Relationships inserted: {inserted}")
    print(f"Relationships already present: {existing}")


if __name__ == "__main__":
    build()
