# src/scrapers/kathmandupost_scraper.py
from pyquery import PyQuery as pq
from src.scrapers.base_scraper import BaseScraper
from src.utils.request_utils import fetch_with_retry
from src.database.models import KathmanduPostArticle
from src.database.session import SessionLocal
import logging
class KathmanduPostScraper(BaseScraper):
    def __init__(self, base_url: str = "https://kathmandupost.com", max_retries: int = 5):
        self.base_url = base_url
        self.max_retries = max_retries

    def scrape(self) -> list:
        response = fetch_with_retry(self.base_url, self.max_retries)
        data = []
        if response:
            doc = pq(response.content)
            rows = doc(".container .row.order article")
            logging.info(f"Found {len(rows)} articles in KathmanduPost.")
            for row in rows:
                data_row = pq(row)
                title = data_row.find("h3 a").text().strip()
                href = f"{self.base_url}{data_row.find('h3 a').attr('href')}"
                summary = data_row.find("p").text().strip()
                img_tag = data_row.find("img")
                image = img_tag.attr("data-src").strip() if img_tag and img_tag.attr("data-src") else ""

                if title:
                    row_data = {
                        "title": title,
                        "href": href,
                        "summary": summary,
                        "image": image,
                    }
                    data.append(row_data)
                    logging.info(
                        f"Extracted KathmanduPost data - title: {title}, href: {href}, summary: {summary}, image: {image}"
                    )
        else:
            logging.error("Failed to retrieve data from KathmanduPost.")
        return data

    def save_to_db(self, data: list):
        session = SessionLocal()
        try:
            for item in data:
                article = KathmanduPostArticle(**item)
                session.add(article)
            session.commit()
            logging.info("KathmanduPost data saved to database.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error saving KathmanduPost data: {e}")
        finally:
            session.close()
