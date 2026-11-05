from __future__ import annotations

from dataclasses import dataclass

from src.ingestion.discover import SourceDocument


@dataclass(frozen=True)
class KnowledgeChunk:
    source_name: str
    file_path: str
    git_commit: str
    content_hash: str
    chunk_index: int
    content: str


def chunk_document(
    document: SourceDocument,
    max_chars: int = 2400,
    overlap_lines: int = 3,
) -> list[KnowledgeChunk]:
    lines = document.content.splitlines()

    chunks = []
    current = []
    current_length = 0

    def emit():
        if current:
            text = "\n".join(current).strip()
            if text:
                chunks.append(text)

    for line in lines:
        if current and current_length + len(line) + 1 > max_chars:
            emit()
            current = current[-overlap_lines:] if overlap_lines else []
            current_length = sum(len(x) + 1 for x in current)

        current.append(line)
        current_length += len(line) + 1

    emit()

    return [
        KnowledgeChunk(
            source_name=document.source_name,
            file_path=document.file_path,
            git_commit=document.git_commit,
            content_hash=document.content_hash,
            chunk_index=index,
            content=text,
        )
        for index, text in enumerate(chunks)
    ]
