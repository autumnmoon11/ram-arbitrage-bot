# app/scrapers/newegg.py
from app.scrapers.base import BaseScraper
from playwright.async_api import async_playwright
import re

class NeweggScraper(BaseScraper):
    async def get_ram_details(self, url: str):
        async with async_playwright() as p:
            browser, page = await self.get_page(p, url)
            
            try:
                # Explicitly wait for core elements to appear
                await page.wait_for_selector(".price-current", timeout=10000)
                await page.wait_for_selector(".product-title", timeout=10000)

                # Extract Product Title
                title_elem = await page.query_selector(".product-title")
                product_name = await title_elem.inner_text() if title_elem else "Unknown RAM Kit"

                # Extract Price
                price_elem = await page.query_selector(".price-current")
                price_text = await price_elem.inner_text() if price_elem else "0"
                
                # Extract Stock Status
                # Use a flexible selector since Newegg button IDs can vary
                buy_button = await page.query_selector("button.btn-primary")
                is_in_stock = await buy_button.is_enabled() if buy_button else False
                
                # Clean the Price
                clean_price = float(re.sub(r'[^\d.]', '', price_text))
                
                return {
                    "retailer": "Newegg",
                    "product_name": product_name.strip(),
                    "price": clean_price,
                    "in_stock": is_in_stock,
                    "url": url
                }
            except Exception as e:
                print(f"SCRAPE ERROR: {e}")
                return {"retailer": "Newegg", "error": str(e), "url": url}
            finally:
                await browser.close()