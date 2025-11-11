from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Dict, Union
import io
from pypdf import PdfReader

from app.services.extractor import extract_courses_from_transcript
from app.services.statistics import calculate_statistics

router = APIRouter()

def _extract_text_from_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    parts: List[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n".join(parts)

def process_transcript(file_obj: Union[io.BytesIO, bytes]) -> Dict:
    """
    Accepts a file-like object with .read() or raw bytes, extracts text,
    parses courses, and returns a statistics dict.
    """
    if hasattr(file_obj, "read"):
        pdf_bytes = file_obj.read()
    elif isinstance(file_obj, (bytes, bytearray)):
        pdf_bytes = bytes(file_obj)
    else:
        raise ValueError("Unsupported file object passed to process_transcript")

    # extract text and parse courses
    text = _extract_text_from_bytes(pdf_bytes)
    courses = extract_courses_from_transcript(text)
    stats = calculate_statistics(courses)

    return stats

@router.post("/transcripts")
async def handle_transcript_upload(file: UploadFile = File(...)):
    try:
        file_stats = process_transcript(file.file)
        return JSONResponse(content=file_stats)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)