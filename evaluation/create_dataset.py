import json
from collections import Counter
from pathlib import Path

A01 = "AI-A01/"
A02 = "AI-A02/"

def a01(path):
    return A01 + path

def a02(path):
    return A02 + path

rows = []

def add(category, question, evidence=(), answerable=True):
    rows.append({
        "id": f"Q{len(rows)+1:03d}",
        "category": category,
        "question": question,
        "answerable": answerable,
        "expected_sources": list(evidence),
        "review_status": "pending_human_review",
    })

# 10 — Architecture decisions
decisions = [
    ("Why adopt modular open-source architecture?", a01("docs/adr/001-open-source-modular-architecture.md")),
    ("Why select LangGraph for orchestration in A01?", a01("docs/adr/002-langgraph-orchestration.md")),
    ("What is the rationale for local model inference in A01?", a01("docs/adr/003-local-model-inference.md")),
    ("Why use PostgreSQL with pgvector in A01?", a01("docs/adr/004-postgresql-pgvector.md")),
    ("Why separate policy enforcement from orchestration in A01?", a01("docs/adr/005-independent-policy-enforcement.md")),
    ("What observability architecture does A01 propose?", a01("docs/adr/006-opentelemetry.md")),
    ("Which orchestration framework was accepted for A02?", a02("docs/adr/ADR-001-orchestration.md")),
    ("What agent topology was selected for A02?", a02("docs/adr/ADR-002-agent-topology.md")),
    ("How does A02 distinguish local agents from remote A2A agents?", a02("docs/adr/ADR-003-a2a.md")),
    ("What governance policy approach was documented in A02?", a02("docs/adr/ADR-006-governance-policy.md")),
]
for q, p in decisions:
    add("decision", q, [p])

# 10 — Implementation and operations
implementations = [
    ("How does A02 implement governance decisions?", "docs/adr/ADR-006-governance-policy.md"),
    ("What logging mechanism is implemented in A02?", "docs/adr/ADR-005-implemented-state-observability.md"),
    ("How is execution history maintained in A02?", "docs/adr/ADR-005-implemented-state-observability.md"),
    ("What A2A interoperability approach does A02 document?", "docs/AI-A02-3-A2A-Interoperability-Guide.md"),
    ("How is A02 orchestration structured?", "docs/AI-A02-2-Orchestration-Guide.md"),
    ("What validation activities are described for A02?", "docs/AI-A02-4-Validation-Operations-Guide.md"),
    ("What operational procedures does A02 document?", "docs/AI-A02-Operations-Runbook.md"),
    ("What security concerns are documented for A02?", "security/SECURITY-REVIEW.md"),
    ("What is the overall implementation scope reported for A02?", "docs/AI-A02-Complete-Project-Report.md"),
    ("How does A02 describe its architecture interfaces?", "docs/AI-A02-Architecture-Specification.md"),
]
for q, p in implementations:
    add("implementation", q, [a02(p)])

# 8 — Cross-project comparisons
comparisons = [
    ("Compare the orchestration decisions in A01 and A02.",
     "docs/adr/002-langgraph-orchestration.md", "docs/adr/ADR-001-orchestration.md"),
    ("Compare A01's governance architecture with A02's governance implementation.",
     "docs/adr/005-independent-policy-enforcement.md", "docs/adr/ADR-006-governance-policy.md"),
    ("Compare A01's proposed observability with A02's implemented logging.",
     "docs/adr/006-opentelemetry.md", "docs/adr/ADR-005-implemented-state-observability.md"),
    ("How do A01's modular architecture principles relate to A02's A2A decision?",
     "docs/adr/001-open-source-modular-architecture.md", "docs/adr/ADR-003-a2a.md"),
    ("Compare A01's requirements with A02's architecture specification.",
     "docs/01-architecture-requirements.md", "docs/AI-A02-Architecture-Specification.md"),
    ("How does A02 extend the agent-orchestration architecture described in A01?",
     "docs/adr/002-langgraph-orchestration.md", "docs/AI-A02-2-Orchestration-Guide.md"),
    ("Compare A01's technology stack with A02's reported implementation.",
     "docs/02-technology-stack.md", "docs/AI-A02-Complete-Project-Report.md"),
    ("What differs between A01's reference architecture and A02's agent design?",
     "README.md", "docs/AI-A02-1-Architecture-Design-Guide.md"),
]
for q, p1, p2 in comparisons:
    add("comparison", q, [a01(p1), a02(p2)])

# 6 — Graph relationship questions
graph_questions = [
    ("How are A2A and the Python policy engine connected in A02?",
     "docs/adr/ADR-003-a2a.md", "docs/adr/ADR-006-governance-policy.md"),
    ("How are LangGraph and A2A related through A02?",
     "docs/adr/ADR-003-a2a.md", "docs/adr/ADR-003-a2a.md"),
    ("What connects A2A and JSON logging in the A02 architecture?",
     "docs/adr/ADR-003-a2a.md", "docs/adr/ADR-005-implemented-state-observability.md"),
    ("How are the policy engine and execution history related in A02?",
     "docs/adr/ADR-006-governance-policy.md", "docs/adr/ADR-005-implemented-state-observability.md"),
    ("What architectural project connects LangGraph and the policy engine?",
     "docs/adr/ADR-003-a2a.md", "docs/adr/ADR-006-governance-policy.md"),
    ("What connects A2A interoperability and in-memory execution history?",
     "docs/adr/ADR-003-a2a.md", "docs/adr/ADR-005-implemented-state-observability.md"),
]
for q, p1, p2 in graph_questions:
    add("multihop", q, sorted({a02(p1), a02(p2)}))

# 6 — Questions expected to be unsupported
unsupported = [
    "What was the exact production uptime percentage for A02 in October 2026?",
    "What is the signed enterprise SLA for A02?",
    "What is the audited annual production cost of A02 for 2027?",
    "Which named customers have deployed A02 in production?",
    "What is A02's independently certified security compliance rating?",
    "What is the measured production p99 latency for A02 across one million requests?",
]
for q in unsupported:
    add("abstention", q, answerable=False)

assert len(rows) == 40
counts = Counter(r["category"] for r in rows)
assert dict(counts) == {
    "decision": 10,
    "implementation": 10,
    "comparison": 8,
    "multihop": 6,
    "abstention": 6,
}

output = Path("evaluation/questions.jsonl")
with output.open("w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("AI-A03 Evaluation Dataset")
print("=" * 45)
for category, count in counts.items():
    print(f"{category}: {count}")
print(f"Total: {len(rows)}")
print(f"Written: {output}")
print("Labels: pending human review")
