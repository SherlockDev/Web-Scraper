import abc
import asyncio
import logging
from dataclasses import dataclass

from app.config import settings
from app.models import Product

logger = logging.getLogger(__name__)


@dataclass
class ScraperContext:
    query: str
    max_pages: int


class BaseScraper(abc.ABC):
    website_name: str

    async def scrape(self, context: ScraperContext) -> list[Product]:
        results: list[Product] = []

        for page in range(1, context.max_pages + 1):
            for attempt in range(1, settings.scraper_retry_attempts + 2):
                try:
                    page_results = await self.scrape_page(context, page)
                    results.extend(page_results)
                    await asyncio.sleep(settings.scraper_rate_limit_seconds)
                    break
                except Exception as exc:  # noqa: BLE001
                    logger.warning("%s scraper failed page=%s attempt=%s: %s", self.website_name, page, attempt, exc)
                    if attempt > settings.scraper_retry_attempts:
                        break
                    await asyncio.sleep(settings.scraper_retry_delay_seconds)

        return results

    @abc.abstractmethod
    async def scrape_page(self, context: ScraperContext, page: int) -> list[Product]:
        raise NotImplementedError
