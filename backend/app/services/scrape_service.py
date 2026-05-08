import asyncio
import hashlib
import json
import uuid
from typing import Any

from app.config import settings
from app.models import JobStatus, Product, ScrapeJob, ScrapeRequest
from app.scrapers.base import ScraperContext
from app.scrapers.registry import SCRAPER_REGISTRY
from app.utils.cache import TTLCache
from app.utils.normalizer import normalize_products


class ScrapeService:
    def __init__(self) -> None:
        self.jobs: dict[str, ScrapeJob] = {}
        self.cache = TTLCache(ttl_seconds=settings.cache_ttl_seconds)

    async def create_job(self, request: ScrapeRequest) -> ScrapeJob:
        job_id = str(uuid.uuid4())
        job = ScrapeJob(id=job_id, status=JobStatus.queued, request=request)
        self.jobs[job_id] = job
        asyncio.create_task(self._run_job(job_id))
        return job

    def get_job(self, job_id: str) -> ScrapeJob | None:
        return self.jobs.get(job_id)

    async def _run_job(self, job_id: str) -> None:
        job = self.jobs[job_id]
        job.status = JobStatus.running

        cache_key = hashlib.sha256(job.request.model_dump_json().encode("utf-8")).hexdigest()
        cached = self.cache.get(cache_key)
        if cached is not None:
            job.results = cached
            job.status = JobStatus.completed
            return

        try:
            context = ScraperContext(query=job.request.query, max_pages=job.request.max_pages)
            all_products: list[Product] = []
            for website in job.request.websites:
                scraper_cls = SCRAPER_REGISTRY[website]
                scraper = scraper_cls()
                all_products.extend(await scraper.scrape(context))

            normalized = normalize_products(all_products, job.request.fields)
            job.results = normalized
            job.status = JobStatus.completed
            self.cache.set(cache_key, normalized)
        except Exception as exc:  # noqa: BLE001
            job.status = JobStatus.failed
            job.error = str(exc)

    def serialize_job(self, job: ScrapeJob) -> dict[str, Any]:
        payload = json.loads(job.model_dump_json())
        payload["results_count"] = len(job.results)
        return payload
