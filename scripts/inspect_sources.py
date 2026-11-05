from collections import Counter

from src.chunking.structure import chunk_document
from src.ingestion.discover import discover_documents


def main():
    documents = discover_documents()
    chunks = [
        chunk
        for document in documents
        for chunk in chunk_document(document)
    ]

    print("AI-A03 Knowledge Source Inspection")
    print("=" * 40)

    for source, count in sorted(
        Counter(d.source_name for d in documents).items()
    ):
        print(f"{source}: {count} documents")

    print(f"\nTotal documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    print("\nDocument types:")
    for extension, count in sorted(
        Counter(d.document_type for d in documents).items()
    ):
        print(f"  {extension}: {count}")

    print("\nSample chunks:")
    for chunk in chunks[:3]:
        print(
            f"\n[{chunk.source_name}] "
            f"{chunk.file_path} "
            f"chunk={chunk.chunk_index}"
        )
        print(chunk.content[:180].replace("\n", " "))


if __name__ == "__main__":
    main()
