from __future__ import annotations

from dataclasses import dataclass, field

from src.retrieval.keyword import keyword_search
from src.retrieval.vector import vector_search


@dataclass
class HybridResult:
    source: str
    file_path: str
    git_commit: str
    chunk_index: int
    content: str
    rrf_score: float = 0.0
    retrieval_methods: list[str] = field(default_factory=list)


def hybrid_search(
    query: str,
    limit: int = 5,
    rrf_k: int = 60,
    source: str | None = None,
) -> list[HybridResult]:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    if rrf_k < 1:
        raise ValueError("rrf_k must be positive")

    candidate_limit = 20

    vector_results = vector_search(query, candidate_limit, source=source)
    keyword_results = keyword_search(query, candidate_limit, source=source)

    combined = {}

    for method, results in (
        ("vector", vector_results),
        ("keyword", keyword_results),
    ):
        for rank, result in enumerate(results, start=1):
            key = (
                result.source,
                result.file_path,
                result.git_commit,
                result.chunk_index,
            )

            if key not in combined:
                combined[key] = HybridResult(
                    source=result.source,
                    file_path=result.file_path,
                    git_commit=result.git_commit,
                    chunk_index=result.chunk_index,
                    content=result.content,
                )

            item = combined[key]
            item.rrf_score += 1.0 / (rrf_k + rank)
            item.retrieval_methods.append(method)

    return sorted(
        combined.values(),
        key=lambda item: (
            -item.rrf_score,
            item.source,
            item.file_path,
            item.chunk_index,
        ),
    )[:limit]
