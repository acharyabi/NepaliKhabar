# backend/scrapers/base.py
from abc import ABC, abstractmethod

class IScraper(ABC):
    @abstractmethod
    def scrape(self) -> list[dict]:
        """
        Return a list of dictionaries, each representing a record:
        Example record:
        {
          "site_name": "SiteA",
          "title": "Some title",
          "content": "Some content",
          "scraped_at": datetime.datetime.utcnow()
        }
        """
        pass
