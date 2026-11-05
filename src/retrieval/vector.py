from __future__ import annotations

from dataclasses import dataclass

from src.embeddings.ollama import embed_text
from src.storage.database import connect


@dataclass(frozen=True)
class SearchResult:
    source: str
    file_path: str
    git_commit: str
    chunk_index: int
    content: str
    distance: float


def vector_search(
    query: str,
    limit: int = 5,
    source: str | None = None,
) -> list[SearchResult]:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    embedding = embed_text(query)
    vector = "[" + ",".join(map(str, embedding)) + "]"

    sql = """
        SELECT
            s.name,
            d.file_path,
            d.git_commit,
            c.chunk_index,
            c.content,
            c.embedding <=> %s::vector AS distance
        FROM document_chunks c
        JOIN documents d ON c.document_id = d.id
        JOIN knowledge_sources s ON d.source_id = s.id
        WHERE c.embedding IS NOT NULL
          AND (%s::text IS NULL OR s.name = %s::text)
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s
    """

    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (vector, source, source, vector, limit))
        rows = cur.fetchall()

    return [
        SearchResult(
            source=row[0],
            file_path=row[1],
            git_commit=row[2],
            chunk_index=row[3],
            content=row[4],
            distance=float(row[5]),
        )
        for row in rows
    ]
