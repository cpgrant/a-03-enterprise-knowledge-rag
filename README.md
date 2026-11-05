# AI-A03 — Enterprise Knowledge Intelligence

**Hybrid RAG · GraphRAG · Architecture Intelligence**

AI-A03 is a local-first enterprise knowledge architecture project.

It combines PostgreSQL/pgvector, hybrid retrieval,
an architectural knowledge graph, and local LLM inference
to support evidence-grounded architectural reasoning.

## Objectives

- Ingest architecture documents and implementation code.
- Support vector and full-text knowledge retrieval.
- Build source-grounded architecture relationships.
- Answer architecture questions with citations.
- Evaluate conventional RAG against GraphRAG.
- Establish foundations for an Architectural Digital Twin.

## Knowledge Sources

- AI-A01 — Enterprise AI Reference Architecture
- AI-A02 — Agent Orchestration and A2A

Both repositories are accessed read-only.

## Technology

- Python 3.12
- FastAPI and Pydantic
- PostgreSQL 17 + pgvector 0.8.7
- PostgreSQL full-text search
- NetworkX
- Ollama
- Docker Desktop / WSL2
- OpenTelemetry (planned)

## Architecture Diagrams

- [System Context](diagrams/01-system-context.mmd)
- [Container Architecture](diagrams/02-container-architecture.mmd)
- [Knowledge Ingestion](diagrams/03-knowledge-ingestion.mmd)
- [Hybrid RAG + GraphRAG](diagrams/04-hybrid-graphrag-retrieval.mmd)

## Documentation

- [Architecture Specification](docs/AI-A03-Architecture-Specification.md)
- [ADRs](docs/adr/)

## Project Schedule

| Day | Focus |
|---|---|
| 1 | Architecture, infrastructure, design and source inventory |
| 2 | Knowledge ingestion, Hybrid RAG and GraphRAG |
| 3 | Evaluation, governance, observability and publication |

## Current Status

Day 1 architecture and infrastructure baseline complete.

PostgreSQL and pgvector have been tested successfully.

Knowledge ingestion, retrieval APIs, graph construction,
LLM generation and evaluation are not yet implemented.

## Architectural Digital Twin

AI-A03 establishes versioned architectural knowledge
and graph relationships.

Future projects will add deployed-state discovery,
continuous telemetry, drift detection and simulation.

## License

To be determined.
