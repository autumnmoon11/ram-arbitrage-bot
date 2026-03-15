# app/scrapers/amazon.py
from app.scrapers.base import BaseScraper
from playwright.async_api import async_playwright
import re

class AmazonScraper(BaseScraper):
    async def get_ram_details(self, url: str):
        async with async_playwright() as p:
            browser, page = await self.get_page(p, url)
            
            try:
                await page.wait_for_selector(".a-price-whole", timeout=10000)
                
                # Extract Product Title
                title_elem = await page.query_selector("#productTitle")
                product_name = await title_elem.inner_text() if title_elem else "Unknown Amazon RAM"
                
                # Extract Price (combining whole and fraction for accuracy)
                whole = await page.query_selector(".a-price-whole")
                fraction = await page.query_selector(".a-price-fraction")
                
                if whole and fraction:
                    price_text = f"{await whole.inner_text()}{await fraction.inner_text()}"
                else:
                    # Fallback to offscreen price
                    offscreen = await page.query_selector(".a-offscreen")
                    price_text = await offscreen.inner_text() if offscreen else "0"
                
                # Extract Stock Status - Check for the 'Add to Cart' button
                add_to_cart = await page.query_selector("#add-to-cart-button")
                is_in_stock = True if add_to_cart else False
                
                # Clean Price
                clean_price = float(re.sub(r'[^\d.]', '', price_text))
                
                return {
                    "retailer": "Amazon",
                    "product_name": product_name.strip(),
                    "price": clean_price,
                    "in_stock": is_in_stock,
                    "url": url
                }
            except Exception as e:
                return {"retailer": "Amazon", "error": str(e), "url": url}
            finally:
                await browser.close() 