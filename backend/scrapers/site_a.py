# backend/scrapers/site_a.py
import datetime
import requests
from bs4 import BeautifulSoup
from .base import IScraper

class SiteAScraper(IScraper):
    def scrape(self) -> list[dict]:
        url = "https://example-site-a.com/latest"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        for item in soup.select(".article"):
            title = item.select_one(".title").get_text(strip=True)
            content = item.select_one(".description").get_text(strip=True)
            data.append({
                "site_name": "SiteA",
                "title": title,
                "content": content,
                "scraped_at": datetime.datetime.utcnow()
            })
        return data
