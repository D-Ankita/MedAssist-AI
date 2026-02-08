"""
Agentic Routing Layer for MedAssist AI — powered by LangGraph.

Uses a LangGraph StateGraph to route user queries through a stateful workflow:
1. classify  → Determine intent (ANSWER / CLARIFY / ESCALATE)
2. escalate  → Return emergency services guidance
3. clarify   → Ask a follow-up question
4. answer    → Run RAG pipeline for a grounded response
"""

from __future__ import annotations

import re
from typing import List, Optional, TypedDict

from langgraph.graph import StateGraph, END

from chain import MedAssistChain


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "cannot breathe",
    "difficulty breathing", "shortness of breath", "choking",
    "severe bleeding", "hemorrhage", "unconscious", "unresponsive",
    "seizure", "convulsion", "stroke", "anaphylaxis", "allergic reaction",
    "overdose", "poisoning", "suicidal", "suicide", "self-harm",
    "severe burn", "head injury", "broken bone", "fracture",
    "loss of consciousness", "fainting", "collapsed",
]

AMBIGUOUS_PATTERNS = [
    r"^(what|tell me) about .{3,10}$",
    r"^(it|this|that|the thing)\b",
    r"\bor\b.*\bor\b",
]

ESCALATION_RESPONSE = (
    "⚠️ **This sounds like it could be a medical emergency.**\n\n"
    "Please take immediate action:\n"
    "- **Call emergency services:** 911 (US), 999 (UK), 112 (EU)\n"
    "- Go to your nearest emergency room\n"
    "- If someone is with you, ask them to help while you call\n\n"
    "Do not wait — getting professional help quickly is critical."
)

CLARIFICATIONS = {
    "diabetes": "Could you clarify — are you asking about Type 1 diabetes, Type 2 diabetes, or gestational diabetes? This will help me find the most relevant information.",
    "pain": "I'd like to help! Could you describe where you're experiencing pain and how long it's been going on? This will help me find relevant information.",
    "medication": "Could you specify which medication you're asking about? Or are you looking for general information about a type of medication?",
    "vaccine": "Are you asking about a specific vaccine (e.g., COVID-19, flu, HPV), or would you like general information about vaccinations?",
    "cancer": "Cancer is a broad topic. Could you specify which type of cancer you'd like to learn about, or what aspect (symptoms, screening, treatment options)?",
}


# ---------------------------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------------------------

class AgentState(TypedDict):
    query: str
    chat_history: list
    intent: str
    answer: str
    sources: list
    chunks_retrieved: int
    relevance_scores: list


# ---------------------------------------------------------------------------
# Graph Nodes
# ---------------------------------------------------------------------------

def classify_intent(state: AgentState) -> AgentState:
    """Classify the user query into ESCALATE / CLARIFY / ANSWER."""
    query_lower = state["query"].lower().strip()

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in query_lower:
            return {**state, "intent": "ESCALATE"}

    if len(query_lower.split()) < 3:
        return {**state, "intent": "CLARIFY"}

    for pattern in AMBIGUOUS_PATTERNS:
        if re.search(pattern, query_lower):
            return {**state, "intent": "CLARIFY"}

    return {**state, "intent": "ANSWER"}


def handle_escalation(state: AgentState) -> AgentState:
    """Return emergency guidance."""
    return {
        **state,
        "answer": ESCALATION_RESPONSE,
        "sources": [],
        "chunks_retrieved": 0,
        "relevance_scores": [],
    }


def handle_clarification(state: AgentState) -> AgentState:
    """Generate a clarifying follow-up question."""
    query_lower = state["query"].lower().strip()

    for keyword, clarification in CLARIFICATIONS.items():
        if keyword in query_lower:
            return {**state, "answer": clarification, "sources": [], "chunks_retrieved": 0, "relevance_scores": []}

    fallback = (
        f"I'd like to help with your question about \"{state['query']}\", but I need "
        f"a bit more detail to find the best information. Could you provide "
        f"more specifics about what you'd like to know?"
    )
    return {**state, "answer": fallback, "sources": [], "chunks_retrieved": 0, "relevance_scores": []}


def handle_answer(state: AgentState) -> AgentState:
    """Run the full RAG pipeline via MedAssistChain."""
    chain = _get_chain()
    result = chain.query(state["query"], state["chat_history"] or None)
    return {
        **state,
        "answer": result["answer"],
        "sources": result["sources"],
        "chunks_retrieved": result["chunks_retrieved"],
        "relevance_scores": result["relevance_scores"],
    }


# ---------------------------------------------------------------------------
# Routing function
# ---------------------------------------------------------------------------

def route_by_intent(state: AgentState) -> str:
    """Route to the appropriate handler based on classified intent."""
    intent = state["intent"]
    if intent == "ESCALATE":
        return "escalate"
    if intent == "CLARIFY" and not state.get("chat_history"):
        return "clarify"
    # If CLARIFY but has chat history, fall through to answer
    return "answer"


# ---------------------------------------------------------------------------
# Build the LangGraph workflow
# ---------------------------------------------------------------------------

def _build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("classify", classify_intent)
    workflow.add_node("escalate", handle_escalation)
    workflow.add_node("clarify", handle_clarification)
    workflow.add_node("answer", handle_answer)

    workflow.set_entry_point("classify")
    workflow.add_conditional_edges(
        "classify",
        route_by_intent,
        {"escalate": "escalate", "clarify": "clarify", "answer": "answer"},
    )
    workflow.add_edge("escalate", END)
    workflow.add_edge("clarify", END)
    workflow.add_edge("answer", END)

    return workflow.compile()


# Module-level compiled graph (lazy-initialized)
_graph = None
_chain_instance = None


def _get_chain() -> MedAssistChain:
    global _chain_instance
    if _chain_instance is None:
        _chain_instance = MedAssistChain()
    return _chain_instance


def _get_graph():
    global _graph
    if _graph is None:
        _graph = _build_graph()
    return _graph


# ---------------------------------------------------------------------------
# Public API  (MedAssistAgent keeps the same interface as before)
# ---------------------------------------------------------------------------

class MedAssistAgent:
    """
    Agent that processes user queries through a LangGraph workflow.

    The graph routes queries to one of three paths:
    - ANSWER:   Use RAG pipeline to answer from medical docs
    - CLARIFY:  Ask the user to provide more details
    - ESCALATE: Direct to emergency services
    """

    def __init__(self):
        self.chain = _get_chain()
        self._graph = _get_graph()

    def classify_intent(self, query: str) -> str:
        """Classify intent without running the full graph (useful for testing)."""
        result = classify_intent({
            "query": query, "chat_history": [], "intent": "",
            "answer": "", "sources": [], "chunks_retrieved": 0, "relevance_scores": [],
        })
        return result["intent"]

    def process_query(
        self,
        query: str,
        chat_history: Optional[List[dict]] = None,
    ) -> dict:
        """
        Process a user query through the LangGraph agent workflow.

        Args:
            query: The user's question
            chat_history: Previous conversation messages

        Returns:
            Dict with intent, answer, sources, chunks_retrieved, relevance_scores
        """
        initial_state: AgentState = {
            "query": query,
            "chat_history": chat_history or [],
            "intent": "",
            "answer": "",
            "sources": [],
            "chunks_retrieved": 0,
            "relevance_scores": [],
        }

        result = self._graph.invoke(initial_state)

        return {
            "intent": result["intent"],
            "answer": result["answer"],
            "sources": result["sources"],
            "chunks_retrieved": result["chunks_retrieved"],
            "relevance_scores": result["relevance_scores"],
        }
