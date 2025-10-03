"""Pydantic models for chatbot interactions."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, root_validator


class ChatbotQueryRequest(BaseModel):
    """Incoming question payload from the frontend."""

    question: str = Field(..., min_length=1, description="Natural language question for the chatbot")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Identifier to maintain conversation context on the RAG backend",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata forwarded to the RAG pipeline",
    )

    @root_validator
    def _strip_question(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        question = values.get("question")
        if question:
            stripped = question.strip()
            if not stripped:
                raise ValueError("question must be a non-empty string")
            values["question"] = stripped
        return values


class ChatbotQueryResponse(BaseModel):
    """Structured response returned to API clients."""

    question: str
    answer: str
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    raw: Dict[str, Any] = Field(default_factory=dict, description="Verbatim payload from the RAG backend")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
