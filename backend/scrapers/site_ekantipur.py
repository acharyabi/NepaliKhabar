# backend/scrapers/site_ekantipur.py
import datetime
import logging
import requests
from pyquery import PyQuery as pq
from .base import IScraper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class SiteEkantipurScraper(IScraper):
    def __init__(self, url="https://ekantipur.com/"):
        self.url = url

    def scrape(self) -> list[dict]:
        response = self.fetch_with_retry(self.url, max_retries=3)
        if response:
            doc = pq(response.content)
            data = []
            rows = doc("section.main-news article")
            for row in rows:
                data_row = pq(row)
                title = data_row.find("h2 a").text()
                href = data_row.find("h2 a").attr("href")
                summary = data_row.find("p").text()
                img_tag = data_row.find("img")
                if img_tag and img_tag.attr("src"):
                    # ekantipur often uses relative paths or images without protocol
                    # We ensure a full URL. If the image src is something like 'ekantipur.com/foo.jpg'
                    # we prefix with 'https://' if not already present
                    img_src = img_tag.attr("src")
                    if img_src.startswith("http"):
                        image = img_src
                    else:
                        image = "https://" + img_src.lstrip("/")
                else:
                    image = ""
                if title.strip():
                    record = {
                        "site_name": "Ekantipur",
                        "title": title.strip(),
                        "content": summary.strip() if summary else "",
                        "scraped_at": datetime.datetime.utcnow()
                    }
                    # If you want to store image and href as well, you can do so by extending your DB model or adding these to 'content'
                    # For now, let's just append them to the content for demonstration
                    record["content"] += f"\nImage: {image}\nLink: {href}"
                    data.append(record)
                    logging.info(
                        f"Extracted data - title: {title}, href: {href}, summary: {summary}, image: {image}"
                    )
            return data
        else:
            logging.error("Failed to retrieve data from ekantipur.")
            return []

    def fetch_with_retry(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logging.warning(f"Fetch attempt {attempt+1} failed: {e}")
        logging.error("All fetch attempts failed.")
        return None
