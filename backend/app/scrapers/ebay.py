from app.models import Product
from app.scrapers.base import BaseScraper, ScraperContext
from app.scrapers.mock_data import build_mock_product


class EbayScraper(BaseScraper):
    website_name = "eBay"

    async def scrape_page(self, context: ScraperContext, page: int) -> list[Product]:
        return [build_mock_product(self.website_name, context.query, page)]
