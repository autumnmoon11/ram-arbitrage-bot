# app/scrapers/base.py
from playwright.async_api import async_playwright

class BaseScraper:
    async def get_page(self, playwright, url):
        """
        Handles the heavy lifting of browser lifecycle and stealth.
        """
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/"
            }
        )
        page = await context.new_page()
        
        # Set a timeout so the bot doesn't hang forever
        page.set_default_timeout(30000) 
        
        await page.goto(url, wait_until="domcontentloaded")
        return browser, page