"""Utilities for interacting with the Pathway-powered procurement chatbot."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PATHWAY_API_URL = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")
DEFAULT_CHAT_ROUTE = os.getenv("PATHWAY_CHAT_ROUTE", "/rag/query")


@dataclass(slots=True)
class ChatbotConfig:
    """Runtime configuration for the procurement chatbot client."""

    base_url: str = DEFAULT_PATHWAY_API_URL
    route: str = DEFAULT_CHAT_ROUTE
    timeout: float = 30.0

    def endpoint(self) -> str:
        route = self.route if self.route.startswith("/") else f"/{self.route}"
        return f"{self.base_url.rstrip('/')}{route}"


class ProcurementChatbot:
    """Simple HTTP client for sending questions to the Pathway RAG backend."""

    def __init__(self, config: Optional[ChatbotConfig] = None) -> None:
        self.config = config or ChatbotConfig()

    def ask(
        self,
        question: str,
        *,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not question or not question.strip():
            raise ValueError("question must be a non-empty string")

        payload: Dict[str, Any] = {"question": question}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        if metadata:
            payload["metadata"] = metadata

        response = requests.post(
            self.config.endpoint(),
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        data = response.json()

        # Ensure the client always returns a predictable payload shape.
        data.setdefault("question", question)
        data.setdefault("answer", "")
        return data


__all__ = ["ChatbotConfig", "ProcurementChatbot"]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Query the procurement chatbot")
    parser.add_argument("question", help="Question to send to the chatbot")
    parser.add_argument("--conversation-id", dest="conversation_id")
    args = parser.parse_args()

    client = ProcurementChatbot()
    result = client.ask(args.question, conversation_id=args.conversation_id)
    print(json.dumps(result, indent=2))
