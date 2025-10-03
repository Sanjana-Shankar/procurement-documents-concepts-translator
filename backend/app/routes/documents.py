from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from backend.app.services.landingai_service import extract_document_data
from typing import List, Dict
from pydantic import BaseModel
from landingai_ade import LandingAIADE
import os
from pathlib import Path
from landingai_ade.types import ExtractResponse
import tempfile
import pathway as pw
import asyncio
import json

router = APIRouter()
'''
@router.post("/documents/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    Step 1: Extract line items from document using LandingAI.
    """
    file_bytes = await file.read()
    document_data = extract_document_data(file_bytes)
    return document_data
'''
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
    amount: int

# Initialize ADE client
client = LandingAIADE(apikey=LANDINGAI_API_KEY)

from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
import os

router = APIRouter()

@router.post("/document/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    Upload a business document (invoice, receipt, etc.) and return normalized JSON.
    """
    # Generate unique temporary file path
    temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"

    try:
        # Save the uploaded file to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call your LandingAI ADE pipeline
        result = extract_document_data(temp_file_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document extraction failed: {e}")

    finally:
        # Always clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def pathway_normalize(extracted_data):
    # Build table
    t = pw.debug.table_from_rows(
        schema=LineItemSchema,
        rows=[(item["description"], item["amount"]) for item in extracted_data]
    )

    # Example: add normalization rule
    normalized = t.select(
        description=t.description,
        amount=t.amount,
        category=pw.when(
            t.description.isin(["Freight", "Shipping", "Logistics"]),
            "Transportation"
        ).when(
            t.description.isin(["Consulting", "Advisory", "Professional Services"]),
            "Professional Services"
        ).otherwise("Other")
    )

    # Collect results into Pandas
    df = pw.debug.to_dataframe(normalized)
    pw.run()  # execute pipeline

    return df

@router.post("/document/normalize")
async def normalize_invoice_pathway(request: Request):
    body = await request.json()
    extracted_data = body.get("line_items", [])

    df = pathway_normalize(extracted_data)
    return df.to_dict(orient="records")

''''
def pathway_normalize(extracted_data):
    # Build table with schema
    t = pw.debug.table_from_rows(
        schema=LineItemSchema,
        rows=[(item["description"], item["amount"]) for item in extracted_data]
    )

    # Select normalized output
    normalized = t.select(
        description=t.description,
        amount=t.amount
    )

    return normalized


@router.post("/document/normalize")
async def normalize_invoice_pathway(request: Request):
    body = await request.json()
    extracted_data = body.get("extracted_data", [])

    # Get Pathway table
    normalized = pathway_normalize(extracted_data)

    # Streaming generator
    async def event_stream():
        q = normalized.subscribe()
        async for update in q:
            # update is a dictionary of row_id → dict of column values
            for _, row in update.items():
                yield json.dumps(row) + "\n"

    return StreamingResponse(event_stream(), media_type="application/json")

def pathway_normalize(extracted_json: dict):
    # Convert dict line items into tuples
    rows = [(item["description"], item["amount"]) for item in extracted_json["line_items"]]

    # Convert extracted JSON into Pathway table
    class LineItemSchema(pw.Schema):
        description: str
        amount: float

    t = pw.debug.table_from_rows(
        rows=rows,
        schema=LineItemSchema
    )

    # Apply concept normalization operator
    # This can be LLM-based (e.g. OpenAI/GPT), or Pathway embeddings + clustering
    normalized = pw.normalize(
        t,
        column="description",
        target_column="category",
        method="llm",  # or "embedding"
        model="gpt-4o-mini",  # for example
        instructions="Map business line items to standardized categories"
    )

    # Aggregate by category
    grouped = normalized.groupby("category").reduce(
        pw.this.amount.sum()
    )

    return grouped.as_dict()

def pathway_normalize(extracted_json: dict):
    # Convert dict line items into tuples
    rows = [(item["description"], item["amount"]) for item in extracted_json["line_items"]]

    # Define schema
    class LineItemSchema(pw.Schema):
        description: str
        amount: float

    # Build Pathway table
    t = pw.debug.table_from_rows(
        rows=rows,
        schema=LineItemSchema
    )

    # Example: just collect results back into Python
    result = [{"description": r.description, "amount": r.amount} for r in t]
    return result

@router.post("/document/normalize")
async def normalize_invoice_pathway(extracted_data: dict):
    """
    Normalizes invoice data into categories using Pathway pipeline.
    """
    normalized_output = pathway_normalize(extracted_data)
    return {
        "invoice_id": extracted_data.get("invoice_id"),
        "line_items": normalized_output
    }
'''

