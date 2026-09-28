# LegalEase Studio

**AI-Assisted Legal Document Drafting Application**

LegalEase Studio is a Python application that accepts a structured document brief, sends the supplied information to Google Gemini through a FastAPI backend, displays the generated first draft in a Streamlit workspace, and exports the reviewed draft as TXT, DOCX, or PDF.

## Key features

- Structured legal-document brief
- Document type, parties, purpose, terms, effective date, and optional jurisdiction
- Gemini-powered first-draft generation
- Editable review workspace
- TXT, DOCX, and PDF export
- FastAPI API with validation and health endpoint
- Automated backend and export tests
- AI-draft disclaimer to encourage professional legal review

## Architecture

```text
Streamlit UI
    |
    | POST /generate
    v
FastAPI backend
    |
    v
Gemini generation service
    |
    v
Generated draft
    |
    +--> Edit / Review
    +--> TXT / DOCX / PDF
```

## Local setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your own Gemini API key.
4. Start the backend:

```bash
uvicorn backend.main:app --reload
```

5. In another terminal start the frontend:

```bash
streamlit run frontend/app.py
```

## Environment variables

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=your_supported_gemini_model
BACKEND_URL=http://127.0.0.1:8000
APP_NAME=LegalEase
COMPANY_NAME=LegalEase
```

Never commit `.env` or an API key to GitHub.

## API

### `GET /health`
Returns application health information.

### `POST /generate`
Accepts:

```json
{
  "document_type": "Rental Agreement",
  "parties": "Owner: A; Tenant: B",
  "purpose": "Residential tenancy",
  "terms": "Monthly rent: 15000",
  "effective_date": "1 October 2026",
  "jurisdiction": "Tamil Nadu, India"
}
```

## Testing

Run:

```bash
pytest -q
```

## Important limitation

LegalEase generates drafts and does not replace a qualified lawyer. Generated content should be checked for accuracy, completeness, and jurisdiction-specific requirements before being signed or relied upon.
