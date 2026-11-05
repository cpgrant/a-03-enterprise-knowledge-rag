import argparse

from src.retrieval.hybrid import hybrid_search
from src.retrieval.keyword import keyword_search
from src.retrieval.vector import vector_search


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()

    query = args.query

    methods = {
        "VECTOR": vector_search(query, 3),
        "KEYWORD": keyword_search(query, 3),
        "HYBRID": hybrid_search(query, 3),
    }

    print(f"\nQuestion: {query}")

    for method, results in methods.items():
        print(f"\n{method}")
        print("-" * 65)

        for rank, result in enumerate(results, 1):
            print(
                f"{rank}. [{result.source}] "
                f"{result.file_path}"
            )

            if method == "HYBRID":
                print(
                    f"   RRF: {result.rrf_score:.5f} "
                    f"Methods: {result.retrieval_methods}"
                )


if __name__ == "__main__":
    main()
