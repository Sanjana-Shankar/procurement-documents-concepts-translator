from fastapi import APIRouter, UploadFile, File
from backend.app.services.landingai_service import extract_document_data
from backend.app.services.normalization import normalize_document_data

router = APIRouter()

@router.post("/documents/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    Step 1: Extract line items from document using LandingAI.
    """
    file_bytes = await file.read()
    document_data = extract_document_data(file_bytes)
    return document_data

@router.post("/document/normalize")
async def normalize_document(invoice_json: dict):
    """
    Step 2: Normalize categories using Pathway ADE Extract + ADE Parse.
    """
    normalized_data = normalize_document_data(invoice_json)
    return normalized_data
