# app/main.py
import asyncio
import sys
import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from sqlmodel import Session, select
from fastapi import HTTPException

from app.database import init_db, engine
from app.models import PricePoint
from app.scrapers.base import BaseScraper
from app.scrapers.newegg import NeweggScraper
from app.scrapers.amazon import AmazonScraper

# Windows Proactor Fix (Crucial for Playwright)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="RAM Arbitrage Bot", lifespan=lifespan)

def run_isolated_scrape(url: str):
    """
    Background task that selects the correct scraper based on the URL.
    """
    # Ensure Playwright can spawn subprocesses on Windows by using the proactor loop
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    try:
        # Routing Logic
        if "amazon.com" in url or "amzn.to" in url:
            scraper = AmazonScraper()
        elif "newegg.com" in url:
            scraper = NeweggScraper()
        else:
            print("Unsupported Retailer")
            return
        
        data = asyncio.run(scraper.get_ram_details(url))
        
        if "error" in data:
            print(f"SCRAPE FAILED: {data['error']}")
            return

        with Session(engine) as session:
            new_entry = PricePoint(
                retailer=data["retailer"],
                product_name=data["product_name"],
                price=data["price"],
                in_stock=data["in_stock"],
                url=data["url"]
            )
            session.add(new_entry)
            session.commit()
        print(f"DATABASE SUCCESS: Saved {data['product_name']}")
        
    except Exception as e:
        print(f"ISOLATED TASK ERROR: {e}")


@app.get("/")
def read_root():
    return {"status": "online", "message": "RAM Spot-Market Engine Active"}


@app.post("/scan")
async def trigger_scan(url: str, background_tasks: BackgroundTasks):
    """Trigger a background RAM price check."""
    # Early Validation: Check if we support this site
    allowed_domains = ["newegg.com", "amazon.com", "amzn.to"]
    
    if not any(domain in url for domain in allowed_domains):
        raise HTTPException(
            status_code=400, 
            detail="Supported retailers: Newegg, Amazon."
        )
    background_tasks.add_task(run_isolated_scrape, url)
    return {"status": "accepted", "message": f"Scan started for {url}"}


@app.get("/results")
def get_results():
    with Session(engine) as session:
        # Fetch results ordered by newest first
        statement = select(PricePoint).order_by(PricePoint.timestamp.desc())
        results = session.exec(statement).all()
        return {"count": len(results), "data": results}
