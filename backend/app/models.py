from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Website(str, Enum):
    amazon = "Amazon"
    ebay = "eBay"
    walmart = "Walmart"
    etsy = "Etsy"
    aliexpress = "AliExpress"


class DataField(str, Enum):
    title = "title"
    price = "price"
    rating = "rating"
    reviews_count = "reviews_count"
    product_url = "product_url"
    product_image = "product_image"
    seller = "seller"
    availability = "availability"


class OutputFormat(str, Enum):
    table = "table"
    csv = "csv"
    json = "json"
    excel = "excel"
    pdf = "pdf"


class ScrapeRequest(BaseModel):
    websites: list[Website] = Field(..., min_length=1)
    query: str = Field(..., min_length=2, max_length=120)
    fields: list[DataField] = Field(..., min_length=1)
    output_format: OutputFormat = OutputFormat.table
    max_pages: int = Field(default=1, ge=1, le=3)

    @field_validator("websites")
    @classmethod
    def unique_websites(cls, values: list[Website]) -> list[Website]:
        return list(dict.fromkeys(values))

    @field_validator("fields")
    @classmethod
    def unique_fields(cls, values: list[DataField]) -> list[DataField]:
        return list(dict.fromkeys(values))


class Product(BaseModel):
    website: str
    title: str | None = None
    price: str | None = None
    rating: str | None = None
    reviews_count: str | None = None
    product_url: str | None = None
    product_image: str | None = None
    seller: str | None = None
    availability: str | None = None


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class ScrapeJob(BaseModel):
    id: str
    status: JobStatus
    request: ScrapeRequest
    results: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None
