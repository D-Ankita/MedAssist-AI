"""Tests for the MedAssist RAG chain."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from langchain.schema import SystemMessage, HumanMessage


class TestBuildPrompt:
    def test_returns_system_and_human_messages(self, mock_chain):
        messages = mock_chain.build_prompt(
            question="What is diabetes?",
            context="Diabetes is a chronic disease.",
        )
        assert len(messages) == 2
        assert isinstance(messages[0], SystemMessage)
        assert isinstance(messages[1], HumanMessage)
        assert messages[1].content == "What is diabetes?"

    def test_includes_context_in_system_message(self, mock_chain):
        messages = mock_chain.build_prompt(
            question="What is diabetes?",
            context="Diabetes is a chronic disease.",
        )
        assert "Diabetes is a chronic disease." in messages[0].content

    def test_includes_chat_history(self, mock_chain):
        history = [
            {"role": "user", "content": "Tell me about diabetes"},
            {"role": "assistant", "content": "Diabetes is a metabolic disease."},
        ]
        messages = mock_chain.build_prompt(
            question="What about symptoms?",
            context="Symptoms include thirst.",
            chat_history=history,
        )
        assert "Patient: Tell me about diabetes" in messages[0].content
        assert "MedAssist: Diabetes is a metabolic disease." in messages[0].content

    def test_no_history_shows_default(self, mock_chain):
        messages = mock_chain.build_prompt(
            question="What is diabetes?",
            context="Context here.",
        )
        assert "No previous conversation." in messages[0].content


class TestQuery:
    def test_returns_expected_structure(self, mock_chain):
        result = mock_chain.query("What is diabetes?")
        assert "answer" in result
        assert "sources" in result
        assert "chunks_retrieved" in result
        assert "relevance_scores" in result

    def test_returns_answer_from_llm(self, mock_chain):
        result = mock_chain.query("What is diabetes?")
        assert "Diabetes" in result["answer"]

    def test_returns_correct_chunk_count(self, mock_chain):
        result = mock_chain.query("What is diabetes?")
        assert result["chunks_retrieved"] == 2

    def test_returns_relevance_scores(self, mock_chain):
        result = mock_chain.query("What is diabetes?")
        assert result["relevance_scores"] == [0.91, 0.85]


class TestExtractSources:
    def test_extracts_unique_sources(self, mock_chain):
        from retriever import RetrievedChunk

        chunks = [
            RetrievedChunk(content="a", source="doc.pdf", page=0, relevance_score=0.9),
            RetrievedChunk(content="b", source="doc.pdf", page=0, relevance_score=0.8),
            RetrievedChunk(content="c", source="doc.pdf", page=1, relevance_score=0.7),
        ]
        sources = mock_chain._extract_sources(chunks)
        # Page 0 appears twice but should only be listed once
        assert len(sources) == 2
        assert sources[0]["page"] == 1  # page 0 + 1
        assert sources[1]["page"] == 2  # page 1 + 1

    def test_strips_path_from_source(self, mock_chain):
        from retriever import RetrievedChunk

        chunks = [
            RetrievedChunk(
                content="text",
                source="/data/knowledge_base/Diabetes-Overview.pdf",
                page=0,
                relevance_score=0.9,
            ),
        ]
        sources = mock_chain._extract_sources(chunks)
        assert sources[0]["document"] == "Diabetes-Overview.pdf"


class TestInvokeWithRetry:
    def test_succeeds_on_first_attempt(self, mock_chain):
        answer = mock_chain._invoke_with_retry([HumanMessage(content="test")])
        assert "Diabetes" in answer

    def test_retries_on_failure_then_succeeds(self, mock_chain):
        mock_chain.llm.invoke.side_effect = [
            Exception("API timeout"),
            MagicMock(content="Recovery answer"),
        ]
        with patch("chain.time.sleep"):
            answer = mock_chain._invoke_with_retry([HumanMessage(content="test")])
        assert answer == "Recovery answer"
        assert mock_chain.llm.invoke.call_count == 2

    def test_raises_after_max_retries(self, mock_chain):
        mock_chain.llm.invoke.side_effect = Exception("Persistent failure")
        from chain import LLMCallError
        with patch("chain.time.sleep"), pytest.raises(LLMCallError):
            mock_chain._invoke_with_retry([HumanMessage(content="test")])
        assert mock_chain.llm.invoke.call_count == 3
