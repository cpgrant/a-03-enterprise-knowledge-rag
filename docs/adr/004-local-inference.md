# ADR-004 — Local-First Embeddings and LLM Inference

Date: 2026-11-05
Status: Accepted

## Context

AI-A03 should operate locally without requiring
external model APIs.

Available infrastructure includes:

- Windows 11
- WSL2 Ubuntu
- NVIDIA RTX 4090
- Ollama
- Docker Desktop

## Decision

Use local embedding generation.

Use Ollama for answer generation.

Select embedding models based on retrieval quality,
embedding dimensions, latency, and resource usage.

## Rationale

- Data locality
- Reproducible experiments
- Controlled inference environment
- No mandatory external API costs
- Integration with existing AI projects

## Consequences

Model quality depends on locally available models.

GPU and system memory must be monitored.

Embedding model changes require re-embedding documents.
