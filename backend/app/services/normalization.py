import requests
import os
from dotenv import load_dotenv

load_dotenv()

LANDINGAI_API_KEY = os.getenv("LANDINGAI_API_KEY")
BASE_URL = "https://api.va.landing.ai/v1/ade"
PATHWAY_API_URL: str = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")

HEADERS = {
    "Authorization": f"Basic {LANDINGAI_API_KEY}"
}

if not LANDINGAI_API_KEY:
    raise ValueError("❌ Missing LANDINGAI_API_KEY in .env file")

def extract_document_data(file_bytes: bytes) -> dict:
    """
    Calls LandingAI ADE Parse API to parse invoice into Markdown,
    then ADE Extract API to pull structured line items.
    """
    headers = {"Authorization": f"Bearer {LANDINGAI_API_KEY}"}

    # Step 1: Parse PDF → Markdown
    parse_resp = requests.post(
        f"{BASE_URL}/parse",
        headers=headers,
        files={"document": ("invoice.pdf", file_bytes, "application/pdf")}
    )
    parse_resp.raise_for_status()
    markdown_output = parse_resp.text  # ADE Parse returns markdown

    # Step 2: Extract schema-driven JSON from Markdown
    schema = {
        "type": "object",
        "properties": {
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"}
                    },
                    "required": ["description", "amount"]
                }
            }
        },
        "required": ["line_items"]
    }

    extract_resp = requests.post(
        f"{BASE_URL}/extract",
        headers=headers,
        files={
            "schema": ("schema.json", str(schema), "application/json"),
            "markdown": ("parsed.md", markdown_output, "text/markdown"),
        },
    )
    extract_resp.raise_for_status()
    return extract_resp.json()

def normalize_document_data(invoice_json: dict) -> dict:
    """
    Sends document JSON to Pathway ADE Extract + ADE Parse
    for normalization of categories/entities.
    """

    # Step 1: Extract entities with ADE Extract
    extract_url = f"{PATHWAY_API_URL}/extract"
    extract_resp = requests.post(
        extract_url,
        headers=HEADERS,
        json={"data": invoice_json}
    )
    extract_resp.raise_for_status()
    extracted = extract_resp.json()

    # Step 2: Parse entities with ADE Parse
    parse_url = f"{PATHWAY_API_URL}/parse"
    parse_resp = requests.post(
        parse_url,
        headers=HEADERS,
        json={"data": extracted}
    )
    parse_resp.raise_for_status()
    normalized = parse_resp.json()

    return normalized