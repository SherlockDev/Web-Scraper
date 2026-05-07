# Web-Scraper

Full-stack scaffold for an e-commerce scraping app with a React + Tailwind frontend and FastAPI backend.

## Features

- Multi-select supported websites: Amazon, eBay, Walmart, Etsy, AliExpress
- Keyword search input for products
- Multi-select data fields to extract
- Output formats: table, CSV, JSON, Excel, PDF
- Async backend job flow with status polling
- Normalized response schema based on selected fields
- Modular scraper layout (one scraper class per website)
- Retry handling, basic rate limiting delay, cache, and logging scaffolding
- Pagination parameter support (`max_pages`)
- Download/export API endpoints

> ⚠️ This repository includes a safe starter scraping architecture and mock scraper output. When adding real website-specific scraping, ensure you respect robots.txt, target site ToS, and legal constraints.

## Recommended Project Structure

```text
.
├── backend
│   ├── app
│   │   ├── api/routes.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── scrapers/
│   │   │   ├── base.py
│   │   │   ├── registry.py
│   │   │   └── <website>.py
│   │   ├── services/scrape_service.py
│   │   └── utils/
│   │       ├── cache.py
│   │       ├── exporters.py
│   │       └── normalizer.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend
│   ├── src/App.tsx
│   ├── src/index.css
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Backend API

### POST `/api/v1/scrape`
Submit a scrape request.

Example request body:

```json
{
  "websites": ["Amazon", "eBay"],
  "query": "wireless gaming mouse",
  "fields": ["title", "price", "product_url", "seller"],
  "output_format": "table",
  "max_pages": 2
}
```

### GET `/api/v1/jobs/{job_id}`
Returns job status and normalized rows.

### GET `/api/v1/jobs/{job_id}/export?output_format=csv|json|excel|pdf`
Returns downloadable export for completed jobs.

## Data Model

Normalized rows include only selected fields plus `website`:

```json
{
  "website": "Amazon",
  "title": "Logitech G Pro Wireless Gaming Mouse",
  "price": "$89.99",
  "product_url": "https://...",
  "seller": "Amazon"
}
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:8000`

## Docker

```bash
docker compose up --build
```

## Architecture Notes / Extension Points

- **Modular scraper design:** add a new class in `app/scrapers/` and register it in `registry.py`.
- **Queue/job system:** currently in-memory async jobs; replace with Celery/RQ + Redis for production.
- **Retry handling:** centralized in `BaseScraper.scrape()`.
- **Rate limiting:** controlled by `SCRAPER_SCRAPER_RATE_LIMIT_SECONDS`.
- **Proxy support:** configure `SCRAPER_PROXY_URL` and pass into browser/network clients.
- **Caching:** simple TTL in-memory cache in `utils/cache.py`.
- **Pagination:** request `max_pages` and iterate per scraper.
- **Logging:** standard Python logging initialized in `main.py`.
- **API validation:** strict enums and constraints in Pydantic models.

## Compliance Guidance

- Respect robots.txt where applicable.
- Do not bypass anti-bot protections in violation of site policies.
- Avoid scraping personal/sensitive data.
- Validate legal requirements for your target geography and use case.
