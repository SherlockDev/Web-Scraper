from app.models import Website
from app.scrapers.aliexpress import AliExpressScraper
from app.scrapers.amazon import AmazonScraper
from app.scrapers.ebay import EbayScraper
from app.scrapers.etsy import EtsyScraper
from app.scrapers.walmart import WalmartScraper

SCRAPER_REGISTRY = {
    Website.amazon: AmazonScraper,
    Website.ebay: EbayScraper,
    Website.walmart: WalmartScraper,
    Website.etsy: EtsyScraper,
    Website.aliexpress: AliExpressScraper,
}
