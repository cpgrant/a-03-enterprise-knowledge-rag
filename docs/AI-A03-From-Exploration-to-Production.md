# AI-A03 — From Exploration to Production

## Enterprise Knowledge Intelligence
### RTX 4090 Deployment, Hardening and Operationalization Roadmap

**Project:** AI-A03 — Enterprise Knowledge Intelligence  
**Architecture:** Hybrid RAG · GraphRAG · Architecture Intelligence  
**Document type:** Productionization Strategy and Engineering Implementation Plan  
**Version:** 1.0  
**Date:** 5 November 2026  
**Status:** Proposed roadmap — not yet implemented

---

## 1. Executive Summary

AI-A03 began as an architecture exploration project demonstrating how local large language models, hybrid retrieval, architecture knowledge graphs and versioned enterprise documentation can support evidence-grounded architectural reasoning.

The prototype successfully integrated PostgreSQL/pgvector, Ollama, semantic retrieval, full-text search, Reciprocal Rank Fusion, a source-backed knowledge graph, graph traversal and local LLM question answering.

The next phase is to transform that research baseline into a secure, observable and operationally reliable Enterprise Knowledge Intelligence service running on a workstation equipped with an NVIDIA RTX 4090 GPU and 24 GB of VRAM.

This transformation involves more than scaling the model or containerizing the application. Production readiness requires reliable ingestion, identity and authorization, evidence verification, controlled inference, monitoring, recovery, security testing and defined operational service objectives.

**Recommended initial target:** A secure, single-node production pilot with controlled internal users, measurable quality, repeatable deployment and documented recovery procedures.

A single RTX 4090 workstation should not be represented as a highly available enterprise platform. High availability, geographic redundancy and enterprise-wide resilience require additional infrastructure.

---

## 2. Project Baseline — Exploration Completed

### 2.1 Existing Architecture

AI-A03 has demonstrated:

- Read-only ingestion from AI-A01 and AI-A02 repositories.
- Git-aware source discovery and provenance.
- Markdown document chunking and local embedding generation.
- PostgreSQL 17 with pgvector 0.8.7.
- 768-dimensional embeddings using `embeddinggemma-2:270m`.
- Semantic vector retrieval.
- PostgreSQL full-text keyword retrieval.
- Hybrid retrieval with Reciprocal Rank Fusion.
- Repository-aware retrieval.
- A curated, evidence-backed architectural knowledge graph.
- NetworkX graph traversal and two-hop path discovery.
- Local architecture answer generation using `granite4.2:8b`.
- Citation identifier validation and basic unsupported-question abstention.
- Automated engineering tests and retrieval benchmarks.

### 2.2 Verified Engineering Baseline

| Measure | Recorded result |
|---|---:|
| Indexed documents | 26 |
| Indexed chunks | 67 |
| Graph entities | 6 |
| Graph relationships | 5 |
| Automated pytest tests | 13 passed |
| Unsupported-question smoke tests | 6/6 abstained |
| Prompt-injection smoke tests | 1 passed |
| Vector Recall@5 | 82.35% |
| Hybrid Recall@5 | 63.24% |
| Keyword Recall@5 | 47.06% |

The retrieval benchmark covered 34 answerable questions. Expected-source relevance labels are provisional and require independent review.

The six successful abstentions and single injection test are limited observations rather than production reliability or security guarantees.

### 2.3 Architectural Lessons

Three findings should guide productionization:

1. **Vector retrieval currently outperforms hybrid retrieval.** Hybrid fusion requires tuning, deduplication and possibly reranking before becoming the default production strategy.
2. **Source-aware retrieval improves the demonstrated cross-project comparison.** The Q026 result improved to 100% expected-source Recall@5 through manually decomposed and balanced source retrieval; this result should not be generalized to unseen queries.
3. **Traceable evidence is essential but not sufficient.** Citation identifiers link answers to retrieved passages, but claim-level support must be evaluated separately.

---

## 3. Production Scope and Definition

