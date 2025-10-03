"""Service layer for interacting with the procurement chatbot."""

from __future__ import annotations

from typing import Optional

from backend.chatbot import ProcurementChatbot
from backend.app.schemas.chatbot import ChatbotQueryRequest, ChatbotQueryResponse


_chatbot_client: Optional[ProcurementChatbot] = None


def _get_client() -> ProcurementChatbot:
    global _chatbot_client
    if _chatbot_client is None:
        _chatbot_client = ProcurementChatbot()
    return _chatbot_client


def ask_chatbot(payload: ChatbotQueryRequest) -> ChatbotQueryResponse:
    """Send question to Pathway RAG backend and wrap the response."""

    client = _get_client()
    result = client.ask(
        payload.question,
        conversation_id=payload.conversation_id,
        metadata=payload.metadata,
    )

    return ChatbotQueryResponse(
        question=result.get("question", payload.question),
        answer=result.get("answer", ""),
        conversation_id=result.get("conversation_id", payload.conversation_id),
        metadata=result.get("metadata"),
        raw=result,
    )
