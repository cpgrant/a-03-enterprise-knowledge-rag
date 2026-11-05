import pytest

from src.retrieval import cross_project
from src.retrieval.vector import SearchResult


def make_result(source, path, chunk_index=0):
    return SearchResult(
        source=source,
        file_path=path,
        git_commit="test-commit",
        chunk_index=chunk_index,
        content="Test architectural evidence",
        distance=0.1,
    )


def test_balanced_retrieval(monkeypatch):
    calls = []

    def fake_search(query, limit=5, source=None):
        calls.append((query, limit, source))

        if source == "AI-A01":
            return [
                make_result("AI-A01", "adr/langgraph.md"),
                make_result("AI-A01", "adr/langgraph.md", 1),
                make_result("AI-A01", "technology.md"),
            ]

        if source == "AI-A02":
            return [
                make_result("AI-A02", "adr/orchestration.md"),
                make_result("AI-A02", "design.md"),
                make_result("AI-A02", "implementation.md"),
            ]

        raise AssertionError("Unexpected repository")

    monkeypatch.setattr(
        cross_project, "vector_search", fake_search
    )

    results = cross_project.cross_project_search(
        "A01 orchestration",
        "A02 implementation",
    )

    assert len(results) == 5
    assert [r.source for r in results] == [
        "AI-A01", "AI-A01",
        "AI-A02", "AI-A02", "AI-A02",
    ]

    assert len({
        (r.source, r.file_path) for r in results
    }) == 5

    assert [call[2] for call in calls] == [
        "AI-A01", "AI-A02"
    ]


@pytest.mark.parametrize(
    "a01_question,a02_question,a01_limit,a02_limit",
    [
        ("", "A02", 2, 3),
        ("A01", "", 2, 3),
        ("A01", "A02", 0, 3),
        ("A01", "A02", 2, 6),
        ("A01", "A02", 3, 3),
    ],
)
def test_invalid_requests(
    a01_question, a02_question, a01_limit, a02_limit
):
    with pytest.raises(ValueError):
        cross_project.cross_project_search(
            a01_question,
            a02_question,
            a01_limit=a01_limit,
            a02_limit=a02_limit,
        )
