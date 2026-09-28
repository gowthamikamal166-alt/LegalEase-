from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = ""
    dates: str = Field(..., min_length=2)


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        response = gemini_generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
    except Exception as exc:  # surface AI/API errors to the client
        raise HTTPException(status_code=502, detail=f"Generation failed: {exc}")
    return {"document": response}
