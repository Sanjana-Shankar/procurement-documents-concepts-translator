"""FastAPI routes for the procurement chatbot."""

from __future__ import annotations

import logging

import requests
from fastapi import APIRouter, HTTPException

from backend.app.schemas.chatbot import ChatbotQueryRequest, ChatbotQueryResponse
from backend.app.services.chatbot_service import ask_chatbot

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/query", response_model=ChatbotQueryResponse)
async def query_chatbot(payload: ChatbotQueryRequest) -> ChatbotQueryResponse:
    """Relay the question to the Pathway RAG backend."""

    try:
        return ask_chatbot(payload)
    except requests.HTTPError as exc:  # type: ignore[attr-defined]
        status_code = exc.response.status_code if exc.response else 502
        detail = exc.response.text if exc.response else str(exc)
        logger.exception("Chatbot HTTP error: %s", detail)
        raise HTTPException(status_code=status_code, detail=detail)
    except requests.RequestException as exc:
        logger.exception("Chatbot request failure: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))
