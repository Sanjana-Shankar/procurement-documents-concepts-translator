import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LANDINGAI_API_KEY: str = os.getenv("LANDINGAI_API_KEY", "eWxyNXFyYThkOGhzOGJ6aGZxMGUzOm56RTg5UU1SVlpwT2Z4UEF5SHJ5OW9PQ1BRejYyS2Vy")
PATHWAY_API_URL: str = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")

def normalize_document_data(invoice_json: dict) -> dict:
    """
    Sends document data to Pathway DPT-2 ADE Extract + ADE Parse pipeline
    for category normalization.
    """

    # ADE Extract: extract structured concepts/entities
    extract_resp = requests.post(
        f"{PATHWAY_API_URL}/ade/extract",
        json={"data": invoice_json}
    )
    extract_resp.raise_for_status()
    extracted = extract_resp.json()

    # ADE Parse: normalize categories/entities
    parse_resp = requests.post(
        f"{PATHWAY_API_URL}/ade/parse",
        json={"data": extracted}
    )
    parse_resp.raise_for_status()
    normalized = parse_resp.json()

    return normalized
