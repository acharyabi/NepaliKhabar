from pyquery import PyQuery as pq
from src.scrapers.base_scraper import BaseScraper
from src.utils.request_utils import fetch_with_retry
import logging 
from src.database.models import EkantipurArticle
from src.database.session import SessionLocal
# logger = get_run_logger()
class EkantipurScraper(BaseScraper):
    def __init__(self, url: str = "https://ekantipur.com/", max_retries: int = 5):
        self.url = url
        self.max_retries = max_retries

    def scrape(self) -> list:
        response = fetch_with_retry(self.url, self.max_retries)
        data = []
        if response:
            doc = pq(response.content)
            rows = doc("section.main-news article")
            for row in rows:
                data_row = pq(row)
                title = data_row.find("h2 a").text().strip()
                href = data_row.find("h2 a").attr("href")
                summary = data_row.find("p").text().strip()
                img_tag = data_row.find("img")
                image = f"https://{img_tag.attr('src')}" if img_tag.attr("src") else ""

                if title:
                    row_data = {
                        "title": title,
                        "href": href,
                        "summary": summary,
                        "image": image,
                    }
                    data.append(row_data)
                    logging.info(
                        f"Extracted Ekantipur data - title: {title}, href: {href}, summary: {summary}, image: {image}"
                    )
        else:
            logging.error("Failed to retrieve data from Ekantipur.")
        return data

    def save_to_db(self, data: list):
        session = SessionLocal()
        try:
            for item in data:
                article = EkantipurArticle(**item)
                session.add(article)
            session.commit()
            logging.info("Ekantipur data saved to database.")
        except Exception as e:
            session.rollback()
            logging.error(f"Error saving Ekantipur data: {e}")
        finally:
            session.close()