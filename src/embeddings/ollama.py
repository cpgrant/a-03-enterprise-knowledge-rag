import httpx

OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "embeddinggemma-2:270m"
EMBEDDING_DIMENSIONS = 768


def embed_text(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Cannot embed empty text")

    response = httpx.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
        timeout=120,
    )

    response.raise_for_status()

    embedding = response.json()["embeddings"][0]

    if len(embedding) != EMBEDDING_DIMENSIONS:
        raise ValueError(
            f"Expected {EMBEDDING_DIMENSIONS} dimensions, "
            f"received {len(embedding)}"
        )

    return embedding
