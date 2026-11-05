from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

from src.retrieval.hybrid import hybrid_search
from src.retrieval.keyword import keyword_search
from src.retrieval.vector import vector_search

METHODS = {
    "vector": vector_search,
    "keyword": keyword_search,
    "hybrid": hybrid_search,
}


def source_id(result):
    return f"{result.source}/{result.file_path}"


def unique_documents(results, limit=5):
    seen = set()
    documents = []

    for result in results:
        key = source_id(result)
        if key not in seen:
            seen.add(key)
            documents.append(key)

        if len(documents) >= limit:
            break

    return documents


def evaluate(question, method, candidate_limit=20):
    start = time.perf_counter()

    results = METHODS[method](
        question["question"],
        limit=candidate_limit,
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    # Collapse chunk-level results into unique documents.
    documents = unique_documents(results, limit=5)

    expected = set(question["expected_sources"])
    retrieved = set(documents)

    top1 = int(bool(documents) and documents[0] in expected)
    hits = len(expected & retrieved)

    recall5 = hits / len(expected)
    all_found = int(expected <= retrieved)

    return {
        "id": question["id"],
        "category": question["category"],
        "method": method,
        "top1": top1,
        "recall5": round(recall5, 4),
        "all_found5": all_found,
        "latency_ms": round(elapsed_ms, 2),
        "expected": json.dumps(sorted(expected)),
        "retrieved": json.dumps(documents),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    dataset = [
        json.loads(line)
        for line in Path(
            "evaluation/questions.jsonl"
        ).read_text(encoding="utf-8").splitlines()
    ]

    answerable = [
        q for q in dataset
        if q["answerable"] and q["expected_sources"]
    ]

    if not args.all:
        answerable = answerable[:args.limit]

    rows = []

    print("AI-A03 — Retrieval Benchmark")
    print("=" * 65)
    print("Questions:", len(answerable))
    print("Methods:", ", ".join(METHODS))
    print("Evaluation status: PROVISIONAL")
    print()

    for question in answerable:
        print(question["id"], question["question"])

        for method in METHODS:
            result = evaluate(question, method)
            rows.append(result)

            print(
                f"  {method:<8}"
                f"top1={result['top1']} "
                f"recall@5={result['recall5']:.2f} "
                f"all@5={result['all_found5']} "
                f"latency={result['latency_ms']:.0f}ms"
            )

    grouped = defaultdict(list)

    for row in rows:
        grouped[row["method"]].append(row)

    print("\nSUMMARY")
    print("-" * 65)

    for method, values in grouped.items():
        n = len(values)

        print(
            f"{method:<8} "
            f"top1={sum(v['top1'] for v in values)/n:.2%} "
            f"recall@5={sum(v['recall5'] for v in values)/n:.2%} "
            f"all@5={sum(v['all_found5'] for v in values)/n:.2%} "
            f"mean_latency={sum(v['latency_ms'] for v in values)/n:.0f}ms"
        )

    output = Path("evaluation/results")
    output.mkdir(parents=True, exist_ok=True)

    filename = (
        "retrieval_full.csv" if args.all
        else "retrieval_smoke.csv"
    )

    with (output / filename).open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=list(rows[0])
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\nResults:", output / filename)
    print("Scores use provisional evidence labels.")


if __name__ == "__main__":
    main()
