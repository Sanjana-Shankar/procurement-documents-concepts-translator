from fastapi import FastAPI
from backend.app.routes import documents  # adjust the import if documents.py is in another folder

app = FastAPI(
    title="Finance Document Processor",
    version="1.0.0",
    description="Extracts and normalizes financial documents using LandingAI + Pathway"
)

# Include your documents router
app.include_router(documents.router, prefix="", tags=["documents"])
