"""Tests for the MedAssist vector retriever."""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from retriever import MedAssistRetriever, RetrievedChunk


# ---------------------------------------------------------------------------
# RetrievedChunk dataclass
# ---------------------------------------------------------------------------

class TestRetrievedChunk:
    def test_creation(self):
        chunk = RetrievedChunk(
            content="Sample text",
            source="test.pdf",
            page=0,
            relevance_score=0.95,
        )
        assert chunk.content == "Sample text"
        assert chunk.source == "test.pdf"
        assert chunk.page == 0
        assert chunk.relevance_score == 0.95


# ---------------------------------------------------------------------------
# format_context
# ---------------------------------------------------------------------------

class TestFormatContext:
    @patch("retriever.HuggingFaceEmbeddings")
    @patch("retriever.chromadb.PersistentClient")
    def test_format_context_with_chunks(self, mock_client, mock_embeddings):
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection

        retriever = MedAssistRetriever()
        chunks = [
            RetrievedChunk(content="Chunk one", source="doc.pdf", page=0, relevance_score=0.9),
            RetrievedChunk(content="Chunk two", source="doc.pdf", page=1, relevance_score=0.8),
        ]
        context = retriever.format_context(chunks)
        assert "[Source 1: doc.pdf, Page 1]" in context
        assert "[Source 2: doc.pdf, Page 2]" in context
        assert "Chunk one" in context
        assert "Chunk two" in context

    @patch("retriever.HuggingFaceEmbeddings")
    @patch("retriever.chromadb.PersistentClient")
    def test_format_context_empty(self, mock_client, mock_embeddings):
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection

        retriever = MedAssistRetriever()
        context = retriever.format_context([])
        assert "No relevant documents" in context


# ---------------------------------------------------------------------------
# retrieve
# ---------------------------------------------------------------------------

class TestRetrieve:
    @patch("retriever.HuggingFaceEmbeddings")
    @patch("retriever.chromadb.PersistentClient")
    def test_retrieve_returns_chunks(self, mock_client, mock_embeddings):
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "documents": [["Diabetes text", "Blood sugar text"]],
            "metadatas": [[
                {"source": "Diabetes-Overview.pdf", "page": 0},
                {"source": "Diabetes-Overview.pdf", "page": 1},
            ]],
            "distances": [[0.1, 0.2]],
        }
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 384

        retriever = MedAssistRetriever()
        chunks = retriever.retrieve("What is diabetes?")

        assert len(chunks) == 2
        assert chunks[0].relevance_score == 0.9
        assert chunks[1].relevance_score == 0.8
        assert chunks[0].source == "Diabetes-Overview.pdf"

    @patch("retriever.HuggingFaceEmbeddings")
    @patch("retriever.chromadb.PersistentClient")
    def test_retrieve_empty_collection(self, mock_client, mock_embeddings):
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 384

        retriever = MedAssistRetriever()
        chunks = retriever.retrieve("Something obscure")
        assert chunks == []

    @patch("retriever.HuggingFaceEmbeddings")
    @patch("retriever.chromadb.PersistentClient")
    def test_document_count(self, mock_client, mock_embeddings):
        mock_collection = MagicMock()
        mock_collection.count.return_value = 150
        mock_client.return_value.get_or_create_collection.return_value = mock_collection

        retriever = MedAssistRetriever()
        assert retriever.document_count == 150
