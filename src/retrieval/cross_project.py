from __future__ import annotations

from dataclasses import dataclass

from src.retrieval.vector import SearchResult, vector_search


@dataclass(frozen=True)
class CrossProjectResult:
    source: str
    file_path: str
    git_commit: str
    chunk_index: int
    content: str
    distance: float


def unique_documents(
    results: list[SearchResult],
    limit: int,
) -> list[CrossProjectResult]:
    documents = []
    seen = set()

    for result in results:
        key = (result.source, result.file_path)

        if key in seen:
            continue

        seen.add(key)

        documents.append(
            CrossProjectResult(
                source=result.source,
                file_path=result.file_path,
                git_commit=result.git_commit,
                chunk_index=result.chunk_index,
                content=result.content,
                distance=result.distance,
            )
        )

        if len(documents) >= limit:
            break

    return documents


def cross_project_search(
    a01_question: str,
    a02_question: str,
    a01_limit: int = 2,
    a02_limit: int = 3,
) -> list[CrossProjectResult]:
    if not a01_question.strip() or not a02_question.strip():
        raise ValueError("Both project questions are required")

    if not 1 <= a01_limit <= 5:
        raise ValueError("a01_limit must be between 1 and 5")

    if not 1 <= a02_limit <= 5:
        raise ValueError("a02_limit must be between 1 and 5")

    if a01_limit + a02_limit > 5:
        raise ValueError("Total document budget must not exceed 5")

    a01_results = vector_search(
        a01_question,
        limit=20,
        source="AI-A01",
    )

    a02_results = vector_search(
        a02_question,
        limit=20,
        source="AI-A02",
    )

    return (
        unique_documents(a01_results, a01_limit)
        + unique_documents(a02_results, a02_limit)
    )
