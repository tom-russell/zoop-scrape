from abc import ABC, abstractmethod
from models import PropertySale


class ScrapingError(Exception):
    pass


class ScrapingNetworkError(ScrapingError):
    def __init__(self, reason: str) -> None:
        self.message = f"Failed to scrape data due to network error: {reason}"
        super().__init__(self.message)


class ScrapingParsingError(ScrapingError):
    def __init__(self, reason: str) -> None:
        self.message = f"Failed to parse scraped data: {reason}"
        super().__init__(self.message)


class BaseScraper(ABC):
    @abstractmethod
    def scrape(outward_code: str) -> list[PropertySale]:
        pass
