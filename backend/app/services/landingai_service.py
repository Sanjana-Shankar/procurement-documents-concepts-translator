import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from landingai_ade import LandingAIADE
from landingai_ade.types import ExtractResponse, ParseResponse
from landingai_ade.lib import pydantic_to_json_schema

# Load environment variables
load_dotenv()

key = os.getenv("LANDINGAI_API_KEY")
print("KEY:", repr(key))

LANDINGAI_API_KEY = os.getenv("LANDINGAI_API_KEY")
PATHWAY_API_URL: str = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")

print("DEBUG API KEY:", LANDINGAI_API_KEY[:5] if LANDINGAI_API_KEY else None)

if not LANDINGAI_API_KEY:
    raise ValueError("❌ Missing LANDINGAI_API_KEY in .env file")

BASE_URL = "https://api.landing.ai/v1/ade"  # correct LandingAI API base

HEADERS = {
    "Authorization": f"Basic {LANDINGAI_API_KEY}"
}

# Initialize ADE client
client = LandingAIADE(apikey=LANDINGAI_API_KEY)

# -----------------------------
# Define schema using Pydantic
# -----------------------------
class InvoiceItem(BaseModel):
    quantity: float = Field(description="Item quantity, typically hours")
    service: str = Field(description="The service performed.")
    rate: str = Field(description="The rate per unit of quantity.")
    total: str = Field(description="The total cost for the item.")

class Invoice(BaseModel):
    invoice_number: str = Field(description="The invoice number.")
    invoice_date: str = Field(description="The invoice date.")
    total_due: float = Field(description="The total amount due.")
    itemized_invoice: list[InvoiceItem]


# -----------------------------
# Pipeline functions
# -----------------------------
def parse_document(file_path: str, model: str = "dpt-2-latest") -> ParseResponse:
    """Parse a document into markdown using DPT-2."""
    response = client.parse(document=Path(file_path), model=model)
    return response

def extract_schema(markdown_path: str, schema_class: BaseModel) -> ExtractResponse:
    """Extract structured data from parsed markdown given a schema."""
    json_schema = pydantic_to_json_schema(schema_class)
    response = client.extract(schema=json_schema, markdown=Path(markdown_path))
    return response


# -----------------------------
# Entry point for FastAPI route
# -----------------------------
def extract_document_data(file_path: str) -> dict:
    """
    Full ADE normalization pipeline using DPT-2:
    1. Parse document -> Markdown
    2. Extract fields -> JSON
    """
    print("Starting normalization...")
    # Step 1: Parse PDF → Markdown
    parse_result = parse_document(file_path)
    markdown_file = "parsed-output.md"
    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write(parse_result.markdown)

    # Step 2: Extract JSON based on schema
    extraction_result = extract_schema(markdown_file, Invoice)
    print("Finished normalization")
    return {
        "extraction": extraction_result.extraction,
        "metadata": extraction_result.extraction_metadata
    }




