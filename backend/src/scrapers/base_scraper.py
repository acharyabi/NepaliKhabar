from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass

    @abstractmethod
    def save_to_db(self, data: List[Dict]):
        pass