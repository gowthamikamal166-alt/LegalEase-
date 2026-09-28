"""Gemini integration: builds the prompt and generates the legal document text."""
import os
import sys

import google.generativeai as genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY, GEMINI_MODEL  # noqa: E402


class GeminiDocumentGenerator:
    def __init__(self, model_name: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        term_list = "\n".join(f"- {t.strip()}" for t in terms.split(";") if t.strip())
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions to include:\n{term_list}\n\n"
            "Requirements:\n"
            "- Use formal legal structure with numbered sections and clear legal clauses "
            "(recitals, definitions where relevant, obligations, term and termination, "
            "confidentiality, governing law, severability, entire agreement, signatures).\n"
            "- Section headings must be on their own line, e.g. '1. Services:'.\n"
            "- Use [square brackets] for any detail not supplied by the user.\n"
            "- Output plain text only: no markdown symbols, no commentary before or after the document."
        )
        response = self.model.generate_content(prompt)
        return response.text