### 3.1 Intended Use

The initial production service will allow authorized users to:

- Search approved architecture documentation.
- Ask natural-language architecture questions.
- Retrieve evidence with traceable source references.
- Compare architectural decisions across designated projects.
- Explore curated architectural relationships.
- Identify missing or insufficient evidence.
- Review indexed source status and knowledge freshness.

### 3.2 Initial Deployment Scope

The first production deployment is deliberately constrained:

- One workstation or server hosting an RTX 4090.
- Local inference and local PostgreSQL.
- Internal, authenticated users.
- Controlled network exposure.
- Approved repositories and document collections.
- Explicit source access permissions.
- Defined concurrency limits.
- Backup and restore capabilities.
- Service monitoring and incident procedures.

### 3.3 Out of Scope for Initial Production

- Enterprise-wide high availability.
- Autonomous architecture changes or approvals.
- Direct unsupervised modification of source repositories.
- Unrestricted file-system or external network access by AI agents.
- A live, fully synchronized Architectural Digital Twin.
- Automatic authorization based solely on LLM output.
- Guaranteed factual correctness of generated answers.
- Production-grade multi-region scaling.

---

## 4. Target Production Architecture

### 4.1 Logical Architecture

```text
                  AUTHORIZED USERS
                        |
                  HTTPS / Web UI
                        |
             Gateway / Authentication
                        |
               AI-A03 REST API
                        |
            Policy and Access Control
                        |
          Query Planning / Orchestration
                        |
            Retrieval Coordination
                   /         \
           Hybrid Search   Graph Search
                 |              |
            PostgreSQL / pgvector
                 |
          Evidence Aggregation
                 |
          Optional Reranking
                 |
       Evidence / Citation Validation
                 |
             Local LLM
          NVIDIA RTX 4090
                 |
         Grounded Response API
                 |
                 UI

BACKGROUND SERVICES

Git / Approved Documents
          |
Ingestion Queue and Workers
          |
Parsing / Chunking / Embeddings
          |
PostgreSQL / pgvector / Graph

CROSS-CUTTING SERVICES

Authentication and Authorization
Audit Logging
Metrics and Distributed Tracing
Backups and Restore
Configuration and Secret Management
Monitoring and Alerts
```

The existing Python retrieval and generation components should be reused as much as possible.

The architecture should initially separate API requests from long-running ingestion tasks.

### 4.2 Service Components

| Service | Proposed technology | Responsibility |
|---|---|---|
| Reverse proxy | Caddy or equivalent | HTTPS, request routing |
| Application API | FastAPI / Pydantic | Authenticated endpoints and request validation |
| Knowledge database | PostgreSQL + pgvector | Documents, embeddings, graph, provenance |
| Inference runtime | Ollama initially | Local LLM and embedding inference |
| Ingestion worker | Python worker | Parsing, chunking, indexing and retries |
| Task queue | Redis-backed queue or PostgreSQL-backed queue | Durable ingestion scheduling |
| Knowledge graph | Existing PostgreSQL graph and NetworkX | Evidence-backed architecture relationships |
| Metrics | Prometheus | Metrics collection |
| Visualization | Grafana | Operational dashboards |
| Tracing | OpenTelemetry | Request and pipeline visibility |
| Logging | Structured application logging | Diagnostics and audit evidence |
| Deployment | Docker Compose initially | Reproducible single-node operations |

These technologies are proposed implementation choices and must be validated before adoption.

A dedicated graph database or more complex orchestration platform is unnecessary until requirements justify it.

---

## 5. RTX 4090 Inference Strategy

### 5.1 Hardware Baseline

The NVIDIA RTX 4090 provides 24 GB of VRAM.

The initial inference strategy should prioritize predictable memory utilization, controlled concurrency, model quality and system stability over maximum model size.

### 5.2 Recommended Initial Model Strategy

