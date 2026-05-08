import csv
import io
import json

from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_csv(rows: list[dict[str, object]]) -> bytes:
    output = io.StringIO()
    fieldnames = list(rows[0].keys()) if rows else []
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def export_json(rows: list[dict[str, object]]) -> bytes:
    return json.dumps(rows, indent=2).encode("utf-8")


def export_excel(rows: list[dict[str, object]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    headers = list(rows[0].keys()) if rows else []
    if headers:
        sheet.append(headers)
        for row in rows:
            sheet.append([row.get(header, "") for header in headers])

    output = io.BytesIO()
    workbook.save(output)
    return output.getvalue()


def export_pdf(rows: list[dict[str, object]]) -> bytes:
    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=letter)
    y = 760
    pdf.setFont("Helvetica", 10)
    for index, row in enumerate(rows, start=1):
        text = f"{index}. " + " | ".join([f"{key}: {value}" for key, value in row.items()])
        pdf.drawString(40, y, text[:140])
        y -= 16
        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 760

    pdf.save()
    return output.getvalue()
