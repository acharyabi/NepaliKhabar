# backend/scrapers/factory.py
from typing import Type
from .base import IScraper
from .site_a import SiteAScraper
from .site_b import SiteBScraper
from .site_ekantipur import SiteEkantipurScraper  # Import the new scraper

class ScraperFactory:
    scrapers = {
        "site_a": SiteAScraper,
        "site_b": SiteBScraper,
        "ekantipur": SiteEkantipurScraper 
    }

    @classmethod
    def get_scraper(cls, site_name: str) -> IScraper:
        scraper_cls: Type[IScraper] = cls.scrapers.get(site_name.lower())
        if not scraper_cls:
            raise ValueError(f"Scraper for site {site_name} not found.")
        return scraper_cls()
