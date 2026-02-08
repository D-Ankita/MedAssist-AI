"""Tests for MedAssist FastAPI endpoints."""

from __future__ import annotations

from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Create a test client with a mocked agent."""
    mock_agent = MagicMock()
    mock_agent.chain.retriever.document_count = 42
    mock_agent.process_query.return_value = {
        "intent": "ANSWER",
        "answer": "Diabetes is a chronic metabolic disease.",
        "sources": [{"document": "Diabetes-Overview.pdf", "page": 1, "relevance": 0.91}],
        "chunks_retrieved": 2,
        "relevance_scores": [0.91, 0.85],
    }

    with patch("main.MedAssistAgent", return_value=mock_agent):
        from main import app
        # Set the global agent
        import main
        main.agent = mock_agent
        yield TestClient(app)
        main.agent = None


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "MedAssist AI"
        assert data["documents_indexed"] == 42


class TestQueryEndpoint:
    def test_query_returns_answer(self, client: TestClient):
        response = client.post("/query", json={
            "question": "What is diabetes?",
            "chat_history": [],
        })
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "ANSWER"
        assert "Diabetes" in data["answer"]
        assert len(data["sources"]) > 0

    def test_query_empty_question_returns_400(self, client: TestClient):
        response = client.post("/query", json={
            "question": "   ",
            "chat_history": [],
        })
        assert response.status_code == 400

    def test_query_with_chat_history(self, client: TestClient):
        response = client.post("/query", json={
            "question": "What about the symptoms?",
            "chat_history": [
                {"role": "user", "content": "Tell me about diabetes"},
                {"role": "assistant", "content": "Diabetes is a metabolic disease."},
            ],
        })
        assert response.status_code == 200


class TestIngestEndpoint:
    def test_ingest_without_admin_key(self, client: TestClient):
        """Ingest should work when no ADMIN_SECRET is set (default)."""
        with patch("main.ingest_pdfs", return_value={
            "status": "success",
            "files_processed": 5,
            "total_pages": 20,
            "total_chunks": 80,
        }):
            response = client.post("/ingest")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
