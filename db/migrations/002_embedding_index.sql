BEGIN;

ALTER TABLE document_chunks
    ALTER COLUMN embedding TYPE vector(768);

CREATE INDEX idx_chunks_embedding_hnsw
    ON document_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

COMMIT;
