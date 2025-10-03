# mcp-server/server.py
from fastmcp import FastMCP

# ⬇ replace these with your real functions later
_NORMALIZED = []

def _stub_extract(file_uri: str | None = None, file_bytes_b64: str | None = None) -> dict:
    return {
        "invoice_id": "INV-001",
        "currency": "USD",
        "line_items": [
            {"description": "Freight charges", "amount": 1200, "loc": {"page": 2, "cell": "T4"}},
            {"description": "Consulting services", "amount": 5000, "loc": {"page": 1, "cell": "R6"}},
        ],
        "meta": {"source_uri": file_uri or "local://stub.pdf"}
    }

def _stub_normalize_and_ingest(invoice_json: dict, overrides: dict | None = None) -> list[dict]:
    cmap = {
        "Transportation": ["Freight", "Shipping", "Logistics"],
        "Professional Services": ["Consulting", "Advisory"],
        **(overrides or {})
    }
    rows = []
    for li in invoice_json.get("line_items", []):
        desc = (li.get("description") or "").lower()
        category = "Other"
        for canon, syns in cmap.items():
            if any(s.lower() in desc for s in syns + [canon]):
                category = canon; break
        rows.append({
            "invoice_id": invoice_json["invoice_id"],
            "category": category,
            "term": li["description"],
            "amount": li.get("amount", 0),
            "source": f'{invoice_json["invoice_id"]}:{li["loc"]["page"]}:{li["loc"]["cell"]}',
        })
    _NORMALIZED.extend(rows)
    return rows

def _stub_query(question: str) -> dict:
    q = question.lower()
    focus = "Transportation" if "transportation" in q else \
            "Professional Services" if "professional" in q else None
    rows = [r for r in _NORMALIZED if (not focus or r["category"] == focus)]
    total = sum(r.get("amount") or 0 for r in rows)
    return {
        "answer": f'We spent ${total:,.0f} on {focus or "all categories"} across {len(rows)} line items.',
        "breakdown": rows[:3],
        "citations": [r["source"] for r in rows[:3]],
    }

mcp = FastMCP("spend-tools")

@mcp.tool()
def extract_spend(file_uri: str | None = None, file_bytes_b64: str | None = None) -> dict:
    """Parse PDF/PO (stub now; swap to LandingAI later)."""
    return _stub_extract(file_uri=file_uri, file_bytes_b64=file_bytes_b64)

@mcp.tool()
def normalize_ingest(invoice_json: dict, concept_map_overrides: dict | None = None) -> dict:
    """Normalize + ingest (stub now; swap to Pathway later)."""
    rows = _stub_normalize_and_ingest(invoice_json, concept_map_overrides or {})
    return {"normalized": rows}

@mcp.tool(name="query_spend")
def query_spend_tool(question: str) -> dict:
    """Answer spend questions with citations."""
    return _stub_query(question)

if __name__ == "__main__":
    # FastMCP will choose a sensible default transport; this starts the server.
    mcp.run(transport="http", host="0.0.0.0", port=8000)

