from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_title: str = "Web Scraper API"
    api_version: str = "1.0.0"
    request_timeout_seconds: int = 20
    max_pages_per_site: int = 3
    scraper_concurrency: int = 4
    scraper_retry_attempts: int = 2
    scraper_retry_delay_seconds: float = 1.0
    scraper_rate_limit_seconds: float = 1.0
    proxy_url: str | None = None
    cache_ttl_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SCRAPER_")


settings = Settings()
