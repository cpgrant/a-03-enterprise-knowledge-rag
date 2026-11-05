from __future__ import annotations

import argparse
import re
import subprocess

from src.chunking.structure import chunk_document
from src.embeddings.ollama import embed_text
from src.ingestion.discover import discover_documents
from src.storage.database import connect

SENSITIVE_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api_key|secret_key|access_token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"\b(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{12,}"),
]


def check_source(document):
    status = subprocess.check_output(
        ["git", "-C", str(document.repository), "status", "--porcelain"],
        text=True,
    )

    if status.strip():
        raise RuntimeError(
            f"Source repository is not clean: {document.repository}"
        )

    if any(pattern.search(document.content) for pattern in SENSITIVE_PATTERNS):
        raise RuntimeError(
            f"Potential sensitive content: {document.source_name}/{document.file_path}"
        )


def ingest(max_documents: int, dry_run: bool, scope: str = 'adr'):
    candidates = [
        doc for doc in discover_documents()
        if doc.document_type == "md"
        and (
            scope == "markdown"
            or "/adr/" in f"/{doc.file_path}"
        )
        and not (
            doc.source_name == "AI-A02"
            and doc.file_path.startswith("docs/prompts/")
        )
    ]

    candidates.sort(key=lambda d: (d.source_name, d.file_path))
    candidates = candidates[:max_documents]

    for doc in candidates:
        check_source(doc)

    print(f"Selected ADR documents: {len(candidates)}")

    if dry_run:
        for doc in candidates:
            chunks = chunk_document(doc)
            print(f"{doc.source_name}: {doc.file_path} — {len(chunks)} chunks")
        print("Dry run complete. No database changes.")
        return

    inserted = 0
    skipped = 0
    total_chunks = 0

    with connect() as conn:
        for doc in candidates:
            # Recheck source state immediately before processing.
            check_source(doc)

            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO knowledge_sources
                        (name, repository_path, git_commit)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        repository_path = EXCLUDED.repository_path,
                        git_commit = EXCLUDED.git_commit
                    RETURNING id
                    """,
                    (
                        doc.source_name,
                        str(doc.repository),
                        doc.git_commit,
                    ),
                )
                source_id = cur.fetchone()[0]

                cur.execute(
                    """
                    SELECT id, content_hash
                    FROM documents
                    WHERE source_id = %s AND file_path = %s
                    """,
                    (source_id, doc.file_path),
                )
                existing = cur.fetchone()

                if existing and existing[1] == doc.content_hash:
                    skipped += 1
                    conn.commit()
                    print(f"SKIP {doc.source_name}/{doc.file_path}")
                    continue

                chunks = chunk_document(doc)
                vectors = [embed_text(chunk.content) for chunk in chunks]

                cur.execute(
                    """
                    INSERT INTO documents
                        (source_id, file_path, content_hash,
                         git_commit, document_type)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (source_id, file_path)
                    DO UPDATE SET
                        content_hash = EXCLUDED.content_hash,
                        git_commit = EXCLUDED.git_commit,
                        document_type = EXCLUDED.document_type
                    RETURNING id
                    """,
                    (
                        source_id, doc.file_path,
                        doc.content_hash, doc.git_commit,
                        doc.document_type,
                    ),
                )
                document_id = cur.fetchone()[0]

                cur.execute(
                    "DELETE FROM document_chunks WHERE document_id = %s",
                    (document_id,),
                )

                for chunk, embedding in zip(chunks, vectors):
                    vector_text = "[" + ",".join(map(str, embedding)) + "]"

                    cur.execute(
                        """
                        INSERT INTO document_chunks
                            (document_id, chunk_index, content, embedding)
                        VALUES (%s, %s, %s, %s::vector)
                        """,
                        (
                            document_id,
                            chunk.chunk_index,
                            chunk.content,
                            vector_text,
                        ),
                    )

                conn.commit()
                inserted += 1
                total_chunks += len(chunks)

                print(
                    f"INDEXED {doc.source_name}/{doc.file_path} "
                    f"({len(chunks)} chunks)"
                )

    print(
        f"\nCompleted: {inserted} indexed, "
        f"{skipped} unchanged, {total_chunks} new chunks"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-documents", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--scope", choices=["adr", "markdown"], default="adr"
    )
    args = parser.parse_args()

    if args.max_documents < 1:
        parser.error("--max-documents must be positive")

    ingest(args.max_documents, args.dry_run, args.scope)


if __name__ == "__main__":
    main()
