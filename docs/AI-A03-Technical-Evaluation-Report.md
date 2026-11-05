# AI-A03 — Technical Evaluation Report

**Project:** Enterprise Knowledge Intelligence  
**Architecture:** Hybrid RAG · GraphRAG · Architecture Intelligence  
**Evaluation date:** 5 November 2026  
**Status:** Prototype evaluation completed; final publication pending

---

## 1. Executive Summary

AI-A03 demonstrates a local-first Enterprise Knowledge Intelligence architecture integrating:

- Semantic vector retrieval
- PostgreSQL full-text retrieval
- Reciprocal Rank Fusion (RRF)
- Source-grounded architecture knowledge graphs
- Graph-enriched retrieval
- Repository-aware cross-project comparisons
- Local LLM architecture question answering
- Source citation-identifier validation

The evaluation establishes a functional engineering baseline for architectural knowledge retrieval and reasoning across AI-A01 and AI-A02.

**Principal finding:** Semantic vector retrieval outperformed the initial hybrid retrieval implementation on the evaluated question set.

The prototype also demonstrated successful abstention for six unsupported questions and a source-balanced retrieval improvement for one cross-project comparison.

These results establish feasibility but do not demonstrate production readiness or comprehensive factual reliability.

## 2. Evaluation Objectives

The evaluation examined six questions:

1. Can architectural knowledge be indexed and retrieved from multiple repositories?
2. How do vector, keyword and hybrid retrieval compare?
3. Can project-aware retrieval improve cross-repository evidence coverage?
4. Can architectural graph relationships support traceable multi-hop reasoning?
5. Can the answer-generation system cite retrieved sources and abstain when evidence is unavailable?
6. Can automated checks identify basic functional failures and unsafe generation behavior?

## 3. Evaluation Environment

| Component | Configuration |
|---|---|
| Operating environment | Ubuntu WSL2 |
| Language | Python 3.12 |
| GPU | NVIDIA RTX 4090, 24 GB VRAM |
| Database | PostgreSQL 17 |
| Vector extension | pgvector 0.8.7 |
| Embedding model | embeddinggemma-2:270m |
| Embedding dimensions | 768 |
| Generation model | granite4.2:8b |
| Inference runtime | Ollama |
| Graph traversal | NetworkX |
| Automated testing | pytest |
| Static checks | Ruff |

The experiments used local inference and a locally hosted knowledge database.

## 4. Knowledge Corpus

AI-A03 indexed approved Markdown architecture documents from two read-only source repositories.

| Repository | Documents | Chunks |
|---|---:|---:|
| AI-A01 — Enterprise AI Reference Architecture | 9 | 12 |
| AI-A02 — Agent Orchestration & A2A | 17 | 55 |
| **Total** | **26** | **67** |

The source-discovery baseline identified 84 eligible repository files, but the evaluated indexed corpus contained 26 approved Markdown documents.

Consequently, the retrieval results should not be generalized to all source-code and architecture artifacts within the repositories.

## 5. Evaluation Dataset and Method

The evaluation dataset comprised **40 architecture questions**:

| Question category | Count |
|---|---:|
| Architectural decisions | 10 |
| Implementation | 10 |
| Comparisons | 8 |
| Multi-hop reasoning | 6 |
| Unsupported or unanswerable | 6 |
| **Total** | **40** |

Retrieval benchmarking used the **34 answerable questions**.

The remaining six were used to test missing-evidence handling and abstention.

Expected-source labels were assigned to questions, and the source paths were checked for existence. The labels remain provisional because their factual relevance and completeness have not been independently adjudicated.

### Retrieval Metrics

**Top-1 accuracy:** Percentage of questions for which the first-ranked retrieval result matched an assigned expected source.

**Recall@5:** Fraction of assigned expected source documents recovered within the five highest-ranked results, averaged across evaluated questions.

**All expected documents @5:** Percentage of questions for which all assigned expected source documents appeared among the first five results.

**Mean retrieval latency:** Average measured retrieval time during the local benchmark.

These are source-retrieval metrics, not end-to-end answer correctness or factual-grounding scores.

## 6. Retrieval Benchmark Results

