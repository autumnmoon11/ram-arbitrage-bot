from app.scrapers.base import BaseScraper
from playwright.async_api import async_playwright
import re
import asyncio

class NeweggScraper(BaseScraper):
    async def get_ram_details(self, url: str):
        async with async_playwright() as p:
            browser, page = await self.get_page(p, url)
            try:
                # Wait for JS to settle and elements to appear
                await asyncio.sleep(3)
                await page.wait_for_selector(".price-current", timeout=10000)

                # 1. Direct Data Extraction
                title = await self._get_text(page, ".product-title")
                price_raw = await self._get_text(page, ".price-current")
                
                # 2. Status & Model Identification
                buy_button = await page.query_selector("button.btn-primary")
                is_in_stock = await buy_button.is_enabled() if buy_button else False
                model_number = await self._extract_model(page, title, url)

                return {
                    "retailer": "Newegg",
                    "product_name": title,
                    "model_number": model_number,
                    "price": self._clean_price(price_raw),
                    "in_stock": is_in_stock,
                    "url": url
                }
            except Exception as e:
                return {"retailer": "Newegg", "error": str(e), "url": url}
            finally:
                await browser.close()

    async def _get_text(self, page, selector):
        """Helper to safely get stripped text from a selector."""
        elem = await page.query_selector(selector)
        return (await elem.inner_text()).strip() if elem else ""

    def _clean_price(self, price_str):
        """Converts currency string to float."""
        try:
            return float(re.sub(r'[^\d.]', '', price_str))
        except ValueError:
            return 0.0

    async def _extract_model(self, page, title, url):
        """Orchestrates the 'Brute Force' model extraction logic."""
        # 1. Check Metadata List
        model_elem = await page.query_selector("li:has-text('Model')")
        if model_elem:
            raw = await model_elem.inner_text()
            potential = re.sub(r'(?i)model\s*:?\s*', '', raw).strip()
            if self._is_valid_model(potential):
                return potential

        # 2. Check Title via Regex
        match = re.search(r'(?i)model\s+([A-Z0-9-]+)', title)
        if match:
            return match.group(1)

        # 3. Last Resort: URL Parsing
        url_match = re.search(r'[A-Z0-9-]{10,25}', url.split('/')[-1])
        return url_match.group(0) if url_match else "UNKNOWN"

    def _is_valid_model(self, text):
        """Validation logic for RAM part numbers."""
        return bool(re.search(r'[A-Z].*\d|\d.*[A-Z]', text)) and len(text) >= 8