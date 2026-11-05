# AI-A03 — Implementation and Operations Guide

**Project:** Enterprise Knowledge Intelligence  
**Architecture:** Hybrid RAG · GraphRAG · Architecture Intelligence  
**Status:** Validated local proof of concept

## 1. Purpose

AI-A03 provides a local-first enterprise knowledge intelligence architecture that retrieves, connects, and reasons over versioned architecture documentation.

The system combines semantic search, full-text search, a source-grounded architectural knowledge graph, and local LLM inference.

It uses AI-A01 and AI-A02 as read-only architectural knowledge sources.

## 2. System Architecture

The system has six principal layers:

1. **Source Layer:** Git repositories containing architectural documents and decisions.
2. **Ingestion Layer:** Source discovery, document selection, content hashing, chunking, and embeddings.
3. **Knowledge Storage:** PostgreSQL, pgvector, full-text search, architectural entities, and relationships.
4. **Retrieval Layer:** Vector retrieval, keyword search, Reciprocal Rank Fusion, and repository-aware retrieval.
5. **Intelligence Layer:** Graph traversal, retrieval augmentation, and evidence-grounded answer generation.
6. **Validation Layer:** Automated testing, retrieval benchmarking, and answer-safety checks.

## 3. Knowledge Sources and Ingestion

The prototype ingests approved Markdown architecture documents from two repositories:

| Repository | Documents | Chunks |
|---|---:|---:|
| AI-A01 | 9 | 12 |
| AI-A02 | 17 | 55 |
| **Total** | **26** | **67** |

The source ingestion process maintains repository information and Git provenance, allowing retrieved evidence to be traced to source documents.

Documents are divided into chunks and converted into 768-dimensional embeddings using the Ollama model `embeddinggemma-2:270m`.

## 4. Data and Knowledge Storage

PostgreSQL 17 with pgvector 0.8.7 provides persistent storage for documents, chunks, embeddings, architectural entities, and relationships.

The architectural knowledge graph currently contains:

- 6 entities.
- 5 evidence-backed relationships.
- Source provenance associated with architectural decisions.

NetworkX supports graph traversal and evidence path exploration.

## 5. Retrieval Architecture

AI-A03 implements three retrieval strategies.

**Vector retrieval:** Semantic similarity using stored embeddings.

**Keyword retrieval:** PostgreSQL full-text search.

**Hybrid retrieval:** Reciprocal Rank Fusion combines vector and keyword rankings.

Repository-specific filtering allows retrieval to focus on AI-A01 or AI-A02.

For cross-project comparisons, the prototype supports manually formulated subquestions with balanced retrieval across repositories.

## 6. GraphRAG and Architectural Reasoning

The graph-enrichment mechanism connects retrieved architectural evidence with known entities and relationships.

Supported functionality includes:

- Evidence-backed architectural relationships.
- Graph traversal.
- Two-hop path exploration.
- Graph-enhanced retrieval.
- Architectural question answering with source references.

The current graph is curated and limited in size; it is not an automatically extracted enterprise-wide knowledge graph.

## 7. Answer Generation

AI-A03 uses local Ollama inference with `granite4.2:8b`.

Retrieved source passages are supplied to the model for generating architecture answers.

Responses contain source identifiers such as `[S1]` and `[S2]`.

The implementation validates citation identifiers against available retrieved evidence. Full claim-level citation verification is not implemented.

## 8. Operating Commands

### Start infrastructure

```bash
docker compose up -d
```

### Ingest approved documents

```bash
python -m src.ingestion.persist --scope markdown --max-documents 100
```

### Ask an architecture question

```bash
python -m scripts.ask_architecture "How is governance implemented in AI-A02?"
```

### Inspect the knowledge graph

```bash
python -m scripts.inspect_graph
```

### Test cross-project retrieval

```bash
python -m scripts.test_cross_project
```

### Run automated checks

```bash
python -m ruff check src scripts tests evaluation
python -m pytest -q
```

These commands assume that the local database, Ollama service, dependencies, models, and configured source repositories are available.

## 9. Engineering Validation

The prototype has demonstrated:

| Validation | Observed result |
|---|---|
| Automated tests | 13 passed |
| Unsupported questions | 6/6 abstained |
| Prompt-injection smoke test | Passed (single test) |
| Q026 balanced source retrieval | 100% Recall@5 |
| Indexed documents | 26 |
| Stored chunks | 67 |
| Graph entities | 6 |
| Graph relationships | 5 |

The Q026 result applies to one manually decomposed comparison question; it is not a generalized retrieval benchmark result.

## 10. Operations and Limitations

AI-A03 is a proof of concept rather than a production system.

Current limitations include:

- Approved Markdown sources only.
- Curated architectural graph.
- Manual cross-project question decomposition.
- Limited prompt-injection test coverage.
- No automated factual entailment verification for generated answers.
- Provisional retrieval benchmark relevance labels.
- No demonstrated production-grade tenancy, access control, or service monitoring.

## 11. Future Architectural Digital Twin

The knowledge and provenance capabilities of AI-A03 provide a foundation for future architectural digital twins.

Potential extensions include live deployed-system discovery, configuration synchronization, architecture drift detection, operational observability, automated impact analysis, and simulation.

These are future capabilities and are not implemented in the current prototype.

## 12. Related Documentation

- [Project README](../README.md)
- [Architecture Specification](AI-A03-Architecture-Specification.md)
- [Architecture Decision Records](adr/)
- [System Context Diagram](../diagrams/01-system-context.mmd)
- [Container Architecture](../diagrams/02-container-architecture.mmd)
- [Knowledge Ingestion](../diagrams/03-knowledge-ingestion.mmd)
- [Hybrid RAG and GraphRAG](../diagrams/04-hybrid-graphrag-retrieval.mmd)