| Workload | Starting strategy |
|---|---|
| Architecture question answering | Current Granite 4.2 8B baseline |
| Document embeddings | Current embeddinggemma-2:270m baseline |
| Reranking | Small reranker, selected through evaluation |
| Query decomposition | Existing generation model with constrained structured outputs |
| Architecture entity extraction | Batch jobs with evidence validation |

Avoid changing all models simultaneously. Establish a baseline before conducting individual model comparisons.

Quantized 8B-class inference is the practical starting point. Larger models and extended contexts must be benchmarked for memory consumption, latency and accuracy.

### 5.3 GPU Scheduling

The same GPU may serve multiple workloads, but shared use must be controlled.

Recommended safeguards:

- Limit simultaneous generation requests.
- Bound prompt and output token counts.
- Separate ingestion workloads from interactive request peaks.
- Monitor GPU memory pressure and utilization.
- Enforce request timeouts and cancellation.
- Prevent uncontrolled model loading and eviction.
- Use backpressure or queueing under heavy load.

### 5.4 Inference Benchmark

Record the following for each tested model configuration:

| Metric | Purpose |
|---|---|
| Peak GPU memory | Determine safe model and concurrency configurations |
| Time to first token | Assess interactive responsiveness |
| Generated tokens/second | Measure decoding throughput |
| End-to-end latency p50/p95 | Assess user experience |
| Successful requests/second | Measure sustained capacity |
| Error and timeout rate | Evaluate reliability |
| Answer quality | Ensure performance changes do not reduce correctness |
| Quality under concurrency | Detect degradation as users increase |

Test with controlled question sets and defined prompt/output length distributions.

No production throughput or latency figures should be claimed before measurement on the target machine.

---

## 6. Production Engineering Workstreams

### Workstream A — Service Platform

**Objective:** Convert AI-A03 from developer-run scripts into a service.

Implementation tasks:

- Add a FastAPI application with versioned `/api/v1` endpoints.
- Define typed request and response contracts.
- Implement question-answering and retrieval endpoints.
- Add readiness and liveness health checks.
- Provide consistent error responses.
- Support request timeouts and cancellation.
- Configure server-side logging with request identifiers.
- Build container images and a reproducible deployment configuration.

Suggested endpoints:

| Endpoint | Function |
|---|---|
| `POST /api/v1/questions` | Generate grounded answers |
| `POST /api/v1/search` | Search knowledge sources |
| `GET /api/v1/sources` | List authorized knowledge sources |
| `GET /api/v1/documents/{id}` | Retrieve permitted document metadata |
| `POST /api/v1/ingestion/jobs` | Launch an authorized ingestion job |
| `GET /api/v1/ingestion/jobs/{id}` | Check ingestion progress |
| `GET /health/live` | Liveness |
| `GET /health/ready` | Dependency readiness |

**Acceptance gate:** Authenticated users can query permitted sources through an API; health checks and failure handling are tested.

### Workstream B — Knowledge Operations

**Objective:** Deliver recoverable, incremental indexing.

Implementation tasks:

- Create durable ingestion jobs and job states.
- Detect new, changed and removed documents.
- Make indexing idempotent.
- Retry transient failures with bounded backoff.
- Quarantine malformed or rejected documents.
- Record source version, content hash, ingestion time and model version.
- Handle embedding-model changes through explicit reindexing.
- Prevent stale or partial indexing from silently replacing healthy data.
- Support a documented recovery and reindex procedure.

**Acceptance gate:** Repeated ingestion produces no unintended duplication, interrupted jobs can recover, and source deletions or updates are handled consistently.

### Workstream C — Retrieval Quality

**Objective:** Establish reliable evidence retrieval.

Implementation tasks:

- Review expected-source labels.
- Expand the benchmark across document types and projects.
- Compare vector, keyword and hybrid methods.
- Implement document-level deduplication.
- Tune RRF weighting and candidate selection.
- Evaluate reranking.
- Introduce controlled query decomposition.
- Compare graph-enriched retrieval against a vector-only baseline.
- Test repository balance and authorization-filtered retrieval.
- Record latency and retrieval quality together.

