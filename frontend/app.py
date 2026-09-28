import html
import os
import sys
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.document_export import create_docx, create_pdf, create_txt

load_dotenv(PROJECT_ROOT / ".env")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase Studio", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
.hero {padding: 1.5rem 1.8rem; border: 1px solid rgba(120,120,120,.25); border-radius: 18px; margin-bottom: 1.5rem;}
.hero h1 {margin: 0; font-size: 2.6rem;}
.hero p {margin: .4rem 0 0; opacity: .72; font-size: 1.05rem;}
.small-note {font-size: .85rem; opacity: .68;}
.preview {border: 1px solid rgba(120,120,120,.3); border-radius: 16px; padding: 28px; height: 650px; overflow-y: auto; white-space: pre-wrap; font-family: Georgia, serif; line-height: 1.75;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='hero'><h1>⚖️ LegalEase Studio</h1><p>AI-assisted drafting workspace for structured legal document first drafts.</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Draft settings")
    jurisdiction = st.text_input("Jurisdiction", placeholder="e.g. Tamil Nadu, India")
    st.caption("Mention a jurisdiction only when it is relevant to your draft.")
    st.divider()
    st.markdown("**Workflow**")
    st.markdown("1. Describe the document\n2. Generate a draft\n3. Review and edit\n4. Export")

left, right = st.columns([1, 1])

with left:
    st.subheader("1 · Document brief")
    document_type = st.selectbox("Document type", [
        "Rental Agreement", "Employment Agreement", "Non-Disclosure Agreement",
        "Service Agreement", "Freelance Agreement", "Partnership Agreement",
        "Sale Agreement", "Custom Legal Document",
    ])
    parties = st.text_area("Parties", placeholder="Example: Owner: A; Tenant: B", height=90)
    purpose = st.text_area("Purpose", placeholder="What is this document intended to accomplish?", height=100)
    terms = st.text_area("Key terms and obligations", placeholder="Payments, responsibilities, deadlines, restrictions, deliverables...", height=170)
    effective_date = st.text_input("Effective date", placeholder="e.g. 1 October 2026")

    generate = st.button("Generate first draft", type="primary", use_container_width=True)

if generate:
    missing = []
    for label, value in [("parties", parties), ("purpose", purpose), ("terms", terms), ("effective date", effective_date)]:
        if not value.strip():
            missing.append(label)
    if missing:
        st.error("Please complete: " + ", ".join(missing) + ".")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "purpose": purpose,
            "terms": terms,
            "effective_date": effective_date,
            "jurisdiction": jurisdiction.strip() or "Not specified",
        }
        try:
            with st.spinner("Preparing your draft..."):
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=120)
            if response.ok:
                document = response.json().get("document", "").strip()
                if document:
                    st.session_state.generated_document = document
                    st.session_state.edited_document = document
                    st.success("Draft generated. Review it before using it.")
                else:
                    st.error("The backend returned an empty document.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text
                st.error(f"Generation failed: {detail}")
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not reach the backend: {exc}")

with right:
    st.subheader("2 · Review workspace")
    if "generated_document" not in st.session_state:
        st.info("Your generated draft will appear here.")
    else:
        edited = st.text_area(
            "Edit draft",
            value=st.session_state.edited_document,
            height=520,
            label_visibility="collapsed",
        )
        st.session_state.edited_document = edited
        st.caption("Editing happens locally in this session; the text is not sent back to the model unless you generate a new draft.")

        final_document = st.session_state.edited_document
        st.markdown("**Export**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("TXT", create_txt(final_document), "legalease_draft.txt", "text/plain", use_container_width=True)
        with c2:
            st.download_button("DOCX", create_docx(final_document), "legalease_draft.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with c3:
            st.download_button("PDF", create_pdf(final_document), "legalease_draft.pdf", "application/pdf", use_container_width=True)

st.divider()
st.markdown("<div class='small-note'>LegalEase creates AI-assisted drafts, not legal advice. Have a qualified legal professional review a document before signing or relying on it.</div>", unsafe_allow_html=True)
