import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf_and_get_gpa_statistics():
    with open("tests/sample_transcript.pdf", "rb") as pdf_file:
        response = client.post("/api/v1/transcripts/", files={"file": pdf_file})
    print(response.json())
    assert response.status_code == 200
    assert "total_courses" in response.json()
    assert "total_credits" in response.json()
    assert "weighted_average" in response.json()
    assert "highest_grade" in response.json()
    assert "lowest_grade" in response.json()


def test_upload_invalid_pdf():
    response = client.post("/api/v1/transcripts/", files={"file": ("invalid.txt", b"invalid content")})
    
    assert response.status_code == 422  # Unprocessable Entity for invalid file type

def test_upload_empty_pdf():
    with open("tests/test_empty_transcript.pdf", "rb") as pdf_file:
        response = client.post("/api/v1/transcripts/", files={"file": pdf_file})
    
    assert response.status_code == 400
