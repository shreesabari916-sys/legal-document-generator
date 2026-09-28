from fastapi.testclient import TestClient

from backend.main import app
from utils.document_export import create_docx, create_pdf, create_txt, format_html_preview, sanitize_text

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["application"] == "LegalEase"
    assert response.json()["version"] == "4.0.0"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_validation_requires_purpose():
    response = client.post("/generate", json={
        "document_type": "Rental Agreement",
        "parties": "Owner: A; Tenant: B",
        "terms": "Monthly rent: 15000",
        "effective_date": "1 October 2026",
    })
    assert response.status_code == 422


def test_generate_validation_rejects_empty_party():
    response = client.post("/generate", json={
        "document_type": "Rental Agreement",
        "parties": "",
        "purpose": "Residential tenancy",
        "terms": "Monthly rent: 15000",
        "effective_date": "1 October 2026",
    })
    assert response.status_code == 422


def test_sanitize_text():
    cleaned = sanitize_text('A “legal” document — with an ellipsis…')
    assert cleaned == 'A "legal" document - with an ellipsis...'


def test_preview_escapes_html():
    preview = format_html_preview("<script>alert('x')</script>")
    assert "&lt;script&gt;" in preview
    assert "<script>" not in preview


def test_exports_return_expected_bytes():
    document = "RENTAL AGREEMENT\nOwner: A\nTenant: B"
    assert isinstance(create_txt(document), bytes)
    assert create_docx(document).startswith(b"PK")
    assert create_pdf(document).startswith(b"%PDF")