**Acceptance gate:** A reviewed benchmark demonstrates an improvement over the established baseline without unacceptable latency or source leakage.

A proposed initial target is at least 90% Recall@5 on an independently reviewed benchmark, subject to refinement after baseline expansion.

### Workstream D — Grounded Answers and Governance

**Objective:** Ensure answers remain attributable and policy-compliant.

Implementation tasks:

- Validate all source references.
- Evaluate whether individual claims are supported by retrieved passages.
- Add answer evaluation using labeled examples and independent review.
- Implement retrieval-level authorization filtering.
- Propagate source permissions through graph traversal and citations.
- Treat document contents and retrieved text as untrusted input.
- Add prompt-injection and data-leakage regression tests.
- Maintain audit records for query access, policy outcomes and ingestion changes.
- Enforce explicit approval for any future state-changing AI actions.

**Acceptance gate:** Authorization tests prevent access to restricted sources, and claim-grounding tests meet agreed acceptance thresholds.

### Workstream E — Observability and Reliability

**Objective:** Make failures visible, diagnosable and recoverable.

Implementation tasks:

- Add structured JSON logs.
- Generate correlation identifiers across API, retrieval and inference.
- Instrument ingestion and answer-generation spans with OpenTelemetry.
- Publish metrics for latency, error rates and resource utilization.
- Monitor PostgreSQL availability and disk growth.
- Track indexing backlog and source freshness.
- Monitor GPU usage and inference queue length.
- Add alerts with documented operator responses.
- Schedule and verify backups.
- Perform restore exercises.
- Define startup, shutdown and deployment rollback procedures.

**Acceptance gate:** A controlled operational failure produces meaningful alerts and the service can be restored using documented procedures.

### Workstream F — User Interface and Operational Experience

**Objective:** Make the platform usable beyond its development team.

Implementation tasks:

- Build a minimal authenticated web interface.
- Display citations with source-document navigation.
- Show knowledge-source freshness and indexing status.
- Display useful explanations of abstention or insufficient evidence.
- Provide a read-only architecture relationship view.
- Add an administration view for ingestion status and errors.
- Include user feedback on answer usefulness and factual support.

**Acceptance gate:** A user can submit a question, inspect supporting evidence and report an incorrect answer without using developer tools.

---

## 7. Phased Implementation Plan

| Phase | Focus | Indicative effort | Deliverable |
|---|---|---:|---|
| P0 | Baseline validation and requirements | 1–2 days | Frozen benchmarks and production requirements |
| P1 | API and service packaging | 3–5 days | Containerized AI-A03 API |
| P2 | Durable ingestion and source lifecycle | 3–5 days | Recoverable indexing pipeline |
| P3 | Retrieval tuning and evaluation | 3–5 days | Improved evidence retrieval |
| P4 | Security and evidence governance | 4–6 days | Authorization and grounding controls |
| P5 | Observability and recovery | 3–5 days | Operational monitoring and runbooks |
| P6 | Load testing and production qualification | 3–5 days | Pilot deployment readiness report |

**Indicative total:** 20–33 engineering days.

This is a planning estimate, not a guarantee. Larger requirements for multi-user authorization, security review or high availability could substantially extend the work.

### Recommended Sequencing

The workstreams should follow two guiding principles:

1. Add a service interface early to expose operational shortcomings.
2. Avoid broadening functionality until reliability and evidence-quality improvements can be measured.

---

## 8. Production Quality Gates

The following are proposed acceptance targets. None should be represented as achieved until the corresponding tests pass.

| Dimension | Proposed production-pilot criterion |
|---|---|
| Retrieval | Recall@5 ≥90% on a reviewed benchmark |
| Answer grounding | ≥95% of sampled factual claims supported by inspected evidence |
| Source permissions | No unauthorized source disclosure in defined test scenarios |
| Interactive latency | p95 ≤10 seconds for specified representative queries |
| Availability | Target 99% for the single-node pilot |
| Ingestion reliability | Idempotent, recoverable jobs with auditable failures |
| Backups | Successful documented backup and restore exercise |
| Reproducibility | Deployment recreated from versioned configuration |
| Observability | Operational dashboards and actionable alerts |
| Security | Documented threat model and critical test cases passing |
| Release control | Tested upgrade and rollback procedure |

