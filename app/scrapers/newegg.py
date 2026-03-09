# app/scrapers/newegg.py
from app.scrapers.base import BaseScraper
from playwright.async_api import async_playwright
import re

class NeweggScraper(BaseScraper):
    async def get_ram_details(self, url: str):
        async with async_playwright() as p:
            browser, page = await self.get_page(p, url)
            
            try:
                # Explicitly wait for the price to appear
                await page.wait_for_selector(".price-current", timeout=10000)

                # Extract Price
                price_elem = await page.query_selector(".price-current")
                price_text = await price_elem.inner_text() if price_elem else "0"
                
                # Extract Stock Status
                # Check if the 'Add to Cart' button exists and is enabled
                buy_button = await page.query_selector("#btn_inner_buy_now")
                is_in_stock = await buy_button.is_enabled() if buy_button else False
                
                # Clean the Price
                clean_price = float(re.sub(r'[^\d.]', '', price_text))
                
                return {
                    "retailer": "Newegg",
                    "price": clean_price,
                    "in_stock": is_in_stock,
                    "url": url
                }
            finally:
                await browser.close()