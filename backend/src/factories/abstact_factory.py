from abc import ABC, abstractmethod
from src.scrapers.base_scraper import BaseScraper

class AbstractFactory(ABC):
    @abstractmethod
    def create_scraper(self) -> BaseScraper:
        pass