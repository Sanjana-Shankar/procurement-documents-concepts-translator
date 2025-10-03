# Procurement Spend Normalizer

## 📌 Overview
The **Procurement Spend Normalizer** is a finance-focused application that helps enterprises unify and analyze their procurement spend data.  
Enterprises often receive **purchase orders and invoices** in mixed formats with inconsistent naming conventions (e.g., "Freight" vs. "Logistics" vs. "Shipping").  
This app extracts data from scanned invoices, normalizes cost categories, and provides a clean **unified spend table** for finance teams to run analytics.  

Additionally, the app includes a **Q&A chatbot** powered by Pathway’s Retrieval-Augmented Generation (RAG) framework, allowing users to clarify finance terms and navigate spend data interactively.

## Problem Statement

Finance teams at growing startups and enterprises often face a common challenge: managing messy, unstructured procurement data. Invoices, receipts, and purchase orders arrive in multiple formats with inconsistent terminology—think “Freight,” “Logistics,” and “Shipping” all referring to the same category. Manually cleaning, categorizing, and analyzing this data is time-consuming, error-prone, and inefficient.

The Procurement Spend Normalizer solves this problem by automatically extracting, cleaning, and normalizing procurement data, mapping inconsistent terms into unified spend categories. Beyond simple data cleaning, it provides a smart, interactive chatbot that allows finance teams to ask natural language questions like:

“Which invoices had professional services over $3,000?”

“How much did we spend on Transportation last quarter?”

The system flags anomalies and high-value spend, links every answer back to the original line items for auditing, and exports data as clean Excel sheets or dashboards.

With the Procurement Spend Normalizer, finance teams can turn chaotic piles of documents into actionable intelligence in seconds—reducing manual work, improving spend visibility, and enabling faster, data-driven decisions
---

## 🚀 Features
- **Document Extraction**: Uses [LandingAI](https://landing.ai/) to parse purchase orders and invoices from PDFs/scans.  
- **Spend Normalization**: Maps inconsistent labels into unified categories (e.g., "Freight/Logistics/Shipping" → "Transportation").  
- **Q&A Chatbot**: Built with [Pathway RAG](https://pathway.com/), allowing users to ask questions about finance terminology and the normalized dataset.  
- **Database Integration**: Store structured spend data in either **MongoDB** or **PostgreSQL**.  
- **Frontend Dashboard**: A React UI to upload invoices, visualize normalized data, and chat with the Q&A assistant.  

---

## 🛠 Tech Stack
- **Frontend**: React (TypeScript, Vite/CRA, TailwindCSS)  
- **Backend**: FastAPI (Python)  
- **Database**:  
  - Option A: MongoDB (via `pymongo`)  
  - Option B: PostgreSQL (via `SQLAlchemy` + `asyncpg` or `psycopg2-binary`)  
- **AI/ML Services**:  
  - [LandingAI](https://landing.ai/) → OCR + Document parsing  
  - [Pathway RAG](https://pathway.com/) → Finance Q&A chatbot  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repo
```
git clone https://github.com/your-org/procurement-spend-normalizer.git
cd procurement-spend-normalizer
```
### 2️⃣ Backend Setup (FastAPI)
#### Create virtual environment
##### macOS/Linux 
```
python3 -m venv venv
source venv/bin/activate   
```
##### Windows
```
python3 -m venv venv
venv\Scripts\activate      
```
#### Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn sqlalchemy pymongo asyncpg
```
```
# If you prefer PostgreSQL with psycopg2 instead of asyncpg:
pip install psycopg2-binary
```

#### Run backend
```bash
# Backend runs at: http://127.0.0.1:8000
uvicorn backend.main:app --reload
```

### 3️⃣ Frontend Setup (React)
```bash
# Frontend runs at: http://localhost:5173 (or CRA default http://localhost:3000).
cd frontend
npm install
npm run dev
```

### 📂 Project Structure
```
graphql

procurement-spend-normalizer/
│── backend/
│   ├── main.py        # FastAPI entry point
│   ├── models/        # SQLAlchemy models
│   ├── routes/        # API routes
│   ├── services/      # LandingAI + Pathway integration
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/  # API calls to backend
│── README.md
```
