BEGIN;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_sources (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    repository_path TEXT NOT NULL,
    git_commit TEXT,
    last_indexed_at TIMESTAMPTZ
);

CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL
        REFERENCES knowledge_sources(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    git_commit TEXT,
    document_type TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (source_id, file_path)
);

CREATE TABLE document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL
        REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    content TEXT NOT NULL,
    embedding VECTOR,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX idx_chunks_document
    ON document_chunks(document_id);

CREATE INDEX idx_chunks_fts
    ON document_chunks
    USING GIN (to_tsvector('english', content));

CREATE TABLE architecture_entities (
    id BIGSERIAL PRIMARY KEY,
    entity_key TEXT NOT NULL UNIQUE,
    entity_type TEXT NOT NULL,
    name TEXT NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE architecture_relations (
    id BIGSERIAL PRIMARY KEY,
    source_entity_id BIGINT NOT NULL
        REFERENCES architecture_entities(id) ON DELETE CASCADE,
    target_entity_id BIGINT NOT NULL
        REFERENCES architecture_entities(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    evidence_document_id BIGINT
        REFERENCES documents(id) ON DELETE SET NULL,
    evidence_chunk_id BIGINT
        REFERENCES document_chunks(id) ON DELETE SET NULL,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb,
    CHECK (source_entity_id <> target_entity_id)
);

CREATE INDEX idx_relations_source
    ON architecture_relations(source_entity_id);

CREATE INDEX idx_relations_target
    ON architecture_relations(target_entity_id);

CREATE INDEX idx_relations_evidence
    ON architecture_relations(evidence_document_id);

COMMIT;