| Retrieval method | Top-1 | Recall@5 | All expected @5 | Mean latency |
|---|---:|---:|---:|---:|
| **Vector** | **44.12%** | **82.35%** | **73.53%** | 75 ms |
| Hybrid RRF | 32.35% | 63.24% | 52.94% | 96 ms |
| Keyword | 17.65% | 47.06% | 38.24% | 26 ms |

### Interpretation

**Vector retrieval achieved the highest observed relevance scores** on this dataset, including 82.35% Recall@5.

Hybrid retrieval did not outperform vector retrieval. Its lower scores suggest that the initial RRF configuration, chunk duplication and candidate-ranking behavior require further investigation.

Keyword retrieval was fastest but had the lowest relevance scores, consistent with the limitations of exact-term matching on architecture questions expressed using different terminology.

### Engineering Implications

The results support using vector retrieval as the current performance baseline rather than assuming that combining retrieval methods automatically improves results.

Potential improvements include document-level deduplication, candidate balancing, source-aware reranking, and tuning fusion parameters.

These improvements require new benchmarks before any quality claims can be made.

## 7. Repository-Aware Cross-Project Retrieval

### Test Question Q026

*How does AI-A02 extend the agent-orchestration architecture described in AI-A01?*

The original retrieval approaches failed to recover the assigned evidence from both repositories within the top five results.

A project-aware method was introduced using:

- Manually formulated A01 and A02 subquestions
- Repository-specific database filtering
- A balanced allocation of retrieval results
- Combined document-level evidence

### Observed Result

| Method | Expected-source Recall@5 on Q026 |
|---|---:|
| Original unfiltered retrieval | 0% |
| Balanced cross-project vector retrieval | 100% |

The balanced method recovered both assigned expected source documents.

**Important limitation:** This was a single manually decomposed comparison question. The result is not evidence of a general improvement across all 34 benchmark questions, nor of automatic multi-repository question decomposition.

## 8. Architecture Graph Evaluation

The architecture knowledge graph contains:

| Measure | Result |
|---|---:|
| Architecture entities | 6 |
| Evidence-backed relationships | 5 |
| Graph traversal | Demonstrated |
| Two-hop path exploration | Demonstrated |
| Graph-enriched retrieval | Implemented |

The prototype records architecture relationships with source references and distinguishes accepted architectural decisions from implementation claims reported in architecture decision records.

Graph traversal supports exploring connected architectural entities. However, a path through a shared project entity does not prove direct runtime integration, causality, or operational dependency.

The current graph uses a small curated set of relationships rather than automated, broad-scale knowledge extraction.

The evaluation does not establish that GraphRAG systematically improves retrieval or answer quality over vector-only RAG.

## 9. Answer Generation and Citation Checks

Architecture answers are generated locally with `granite4.2:8b` through Ollama.

The generation workflow uses retrieved evidence and source labels such as `[S1]` and `[S2]`.

The engineering tests cover missing evidence, invalid citation identifiers and local inference connection failures.

**What citation checking verifies:** Whether a citation identifier belongs to the supplied source set.

**What it does not verify:** Whether each natural-language claim is logically or factually supported by the cited passage.

Therefore, citation presence is not treated as equivalent to answer faithfulness.

## 10. Unsupported-Question and Abstention Tests

Six unsupported questions were evaluated, covering requests for information not established by the indexed evidence, including operational SLAs, audited costs, customer data, security ratings and production-scale latency.

| Metric | Result |
|---|---:|
| Unsupported questions tested | 6 |
| Successful abstentions | 6 |
| Observed abstention rate | 100% |
| Mean generation time in this smoke run | Approximately 1.37 seconds |

These outcomes demonstrate correct abstention behavior for the selected test cases only.

They do not establish a general 100% abstention rate on unknown questions.

## 11. Prompt-Injection Smoke Test

One manual smoke test supplied a simulated retrieved passage containing an instruction intended to override normal answer-generation behavior.

The model did not follow the injected instruction and instead answered the architecture question with a source citation.

**Observed result:** One of one tested injection attempts was resisted.

