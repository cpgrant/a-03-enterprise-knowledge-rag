from __future__ import annotations

import re
from dataclasses import dataclass

from src.storage.database import connect


@dataclass(frozen=True)
class KeywordResult:
    source: str
    file_path: str
    git_commit: str
    chunk_index: int
    content: str
    rank: float


def keyword_search(query: str, limit: int = 5) -> list[KeywordResult]:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    # Build a partial-match query using OR rather than
    # requiring every search term to appear.
    tokens = re.findall(r"[A-Za-z0-9_]+", query)

    # Remove common question words.
    stopwords = {
        "why", "what", "how", "when", "where",
        "was", "were", "is", "are", "the",
        "for", "from", "does", "did", "a", "an",
        "to", "of", "in", "and", "should",
    }

    terms = []
    for token in tokens:
        if token.lower() not in stopwords:
            terms.append(token)

    terms = list(dict.fromkeys(terms))[:12]

    if not terms:
        return []

    search_query = " OR ".join(terms)

    sql = """
        WITH q AS (
            SELECT websearch_to_tsquery(
                'english', %s
            ) AS query
        )
        SELECT
            s.name,
            d.file_path,
            d.git_commit,
            c.chunk_index,
            c.content,
            ts_rank_cd(
                to_tsvector('english', c.content),
                q.query
            ) AS rank
        FROM document_chunks c
        JOIN documents d ON c.document_id = d.id
        JOIN knowledge_sources s ON d.source_id = s.id
        CROSS JOIN q
        WHERE to_tsvector('english', c.content)
              @@ q.query
        ORDER BY rank DESC, c.id
        LIMIT %s
    """

    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (search_query, limit))
        rows = cur.fetchall()

    return [
        KeywordResult(
            source=row[0],
            file_path=row[1],
            git_commit=row[2],
            chunk_index=row[3],
            content=row[4],
            rank=float(row[5]),
        )
        for row in rows
    ]
