from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from backend.app.services.landingai_service import extract_document_data
from typing import List, Dict, Optional
from pydantic import BaseModel
from landingai_ade import LandingAIADE
import os
from pathlib import Path
from landingai_ade.types import ExtractResponse
import tempfile
import pathway as pw
import asyncio
import json
from openai import OpenAI
from google import generativeai  # or whatever the SDK name is
import requests
from backend.app.routes.chatbot import NORMALIZED_SPEND_DATA

# Configure client
generativeai.configure(api_key=os.getenv("GEMINI_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

LANDINGAI_API_KEY = os.getenv("LANDINGAI_API_KEY")
PATHWAY_API_URL: str = os.getenv("PATHWAY_API_URL", "http://127.0.0.1:8000")

#Models 
class LineItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    invoice_id: str
    line_items: List[LineItem]

class InvoiceRequest(BaseModel):
    invoice_id: str
    line_items: list[LineItem]

class NormalizedLineItem(BaseModel):
    category: str
    amount: float

class NormalizedInvoice(BaseModel):
    invoice_id: str
    line_items: List[NormalizedLineItem]

class LineItemSchema(pw.Schema):
    description: str
    amount: float
    category: str

# Initialize ADE client
client = LandingAIADE(apikey=LANDINGAI_API_KEY)

from fastapi import APIRouter, UploadFile, File, HTTPException, FastAPI
import shutil
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Finance Document Processor",
    version="1.0.0",
    description="Extracts and normalizes financial documents using LandingAI + Pathway"
)

#NORMALIZED_SPEND_DATA = []
router = APIRouter()

# Input model for each spend entry
class SpendEntry(BaseModel):
    description: str
    amount: float
    category: str
    spend_type: str

class SpendEntryWithThreshold(SpendEntry):
    threshold: float
    is_over_budget: bool
    explanation: str | None = None


# --- Route ---
@router.post("/spend/check-thresholds", response_model=List[SpendEntryWithThreshold])
async def check_spend_thresholds(entries: List[SpendEntry]):
    """
    Dynamically infers realistic spending thresholds per category using Gemini 1.5.
    """
    enriched_entries = []

    for entry in entries:
        prompt = f"""
        You are a financial benchmark analyst.
        Given this spending entry:
        - Description: {entry.description}
        - Amount: {entry.amount}
        - Category: {entry.category}
        - Spend Type: {entry.spend_type}

        Task:
        1. Estimate a realistic upper spending threshold (numeric value in USD)
           for this type of expense based on industry averages.
        2. Make it such that at least some of the thresholds are lower than the numeric values in the invoices but not all of the items in the documents as overspending.
        2. Return only a JSON object:
           {{
             "threshold": <number>,
             "reason": "<short explanation>"
           }}
        """

        try:
            # --- Call Gemini model safely ---
            model = generativeai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            print(f"Response from GEMINI: {response}")

            raw_text = response.text.strip()

            # --- Parse model output to JSON ---
            try:
                threshold_info = json.loads(raw_text)
            except json.JSONDecodeError:
                import re
                match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                threshold_info = json.loads(match.group(0)) if match else {}

            threshold = float(threshold_info.get("threshold", 1000))
            print(f"Threshold: {threshold}")
            reason = threshold_info.get("reason", "No reason provided")

        except Exception as e:
            print(f"⚠️ Gemini threshold fetch failed for {entry.category}: {e}")
            threshold = 1000
            reason = "Default threshold used due to Gemini API failure."

        # --- Compare threshold ---
        is_over_budget = entry.amount > threshold
        explanation = (
            f"Spending for '{entry.description}' in category '{entry.category}' "
            f"exceeds threshold (${threshold:.2f}). Reason: {reason}"
            if is_over_budget
            else None
        )
        print(f"Explanation: {explanation}")

        enriched_entries.append(
            SpendEntryWithThreshold(
                **entry.model_dump(),
                is_over_budget=is_over_budget,
                threshold=threshold,
                explanation=explanation,
            )
        )
        print("Enriched Entries:")
        for e in enriched_entries:
            print(e.model_dump())

    return enriched_entries

# Enable CORS so your React frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/document/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    Upload a business document (invoice, receipt, etc.) and return normalized JSON.
    """
    # Generate unique temporary file path
    print("Entered in API key ")
    temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"

    try:
        # Save the uploaded file to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call your LandingAI ADE pipeline
        result = extract_document_data(temp_file_path)
        print(f"Extracted text: {result}")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document extraction failed: {e}")

    finally:
        # Always clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def parse_amount(value):
    """
    Safely convert messy string amounts like '€130,00', '$1,200.50', or '1.000,00 €'
    into a clean float. Returns 0.0 if parsing fails.
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    # Convert to string and clean up currency symbols and separators
    s = str(value)
    s = s.replace("€", "").replace("$", "").replace("£", "")
    s = s.replace("USD", "").replace("EUR", "")
    s = s.replace(" ", "").strip()

    # Replace comma with dot only if comma is used as decimal separator
    if "," in s and "." not in s:
        s = s.replace(",", ".")

    # Remove thousand separators (e.g., "1.000,00" → "1000.00")
    s = s.replace(",", "")

    try:
        return float(s)
    except ValueError:
        print(f"[WARN] Could not parse amount: {value}")
        return 0.0

# Workflow: Once information is extracted from the document, using openAI to categorize many terms into certain important business categories and using pathway to create proper neat clean tables 

def categorize_line_items_with_gemini(extracted_data):
    """
    Uses Gemini API to infer categories for each line item.
    """
    categorized_items = []

    # Build a single batched prompt to reduce API calls
    descriptions = [item["description"] for item in extracted_data]
    amounts = [item["amount"] for item in extracted_data]

    prompt = "You are a financial categorize assistant. For each of the following items, give a category meanwhile keeping the same price of each item listed in the input document.\n"
    for desc, amt in zip(descriptions, amounts):
        prompt += f"- Description: \"{desc}\", Amount: {amt}\n"
    prompt += "\nRespond with JSON in this format:\n"
    prompt += "[ { \"description\": ..., \"amount\": ..., \"category\": ... }, ... ]"

    try:
        response = generativeai.models.generate_content(
            model="gemini-2.5-flash",  # or whatever model version
            contents=[prompt]
        )
        resp_text = response.candidates[0].content.parts[0].text
        # Parse JSON from resp_text
        parsed = json.loads(resp_text)
        for item in parsed:
            categorized_items.append(item)
    except Exception as e:
        print("Gemini error:", e)
        # fallback: categorize everything as “Other”
        for item in extracted_data:
            categorized_items.append({
                "description": item["description"],
                "amount": item["amount"],
                "category": "Other"
            })

    print(f"Categorized items (Gemini): {categorized_items}")
    return categorized_items


def pathway_normalize(extracted_data):
    """
    Normalize spend data using Pathway pipeline, after OpenAI categorization.
    """
    categorized_data = categorize_line_items_with_gemini(extracted_data)
    print(f"Categorized data inside pathway_normalize: {categorized_data}")
    
    # ✅ Build Pathway table with Schema class
    t = pw.debug.table_from_rows(
        schema=LineItemSchema,
        rows=[(
            str(item["description"]),
            float(item["amount"]),   # ensures plain Python float
            str(item["category"])
        ) for item in categorized_data]
    )

    # Normalize & add computed field
    normalized = t.select(
        description=t.description,
        amount=t.amount,
        category=t.category,
        spend_type=pw.if_else(t.amount > 1000, "High Spend", "Regular Spend")
    )

    print(f"Normalized table schema: {normalized.schema}")
    pw.run()

    # ✅ Convert Pathway table → Pandas DataFrame (older API)
    df = pw.debug.table_to_pandas(normalized)


    print("Final normalized DataFrame:")
    print(df)

    print("✅ Categorized data inside pathway_normalize:", df.to_dict(orient="records"))

    return df

@router.post("/document/normalize")
async def normalize_invoice_pathway(request: Request):
    """
    Normalizes extracted invoice data into unified spend categories and a clean table.
    """
    try:
        print("Entered into document/normalize API endpoint")
        body = await request.json()
        print(f"Raw body of data: {body}")
        extracted_data = body.get("line_items", {})
        print(f"Extracted data: {extracted_data}")

        # Extract line items properly
        itemized = extracted_data.get("extraction", {}).get("itemized_invoice", [])
        if not itemized:
            raise HTTPException(status_code=400, detail="No itemized line items found")

        # Transform into the normalized format expected by pathway_normalize
        line_items = []
        for item in itemized:
            desc = item.get("service") or item.get("description") or "Unknown"
            amt = item.get("total") or item.get("amount") or "$0.00"

            amt_value = parse_amount(amt)

            line_items.append({
                "description": desc,
                "amount": amt_value
            })

        print(f"Prepared {len(line_items)} line items for normalization: {line_items}")
        # ✅ Store normalized data globally for chatbot
        #NORMALIZED_SPEND_DATA.clear()
        #NORMALIZED_SPEND_DATA.extend(line_items)

        df = pathway_normalize(line_items)
        print(f"Normalized categories and clean table: {df.to_dict(orient='records')}")
        #set_spend_data(df.to_dict(orient="records"))
        NORMALIZED_SPEND_DATA.clear()
        NORMALIZED_SPEND_DATA.extend(df.to_dict(orient="records"))
        return df.to_dict(orient="records")

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Normalization failed: {e}")