from src.factories.abstact_factory import AbstractFactory
from src.scrapers.ekantipur_scraper import EkantipurScraper
from src.scrapers.kathmandupost_scraper import KathmanduPostScraper

class EkantipurFactory(AbstractFactory):
    def create_scraper(self) -> EkantipurScraper:
        return EkantipurScraper()

class KathmanduPostFactory(AbstractFactory):
    def create_scraper(self) -> KathmanduPostScraper:
        return KathmanduPostScraper()