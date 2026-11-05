# ADR-001 — PostgreSQL + pgvector

Date: 2026-11-05
Status: Accepted

## Context

AI-A03 requires persistent storage for documents, embeddings,
metadata, architectural entities, and relationships.

## Decision

Use PostgreSQL 17 with pgvector 0.8.7.

Use PostgreSQL full-text search for keyword retrieval.

Use cosine distance for vector similarity.

Store source provenance and graph relationships in PostgreSQL.

## Rationale

- Local-first deployment
- SQL and JSONB support
- Vector similarity search
- Integrated keyword retrieval
- Transactional consistency
- Alignment with AI-A01 architecture

## Consequences

A03 operates one primary database.

Vector index configuration will follow embedding model selection.

Graph traversal will initially use NetworkX.
