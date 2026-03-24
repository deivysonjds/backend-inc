import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class Scraping:

    def scrap_page_sync(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="networkidle")
            html = page.content()

            browser.close()
            return html

    async def scrap_page(self, url):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.scrap_page_sync,
            url
        )

    def extract_text(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.extract()

        return soup.get_text(separator=" ")


scraping = Scraping()