Availability, latency and throughput targets must specify the observation window, workload and maintenance assumptions.

A single-node pilot cannot meet a zero-downtime high-availability objective without additional infrastructure.

---

## 9. Security Architecture

### 9.1 Trust Boundaries

The implementation should explicitly separate:

- User requests.
- System and developer instructions.
- Retrieved source content.
- Tool responses.
- Database credentials.
- Inference service permissions.
- Administrative operations.

Retrieved documents must never be allowed to override application-level policies.

### 9.2 Authorization

Authorization must be enforced at the application and data-access layers, not merely through prompts.

Important requirements:

- Authenticated users.
- Role- or attribute-based permissions.
- Source repository access checks.
- Retrieval filtering before evidence reaches the model.
- Graph relationship access filtering.
- Protection against metadata and citation leakage.
- Explicit separation of user and administrator capabilities.

### 9.3 Secrets and Network Exposure

- Keep secrets outside Git.
- Use least-privilege database credentials.
- Bind internal services to restricted interfaces.
- Use TLS for external access.
- Protect administration endpoints.
- Pin and scan container dependencies.
- Define update and vulnerability-management procedures.
- Apply resource limits and request quotas.

### 9.4 Prompt-Injection Protection

Security controls should include:

- Defensive treatment of retrieved content.
- Constrained model output where appropriate.
- No direct execution of model-generated commands.
- Explicit tool permission boundaries.
- Deny-by-default policies for state-changing actions.
- Red-team tests using realistic malicious documents.
- Evaluation of cross-document instruction conflicts.

Prompt-injection resistance must be assessed continuously; no prompt format guarantees complete immunity.

---

## 10. Observability and Operations

### 10.1 Core Metrics

The system should publish metrics across five operational domains.

**API:** Requests, errors, p50/p95 latency, active requests.

**Retrieval:** Candidate counts, search latency, source coverage, retrieval failures.

**Inference:** Time to first token, generation throughput, GPU memory use, queued requests, timeouts.

**Ingestion:** Job state, indexing duration, failed documents, source freshness.

**Storage:** Database availability, connections, disk use, vector index size, backup age.

### 10.2 Operator Runbook

Create specific procedures for:

1. Starting and stopping AI-A03.
2. Checking dependency health.
3. Diagnosing unavailable Ollama models.
4. Restarting failed ingestion jobs.
5. Rebuilding indexes.
6. Restoring PostgreSQL.
7. Investigating unexplained retrieval degradation.
8. Rotating secrets.
9. Applying upgrades.
10. Rolling back a failed release.

### 10.3 Backup and Recovery

Backups should include:

- PostgreSQL database contents.
- Graph and source provenance metadata.
- Configuration necessary for restoration.
- Versioned model identifiers and embedding specifications.
- Approved source repository references.

Large derived embedding datasets may be reproducible, but rebuilding them must be tested before treating backups as optional.

Recovery Point Objective (RPO) and Recovery Time Objective (RTO) must be established through operational requirements and tested restore exercises.

---

## 11. Validation and Benchmark Strategy

Production qualification should measure three separate concerns.

### 11.1 Retrieval Quality

- Recall@k.
- Precision@k.
- Mean reciprocal rank or nDCG.
- Source coverage.
- Repository balance.
- Retrieval latency.

### 11.2 Answer Quality

- Claim-level evidence support.
- Correctness against adjudicated reference answers.
- Unsupported-claim frequency.
- Abstention accuracy.
- Citation completeness.
- Robustness under contradictory evidence.

### 11.3 Operational Quality

- p50/p95/p99 latency.
- Inference throughput.
- Error and timeout rates.
- Recovery behavior.
- Database stability.
- GPU memory pressure.
- Performance degradation under concurrency.

