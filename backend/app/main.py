from fastapi import FastAPI
from backend.app.routes import documents, chatbot

app = FastAPI(
    title="Finance Document Processor",
    version="1.0.0",
    description="Extracts and normalizes financial documents using LandingAI + Pathway"
)

app.include_router(documents.router, prefix="", tags=["documents"])
app.include_router(chatbot.router)
