from src.embeddings.ollama import embed_text
from src.storage.database import connect


def main():
    text = (
        "AI-A02 uses agent orchestration and "
        "architecture governance."
    )

    print("Generating embedding...")

    embedding = embed_text(text)

    print(f"Dimensions: {len(embedding)}")

    vector = "[" + ",".join(map(str, embedding)) + "]"

    print("Connecting to PostgreSQL...")

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
                SELECT
                    vector_dims(%s::vector),
                    %s::vector <=> %s::vector
                """,
            (vector, vector, vector),
        )

        dimensions, distance = cur.fetchone()

    print(f"Database vector dimensions: {dimensions}")
    print(f"Self cosine distance: {distance:.8f}")

    assert dimensions == 768
    assert abs(distance) < 0.00001

    print("Embedding/database integration passed.")


if __name__ == "__main__":
    main()