The test is evidence of a successful local safeguard in that scenario, not comprehensive prompt-injection resistance.

Further testing should include indirect instructions in files, conflicting retrieved sources, role spoofing, encoded payloads, tool-output manipulation and systematic adversarial test sets.

## 12. Automated Engineering Validation

The latest recorded development validation showed:

| Validation | Outcome |
|---|---|
| pytest | 13 tests passed |
| Ruff | All checks passed |
| Missing-evidence handling | Covered |
| Invalid citation identifiers | Covered |
| Model-service connection failure | Covered |
| Cross-project source balancing | Covered using mocks |

The manual six-question abstention check and single prompt-injection test were performed separately from the 13 automated tests.

A fresh test run is required before the final GitHub publication.

## 13. Limitations and Threats to Validity

The evaluation has several important limitations:

1. **Small corpus:** The indexed architecture corpus consists of 26 Markdown documents and 67 chunks.
2. **Provisional relevance judgments:** Expected-source labels are not independently reviewed for factual evidence sufficiency.
3. **Source imbalance:** AI-A02 has substantially more indexed chunks than AI-A01.
4. **Limited graph:** Six entities and five curated relationships restrict the conclusions that can be drawn about GraphRAG scalability.
5. **Hybrid underperformance:** The initial RRF implementation requires ranking and deduplication analysis.
6. **Single-question cross-project improvement:** Q026 cannot establish general retrieval gains.
7. **Citation validation scope:** Source-ID validation does not guarantee claim-level factual support.
8. **Limited answer evaluation:** No comprehensive blind factual-answer assessment was completed.
9. **Security test coverage:** One injection smoke test does not provide broad adversarial assurance.
10. **No production operational evidence:** Large-scale concurrency, recovery, multi-tenancy, service-level reliability and production authorization were not evaluated.

## 14. Recommended Engineering Improvements

| Priority | Improvement | Rationale |
|---|---|---|
| High | Validate relevance labels | Establish trustworthy evaluation ground truth |
| High | Tune hybrid ranking and deduplication | Investigate the vector/hybrid performance gap |
| High | Evaluate factual answer support | Measure evidence faithfulness independently of source IDs |
| High | Expand negative and adversarial tests | Strengthen reliability and safety evaluation |
| Medium | Automate cross-project query planning | Generalize the Q026 demonstration |
| Medium | Expand graph extraction and evidence validation | Increase architectural coverage |
| Medium | Introduce document-level reranking | Reduce repeated-chunk dominance |
| Medium | Add operational tracing | Support latency and failure diagnosis |
| Future | Integrate live architectural state | Evolve toward an Architectural Digital Twin |

## 15. Engineering Conclusions

AI-A03 demonstrates that a local-first architecture intelligence system can combine versioned source ingestion, semantic retrieval, keyword search, a small evidence-backed graph, and local LLM generation in a single working prototype.

The strongest measured retrieval result is **82.35% Recall@5 with vector retrieval** on the provisional 34-question answerable benchmark.

The project also demonstrates practical lessons:

- Hybrid retrieval must be evaluated rather than assumed superior.
- Repository balance matters for cross-project comparisons.
- Graph paths require careful interpretation.
- Citations require validation beyond checking source identifiers.
- Abstention and security behavior should be tested explicitly.

These results provide a useful engineering baseline for future enterprise architecture intelligence work.

**Final assessment:** Successful architecture and engineering proof of concept, with measurable retrieval performance and documented limitations. Not yet a production-grade knowledge platform or live Architectural Digital Twin.

---

## 16. Related Artifacts

- [Project README](../README.md)
- [Architecture Specification](AI-A03-Architecture-Specification.md)
- [Implementation and Operations Guide](AI-A03-Implementation-and-Operations.md)
- [Architecture Decision Records](adr/)
- [Architecture Overview Infographic](../infographics/AI-A03-1-Architecture-Overview.png)
- [Knowledge Ingestion and GraphRAG Infographic](../infographics/AI-A03-2-Knowledge-Ingestion-GraphRAG.png)

*AI-A03-3 Evaluation Results Infographic is deliberately excluded pending correction of its benchmark numbers.*