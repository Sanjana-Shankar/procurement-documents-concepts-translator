import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LANDINGAI_API_KEY: str = os.getenv("LANDINGAI_API_KEY", "eWxyNXFyYThkOGhzOGJ6aGZxMGUzOm56RTg5UU1SVlpwT2Z4UEF5SHJ5OW9PQ1BRejYyS2Vy")
PATHWAY_API_URL: str = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")

if not LANDINGAI_API_KEY:
    raise ValueError("❌ Missing LANDINGAI_API_KEY in .env file")

BASE_URL = "https://api.landing.ai/v1"  # LandingAI API base


def extract_document_data(file_bytes: bytes) -> dict:
    """
    Calls LandingAI Vision API to extract structured invoice data.
    """

    headers = {"Authorization": f"Bearer {LANDINGAI_API_KEY}"}
    files = {"file": ("invoice.pdf", file_bytes, "application/pdf")}
    
    response = requests.post(
        f"{BASE_URL}/inference",
        headers=headers,
        files=files
    )
    response.raise_for_status()
    result = response.json()

    return {
        "document_id": result.get("document_id", "unknown"),
        "line_items": [
            {"description": item["description"], "amount": item["amount"]}
            for item in result.get("line_items", [])
        ]
    }
