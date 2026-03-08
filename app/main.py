# app/main.py
from fastapi import FastAPI, BackgroundTasks
from app.scrapers.base import BaseScraper
import datetime

app = FastAPI(title="RAM Arbitrage Bot")

# Temporary in-memory store
scan_results = []

async def run_price_scan(url: str):
    """Background task to fetch data without blocking the API."""
    scraper = BaseScraper()
    result = await scraper.get_page_content(url)
    
    # Enrich with metadata
    result["timestamp"] = datetime.datetime.now().isoformat()
    scan_results.append(result)
    print(f"SUCCESS: Scanned {result['site']}")

@app.get("/")
def read_root():
    return {"status": "online", "message": "RAM Spot-Market Engine Active"}

@app.post("/scan")
async def trigger_scan(url: str, background_tasks: BackgroundTasks):
    """Trigger a background RAM price check."""
    background_tasks.add_task(run_price_scan, url)
    return {"status": "accepted", "message": f"Scan started for {url}"}

@app.get("/results")
def get_results():
    return {"count": len(scan_results), "data": scan_results}
