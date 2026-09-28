import os
import sys

import requests
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_core.generator import (format_docx, format_html_preview, format_pdf,  # noqa: E402
                               sanitize_text)
from config import BACKEND_URL, WEB_LOGO_PATH  # noqa: E402

st.set_page_config(page_title="LegalEase", layout="centered")

# ---- Header ----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(WEB_LOGO_PATH):
        st.image(WEB_LOGO_PATH, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

# ---- Inputs ----
document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

# ---- Generate ----
if st.button("Generate Document"):
    if not (document_type.strip() and parties.strip() and dates.strip()):
        st.warning("Please fill in Document Type, Parties Involved and Effective Date.")
    else:
        with st.spinner("Generating your document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={"document_type": document_type, "parties": parties,
                          "terms": terms, "dates": dates},
                    timeout=120,
                )
                response.raise_for_status()
                st.session_state.generated_text = sanitize_text(response.json()["document"])
                st.session_state.doc_type = document_type
                st.session_state.terms = terms
                st.session_state.show_edit = False
                st.success("✅ Document Generated Successfully!")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Start it with: uvicorn legalEaseAPI.main:app --reload")
            except Exception as e:
                st.error(f"Error: {e}")

if "generated_text" not in st.session_state:
    st.info("Click 'Generate Document' to start")
    st.stop()

# ---- Preview ----
styled_html = format_html_preview(st.session_state.generated_text)
st.markdown(
    "<div style='background:#0f1626;color:#e6e6e6;padding:20px;border-radius:10px;"
    f"max-height:350px;overflow-y:auto;'>{styled_html}</div>",
    unsafe_allow_html=True,
)

# ---- Edit ----
if st.button("✏️ Click to Edit Document"):
    st.session_state.show_edit = True

if st.session_state.get("show_edit"):
    edited_text = st.text_area("Edit Document Below:", st.session_state.generated_text, height=300)
    st.session_state.generated_text = edited_text

# ---- Downloads ----
text = st.session_state.generated_text
doc_type = st.session_state.doc_type
fname = doc_type.replace(" ", "_").lower()

st.download_button("📄 Download as .TXT", data=text, file_name=f"{fname}.txt", mime="text/plain")
st.download_button(
    "📝 Download as .DOCX",
    data=format_docx(text, doc_type, st.session_state.get("terms", "")),
    file_name=f"{fname}.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)
st.download_button("📕 Download as .PDF", data=format_pdf(text, doc_type),
                   file_name=f"{fname}.pdf", mime="application/pdf")
