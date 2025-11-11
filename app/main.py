from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import Response as StarletteResponse
import asyncio
import io
import inspect
from pypdf import PdfReader

from app.api.v1.endpoints.transcripts import process_transcript
from app.core.config import settings
from app.services.extractor import extract_courses_from_transcript

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.post("/api/v1/transcripts/")
async def upload_transcript(file: UploadFile = File(...)):
    # Basic file-type validation to match tests (422 for invalid type)
    filename = (file.filename or "").lower()
    if not filename.endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF uploads are accepted")

    try:
        pdf_bytes = await file.read()
        # processor expects a file-like object; wrap bytes in BytesIO
        pdf_file = io.BytesIO(pdf_bytes)

        # Call processor safely whether it's sync or async and whether it
        # returns a coroutine or direct value.
        if inspect.iscoroutinefunction(process_transcript):
            result = await process_transcript(pdf_file)
        else:
            result = process_transcript(pdf_file)
        if inspect.isawaitable(result):
            result = await result

        # If the processor already returned a Response (JSONResponse/etc), forward it.
        if isinstance(result, StarletteResponse):
            return result

        # Expect (courses, statistics) otherwise accept a dict as statistics.
        if isinstance(result, (list, tuple)) and len(result) == 2:
            courses, statistics = result
            return JSONResponse(content=statistics)

        if isinstance(result, dict):
            return JSONResponse(content=result)

        raise HTTPException(status_code=500, detail="Unexpected response from processor")
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

def _convert_percent_to_uwo_gpa(percent: int) -> float:
    """Convert numeric percent grade to UWO 4.0-scale GPA (per table provided)."""
    if percent >= 90:
        return 4.0
    if 85 <= percent <= 89:
        return 3.9
    if 80 <= percent <= 84:
        return 3.7
    if 77 <= percent <= 79:
        return 3.3
    if 73 <= percent <= 76:
        return 3.0
    if 70 <= percent <= 72:
        return 2.7
    if 67 <= percent <= 69:
        return 2.3
    if 63 <= percent <= 66:
        return 2.0
    if 60 <= percent <= 62:
        return 1.7
    if 57 <= percent <= 59:
        return 1.3
    if 53 <= percent <= 56:
        return 1.0
    if 50 <= percent <= 52:
        return 0.7
    return 0.0  # 0-49 => F

@app.post("/api/v1/transcripts/uwo")
async def upload_transcript_uwo(file: UploadFile = File(...)):
    """
    Accepts a PDF upload, converts each numeric course grade to UWO GPA
    (per provided table) and returns the simple average of those GPAs.
    """
    filename = (file.filename or "").lower()
    if not filename.endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF uploads are accepted")

    try:
        pdf_bytes = await file.read()
        pdf_file = io.BytesIO(pdf_bytes)

        # Extract text from PDF using pypdf
        reader = PdfReader(pdf_file)
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        transcript_text = "\n".join(parts)

        # Parse courses (uses your existing extractor)
        courses = extract_courses_from_transcript(transcript_text)

        # Convert numeric grades to UWO GPA scale and average the GPAs (simple average)
        gpas = []
        for c in courses:
            grade = c.get("grade")
            if isinstance(grade, (int, float)):
                gpas.append(_convert_percent_to_uwo_gpa(int(grade)))

        if not gpas:
            return JSONResponse(content={"uwo_average_gpa": 0.0, "count": 0})

        avg = sum(gpas) / len(gpas)
        return JSONResponse(content={"uwo_average_gpa": round(avg, 2), "count": len(gpas)})
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
#