A retrieval improvement must not be presented as an improvement in factual answer quality unless that relationship is independently measured.

---

## 12. Release and Deployment Model

### 12.1 Development

Develop new features on short-lived branches using automated testing and review.

### 12.2 Staging

Use a production-like staging configuration with representative synthetic or approved test data.

Validate:

- Container startup.
- Database migrations.
- Ingestion.
- Retrieval.
- API authorization.
- Answer grounding.
- Monitoring.
- Backup and restore.
- Rollback.

### 12.3 Production Pilot

Deploy only after passing all critical acceptance gates.

Use controlled access, explicit user onboarding, operational monitoring and a documented rollback path.

### 12.4 Version Control

Recommended repository practices:

- Preserve the completed AI-A03 prototype baseline.
- Create a productionization milestone or branch.
- Record major design changes as ADRs.
- Tag reproducible releases.
- Maintain an operational changelog.
- Avoid committing environment secrets, local models or runtime database state.

---

## 13. Production Definition of Done

AI-A03 should be considered production-capable for its defined pilot scope only when:

- [ ] The service runs through a reproducible deployment process.
- [ ] Authentication and source-level authorization are enforced.
- [ ] Ingestion jobs are durable, idempotent and recoverable.
- [ ] Retrieval metrics meet reviewed acceptance criteria.
- [ ] Generated answers include traceable evidence.
- [ ] Claim-level grounding has been evaluated.
- [ ] Security tests and threat-review findings are addressed.
- [ ] GPU memory use and concurrency are measured.
- [ ] Health checks, monitoring and alerts are operational.
- [ ] Backup and restore are tested.
- [ ] Operational procedures and rollback are documented.
- [ ] The deployment has completed a controlled acceptance test.
- [ ] Residual risks and service limitations are recorded.

**Production-ready is a demonstrated operating state, not a feature checklist alone.**

---

## 14. Beyond Production — Architectural Digital Twin

A successful production knowledge service establishes a stronger foundation for architectural digital twin development.

Future phases could integrate:

- Deployed architecture discovery.
- Live service and infrastructure state.
- Architecture-to-implementation traceability.
- Event and configuration synchronization.
- Drift detection.
- Dependency impact analysis.
- Operational simulation.
- Governance-aware architectural recommendations.

These capabilities represent a subsequent architectural research and engineering program.

They should not be treated as dependencies for completing the initial AI-A03 production pilot.

---

## 15. Portfolio and Strategic Significance

AI-A03 demonstrates a progression from architectural exploration toward operational engineering.

**Exploration:** Define a reference architecture and identify feasible local technologies.

**Prototype:** Implement ingestion, retrieval, graph relationships and local inference.

**Evaluation:** Benchmark retrieval, test answer behavior and document limitations.

**Production engineering:** Introduce service interfaces, security, durable workflows, observability and recovery.

**Operational validation:** Demonstrate measurable quality, reliable operation and controlled release procedures.

This progression provides evidence of both strategic architecture capabilities and hands-on engineering execution.

The resulting project can be presented as a practical case study in designing, implementing, evaluating and operationalizing enterprise AI systems.

---

## 16. Related Project Documentation

- [AI-A03 README](../README.md)
- [Architecture Specification](AI-A03-Architecture-Specification.md)
- [Implementation and Operations Guide](AI-A03-Implementation-and-Operations.md)
- [Technical Evaluation Report](AI-A03-Technical-Evaluation-Report.md)
- [Architecture Decision Records](adr/)
- [Architecture Overview Infographic](../infographics/AI-A03-1-Architecture-Overview.png)
- [Knowledge Ingestion and GraphRAG Infographic](../infographics/AI-A03-2-Knowledge-Ingestion-GraphRAG.png)

---

**Document status:** Proposed implementation roadmap.

**Next milestone:** P0 — Freeze the existing prototype baseline, establish operational requirements and benchmark the current system on the RTX 4090.