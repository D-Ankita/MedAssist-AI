"""Shared fixtures for MedAssist AI tests."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure the ai-service package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture()
def mock_retriever():
    """Return a mocked MedAssistRetriever that returns canned chunks."""
    from retriever import RetrievedChunk

    retriever = MagicMock()
    retriever.document_count = 42
    retriever.retrieve.return_value = [
        RetrievedChunk(
            content="Diabetes is a chronic metabolic disease.",
            source="Diabetes-Overview.pdf",
            page=0,
            relevance_score=0.91,
        ),
        RetrievedChunk(
            content="Type 2 diabetes accounts for 90-95% of cases.",
            source="Diabetes-Overview.pdf",
            page=1,
            relevance_score=0.85,
        ),
    ]
    retriever.format_context.return_value = (
        "[Source 1: Diabetes-Overview.pdf, Page 1]\n"
        "Diabetes is a chronic metabolic disease.\n\n---\n\n"
        "[Source 2: Diabetes-Overview.pdf, Page 2]\n"
        "Type 2 diabetes accounts for 90-95% of cases."
    )
    return retriever


@pytest.fixture()
def mock_llm():
    """Return a mocked LLM that returns a canned response."""
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(
        content="Diabetes is a chronic condition affecting blood sugar levels. "
        "According to Diabetes-Overview.pdf, it accounts for significant health burden worldwide."
    )
    return llm


@pytest.fixture()
def mock_chain(mock_retriever, mock_llm):
    """Return a MedAssistChain with mocked retriever and LLM."""
    with patch("chain.MedAssistRetriever", return_value=mock_retriever), \
         patch("chain.get_system_prompt", return_value="System: {context}\n{chat_history}\n{question}"):
        from chain import MedAssistChain
        chain = MedAssistChain.__new__(MedAssistChain)
        chain.retriever = mock_retriever
        chain.llm = mock_llm
        chain.system_prompt_template = "System: {context}\n{chat_history}\n{question}"
        return chain
