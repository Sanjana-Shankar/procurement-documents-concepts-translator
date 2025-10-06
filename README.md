# BudgetIQ - Clean categories, confident calls!

## 📌 Overview
**BudgetIQ** is a finance-focused application that helps enterprises unify and analyze their procurement spend data.  
Enterprises often receive **purchase orders and invoices** in mixed formats with inconsistent naming conventions (e.g., "Freight" vs. "Logistics" vs. "Shipping").  
This app extracts data from scanned invoices, normalizes cost categories, and provides a clean **unified spend table** for finance teams to run analytics.  

Additionally, the app includes a **Q&A agent** powered by Pathway’s Retrieval-Augmented Generation (RAG) framework, allowing users to clarify finance terms and navigate spend data interactively.

---
> BudgetIQ Demo Video

[![Demo Video](<img width="1299" height="497" alt="Screenshot 2025-10-04 at 11 50 37 PM" src="https://github.com/user-attachments/assets/f3f1b796-7df0-4382-a8cd-7e16c4ea0f5f" />)](https://github.com/user-attachments/assets/ddfe55b4-a81d-425d-a5c3-8c8bc5549c60)


---

> BudgetIQ Workflow Architecture Diagram:
<p align="center">
<img width="497" height="547" alt="BudgetIQ Architecture Diagram" src="https://github.com/user-attachments/assets/8184c39c-734e-4af8-a27f-cc83c002a9c3" />
</p>

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
- **Q&A Agent**: Built with [Pathway RAG](https://pathway.com/), allowing users to ask questions about finance terminology and the normalized dataset, and built with [Inkeep](https://inkeep.com/) which enables multiple agents to answer clients questions and export data to Google Drive as needed.
- **Database Integration**: Store structured spend data in either **MongoDB** or **PostgreSQL**.  
- **Frontend Dashboard**: A React UI to upload invoices, visualize normalized data, and chat with the Q&A agent.  

---

## 🛠 Tech Stack
- **Frontend**: React (TypeScript, Vite/CRA, TailwindCSS)  
- **Backend**: FastAPI (Python)  
- **Database**:  
  - Option A: MongoDB (via `pymongo`)  
  - Option B: PostgreSQL (via `SQLAlchemy` + `asyncpg` or `psycopg2-binary`)  
- **AI/ML Services**:  
  - [LandingAI](https://landing.ai/) → OCR + Document parsing  
  - [Pathway RAG](https://pathway.com/) → Finance Q&A agent
  - [Inkeep](https://inkeep.com/) → MCP Server with multiple agents

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
│── mcp-server/
│    ├── my-agents/
│── README.md
```

### 📝 Problem Statement

*Enterprises often receive messy, inconsistent invoices and purchase orders from multiple vendors. These documents may vary in format, terminology, and completeness, making it challenging for finance teams to:*
- Quickly consolidate and organize procurement data into a clean, readable format.
- Break down expenses to detailed line items to understand exactly where money is being spent.
- Identify cost trends, anomalies, or potential overspending.
- Generate accurate reports without extensive manual effort.


> BudgetIQ addresses these challenges by:

- Extracting data from unstructured and messy documents using OCR.
- Normalizing inconsistent spend categories into a unified, readable table.
- Providing detailed expense breakdowns to give finance teams visibility into every line item.
- Enabling interactive queries via a Q&A agent for fast insights and anomaly detection.

The ultimate goal is to streamline procurement analytics, maintain budget control, and prevent overspending by transforming messy invoices into actionable, organized data.

---

### 👤 Sample User Story

**Title: Finance Analyst wants to organize messy invoices and track detailed expenses** 

*As a finance analyst
I want to upload messy invoices and automatically organize them into a clean, readable spend table
So that I can break down expenses into detailed categories and avoid overspending.*

Acceptance Criteria:
*I can upload invoices in various formats (PDF, scanned images, CSV/Excel).*

-> The system extracts line items and normalizes inconsistent categories into unified labels (e.g., “Freight/Shipping/Logistics” → “Transportation”).

*I can view a clean, readable spend table with detailed breakdowns per line item, vendor, and category.*

-> The dashboard highlights high-value or unusual transactions to prevent overspending.

*I can ask the Q&A agent questions like:*
- “Which categories have exceeded budget limits this month?”
- “Show invoices over $5,000 in Marketing or Transportation.”

*I can export the normalized and detailed data to Excel for reporting and auditing.*
