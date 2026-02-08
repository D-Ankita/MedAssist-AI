"""Tests for the MedAssist agent routing layer."""

from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

from agent import (
    classify_intent,
    handle_escalation,
    handle_clarification,
    route_by_intent,
    ESCALATION_RESPONSE,
    MedAssistAgent,
)


# ---------------------------------------------------------------------------
# Intent classification
# ---------------------------------------------------------------------------

def _make_state(query: str, chat_history: list | None = None) -> dict:
    return {
        "query": query,
        "chat_history": chat_history or [],
        "intent": "",
        "answer": "",
        "sources": [],
        "chunks_retrieved": 0,
        "relevance_scores": [],
    }


class TestClassifyIntent:
    @pytest.mark.parametrize("query", [
        "I'm having chest pain",
        "my friend is choking on food",
        "I think I'm having a heart attack",
        "someone is unconscious",
        "severe bleeding from a wound",
        "I feel suicidal",
    ])
    def test_emergency_queries_return_escalate(self, query: str):
        result = classify_intent(_make_state(query))
        assert result["intent"] == "ESCALATE"

    @pytest.mark.parametrize("query", [
        "hi",
        "pain",
        "what about diabetes or cancer or flu",
    ])
    def test_ambiguous_queries_return_clarify(self, query: str):
        result = classify_intent(_make_state(query))
        assert result["intent"] == "CLARIFY"

    @pytest.mark.parametrize("query", [
        "What are the symptoms of type 2 diabetes?",
        "How do I treat a cold at home?",
        "What is the normal blood pressure range?",
    ])
    def test_normal_queries_return_answer(self, query: str):
        result = classify_intent(_make_state(query))
        assert result["intent"] == "ANSWER"


# ---------------------------------------------------------------------------
# Escalation handler
# ---------------------------------------------------------------------------

class TestHandleEscalation:
    def test_returns_escalation_response(self):
        state = _make_state("chest pain")
        state["intent"] = "ESCALATE"
        result = handle_escalation(state)
        assert result["answer"] == ESCALATION_RESPONSE
        assert result["sources"] == []
        assert result["chunks_retrieved"] == 0


# ---------------------------------------------------------------------------
# Clarification handler
# ---------------------------------------------------------------------------

class TestHandleClarification:
    def test_diabetes_clarification(self):
        state = _make_state("diabetes")
        result = handle_clarification(state)
        assert "Type 1" in result["answer"]
        assert "Type 2" in result["answer"]

    def test_generic_clarification(self):
        state = _make_state("xyz")
        result = handle_clarification(state)
        assert "more detail" in result["answer"]


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

class TestRouteByIntent:
    def test_escalate_routes_to_escalate(self):
        state = _make_state("chest pain")
        state["intent"] = "ESCALATE"
        assert route_by_intent(state) == "escalate"

    def test_clarify_no_history_routes_to_clarify(self):
        state = _make_state("hi")
        state["intent"] = "CLARIFY"
        assert route_by_intent(state) == "clarify"

    def test_clarify_with_history_routes_to_answer(self):
        state = _make_state("hi", chat_history=[{"role": "user", "content": "hello"}])
        state["intent"] = "CLARIFY"
        assert route_by_intent(state) == "answer"

    def test_answer_routes_to_answer(self):
        state = _make_state("What are diabetes symptoms?")
        state["intent"] = "ANSWER"
        assert route_by_intent(state) == "answer"


# ---------------------------------------------------------------------------
# MedAssistAgent integration (with mocked chain)
# ---------------------------------------------------------------------------

class TestMedAssistAgent:
    @patch("agent._get_chain")
    @patch("agent._get_graph")
    def test_classify_intent_method(self, mock_graph, mock_chain):
        agent = MedAssistAgent.__new__(MedAssistAgent)
        agent.chain = mock_chain
        agent._graph = mock_graph

        assert agent.classify_intent("I have chest pain") == "ESCALATE"
        assert agent.classify_intent("What are cold symptoms and remedies?") == "ANSWER"
