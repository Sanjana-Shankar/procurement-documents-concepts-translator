from fastapi import FastAPI
from backend.app.routes import documents, chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Finance Document Processor",
    version="1.0.0",
    description="Extracts and normalizes financial documents using LandingAI + Pathway"
)


# Enable CORS so your React frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="", tags=["documents"])
app.include_router(chatbot.router, prefix="", tags=["chatbot"])
app.include_router(documents.router, prefix="", tags=["spend"])
