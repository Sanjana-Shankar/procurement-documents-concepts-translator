from fastapi import APIRouter, HTTPException, Request
import os
import httpx
from google import generativeai  # or whatever the SDK name is
router = APIRouter()
import json
from pydantic import BaseModel

# URL of the Pathway RAG REST API
PATHWAY_RAG_URL = os.getenv("PATHWAY_RAG_URL", "http://localhost:8000")

generativeai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    prompt: str

# Global store (in-memory)
NORMALIZED_SPEND_DATA = []

#def set_spend_data(data):
    #global NORMALIZED_SPEND_DATA
    #NORMALIZED_SPEND_DATA = data

@router.post("/chatbot/ask")
async def ask_chatbot(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    if not prompt:
        return {"answer": "⚠️ Please ask a question about the spend data."}

    global NORMALIZED_SPEND_DATA
    if not NORMALIZED_SPEND_DATA:
        return {"answer": "⚠️ No spend data available yet. Please upload a document first."}

    # Convert spend data into a readable format for the model
    spend_context = json.dumps(NORMALIZED_SPEND_DATA, indent=2)

    system_prompt = f"""
You are a financial assistant specialized in procurement spend analysis.
You are given one company's normalized spend table extracted from a single uploaded document.
Answer questions about the spending amounts, categories, or potential overspending.

Use the data below to answer the user's question accurately:
{spend_context}
"""

    try:
        # Initialize Gemini model
        generativeai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = generativeai.GenerativeModel("gemini-2.5-flash")

        # Combine system context and user prompt
        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\nUser question: {prompt}"}
                ]
            }
        ])

        return {"answer": response.text}

    except Exception as e:
        print("Gemini chatbot error:", e)
        raise HTTPException(status_code=500, detail=f"Gemini chatbot error: {e}")
    