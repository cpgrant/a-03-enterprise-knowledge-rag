# ADR-003 — Source-Grounded Architecture Knowledge Graph

Date: 2026-11-05
Status: Accepted

## Context

Enterprise architecture consists of components,
interfaces, decisions, policies, and dependencies.

LLM-generated relationships may be incorrect.

## Decision

Use a typed architectural knowledge graph.

Persist entities and relations in PostgreSQL.

Use NetworkX for initial graph traversal.

Extract relationships deterministically where possible.

Require source evidence for architectural claims.

## Rationale

- Explainable dependency analysis
- Source traceability
- Reproducible knowledge extraction
- Architecture impact analysis
- Digital Twin foundations

## Consequences

Graph extraction requires validation.

Unverified relationships must not be presented as facts.

Neo4j may be evaluated in a future project.
