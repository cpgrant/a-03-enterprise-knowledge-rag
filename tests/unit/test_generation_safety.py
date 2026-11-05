from types import SimpleNamespace

import httpx
import pytest

from src.generation import answer as generation


def test_no_evidence_returns_abstention(monkeypatch):
    monkeypatch.setattr(
        generation,
        "graphrag_search",
        lambda query, limit=4: ([], []),
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Ollama should not be called")

    monkeypatch.setattr(
        generation.httpx, "post", fail_if_called
    )

    result = generation.answer_architecture(
        "What is the production SLA?"
    )

    assert result.done_reason == "no_evidence"
    assert result.sources == []
    assert "No relevant" in result.answer


def test_unknown_citation_is_detected(monkeypatch):
    passage = SimpleNamespace(
        source="AI-A02",
        file_path="docs/adr/ADR-003-a2a.md",
        git_commit="test-commit",
        content="Use A2A across the remote agent boundary.",
    )

    monkeypatch.setattr(
        generation,
        "graphrag_search",
        lambda query, limit=4: ([passage], []),
    )

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "response": "A2A is selected. [S99]",
                "done_reason": "stop",
            }

    monkeypatch.setattr(
        generation.httpx,
        "post",
        lambda *args, **kwargs: FakeResponse(),
    )

    result = generation.answer_architecture(
        "What protocol does A02 select?"
    )

    assert result.citation_ids_valid is False
    assert result.done_reason == "stop"


def test_ollama_connection_error_propagates(monkeypatch):
    passage = SimpleNamespace(
        source="AI-A02",
        file_path="docs/adr/ADR-003-a2a.md",
        git_commit="test-commit",
        content="A2A interoperability.",
    )

    monkeypatch.setattr(
        generation,
        "graphrag_search",
        lambda query, limit=4: ([passage], []),
    )

    def connection_failure(*args, **kwargs):
        raise httpx.ConnectError("Service unavailable")

    monkeypatch.setattr(
        generation.httpx, "post", connection_failure
    )

    with pytest.raises(httpx.ConnectError):
        generation.answer_architecture(
            "How is A2A used?"
        )
