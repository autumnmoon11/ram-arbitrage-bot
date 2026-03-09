# app/main.py
import asyncio
import sys
import datetime
from fastapi import FastAPI, BackgroundTasks
from app.scrapers.base import BaseScraper
from app.scrapers.newegg import NeweggScraper


app = FastAPI(title="RAM Arbitrage Bot")

# Temporary in-memory store
scan_results = []


def run_price_scan(url: str):
    """
    Background task that selects the correct scraper based on the URL.
    """
    # Ensure Playwright can spawn subprocesses on Windows by using the proactor loop
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    try:
        # Routing logic: Use NeweggScraper if it's a Newegg link
        if "newegg.com" in url:
            scraper = NeweggScraper()
            result = asyncio.run(scraper.get_ram_details(url))
        else:
            # Fallback to base scraper for non-supported sites
            scraper = BaseScraper()
            # The base scraper just returns a generic dict for now
            result = {"retailer": "Unknown", "url": url, "note": "Basic scan only"}

        # Enrich with metadata
        result["timestamp"] = datetime.datetime.now().isoformat()
        scan_results.append(result)
        print(f"SUCCESS: Scanned {result.get('site', 'unknown site')}")
    except Exception as e:
        print(f"SCRAPE ERROR: {e}")


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
