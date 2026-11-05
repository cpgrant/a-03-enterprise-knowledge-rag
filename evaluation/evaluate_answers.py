from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from src.generation.answer import answer_architecture

DATASET = Path("evaluation/questions.jsonl")
OUTPUT = Path("evaluation/results/answer_smoke.jsonl")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ids",
        nargs="+",
        default=["Q011", "Q035"],
    )
    args = parser.parse_args()

    questions = {
        q["id"]: q
        for q in (
            json.loads(line)
            for line in DATASET.read_text(
                encoding="utf-8"
            ).splitlines()
        )
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    print("AI-A03 — Answer Quality Evaluation")
    print("=" * 65)

    with OUTPUT.open("w", encoding="utf-8") as file:
        for question_id in args.ids:
            q = questions[question_id]

            print(f"\n{question_id}: {q['question']}")
            print("Expected answerable:", q["answerable"])

            start = time.perf_counter()
            result = answer_architecture(
                q["question"], limit=4
            )
            elapsed = time.perf_counter() - start

            record = {
                "id": question_id,
                "category": q["category"],
                "question": q["question"],
                "expected_answerable": q["answerable"],
                "answer": result.answer,
                "sources": result.sources,
                "citation_ids_valid": (
                    result.citation_ids_valid
                ),
                "generation_completed": (
                    result.done_reason
                ),
                "latency_seconds": round(elapsed, 2),
                "human_review": {
                    "factually_supported": None,
                    "appropriate_abstention": None,
                    "citation_claim_support": None,
                    "notes": "",
                },
            }

            file.write(
                json.dumps(record, ensure_ascii=False)
                + "\n"
            )

            print("\nANSWER:")
            print(result.answer)
            print("\nSources:", len(result.sources))
            print(
                "Citation IDs valid:",
                result.citation_ids_valid,
            )
            print("Latency:", round(elapsed, 2), "seconds")
            print("Completed:", result.done_reason)

    print("\nResults saved to:", OUTPUT)
    print("Human evidence review required.")


if __name__ == "__main__":
    main()
