# ADR-002 — Hybrid RAG and GraphRAG

Date: 2026-11-05
Status: Accepted

## Context

Architecture questions require both document retrieval
and relationship-based reasoning.

## Decision

Implement three retrieval strategies:

1. Vector similarity search
2. Hybrid vector and keyword search
3. Graph-enhanced retrieval

Use Reciprocal Rank Fusion for hybrid ranking.

Compare retrieval quality with a fixed evaluation dataset.

## Rationale

Vector retrieval supports semantic similarity.

Keyword retrieval improves exact identifier matching.

Graph traversal supports dependency and multi-hop questions.

## Consequences

Retrieval complexity increases.

All strategies must be evaluated on the same source corpus.

Graph retrieval must return supporting source evidence.
