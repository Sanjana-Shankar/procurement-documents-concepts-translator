# Procurement Spend Normalizer

## 📌 Overview
The **Procurement Spend Normalizer** is a finance-focused application that helps enterprises unify and analyze their procurement spend data.  
Enterprises often receive **purchase orders and invoices** in mixed formats with inconsistent naming conventions (e.g., "Freight" vs. "Logistics" vs. "Shipping").  
This app extracts data from scanned invoices, normalizes cost categories, and provides a clean **unified spend table** for finance teams to run analytics.  

Additionally, the app includes a **Q&A chatbot** powered by Pathway’s Retrieval-Augmented Generation (RAG) framework, allowing users to clarify finance terms and navigate spend data interactively.

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
```bash
git clone https://github.com/your-org/procurement-spend-normalizer.git
cd procurement-spend-normalizer
2️⃣ Backend Setup (FastAPI)
Create virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
Install dependencies
bash
Copy code
pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn sqlalchemy pymongo asyncpg
If you prefer PostgreSQL with psycopg2 instead of asyncpg:
pip install psycopg2-binary

Run backend
bash
Copy code
uvicorn backend.main:app --reload
Backend runs at: http://127.0.0.1:8000

3️⃣ Frontend Setup (React)
bash
Copy code
cd frontend
npm install
npm run dev
Frontend runs at: http://localhost:5173 (or CRA default http://localhost:3000).

📂 Project Structure
graphql
Copy code
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
