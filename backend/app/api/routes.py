from fastapi import APIRouter, HTTPException, Response

from app.models import JobStatus, OutputFormat, ScrapeRequest
from app.services.scrape_service import ScrapeService
from app.utils.exporters import export_csv, export_excel, export_json, export_pdf

router = APIRouter(prefix="/api/v1", tags=["scraper"])
service = ScrapeService()


@router.post("/scrape")
async def submit_scrape_job(payload: ScrapeRequest) -> dict[str, str]:
    job = await service.create_job(payload)
    return {"job_id": job.id, "status": job.status}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> dict[str, object]:
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return service.serialize_job(job)


@router.get("/jobs/{job_id}/export")
async def export_job(job_id: str, output_format: OutputFormat) -> Response:
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.completed:
        raise HTTPException(status_code=409, detail="Job is not completed")

    content: bytes
    media_type: str
    filename: str

    if output_format == OutputFormat.csv:
        content = export_csv(job.results)
        media_type = "text/csv"
        filename = "results.csv"
    elif output_format == OutputFormat.json:
        content = export_json(job.results)
        media_type = "application/json"
        filename = "results.json"
    elif output_format == OutputFormat.excel:
        content = export_excel(job.results)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "results.xlsx"
    elif output_format == OutputFormat.pdf:
        content = export_pdf(job.results)
        media_type = "application/pdf"
        filename = "results.pdf"
    else:
        raise HTTPException(status_code=400, detail="Table output is available directly via /jobs/{job_id}")

    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=content, media_type=media_type, headers=headers)
