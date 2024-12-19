# backend/scrapers/site_b.py
import datetime
import requests
from bs4 import BeautifulSoup
from .base import IScraper

class SiteBScraper(IScraper):
    def scrape(self) -> list[dict]:
        url = "https://example-site-b.com/news"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        for item in soup.select(".news-item"):
            title = item.select_one("h2").get_text(strip=True)
            content = item.select_one("p.summary").get_text(strip=True)
            data.append({
                "site_name": "SiteB",
                "title": title,
                "content": content,
                "scraped_at": datetime.datetime.utcnow()
            })
        return data
