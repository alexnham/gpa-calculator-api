from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf_and_get_uwo_average():
    with open("tests/sample_transcript.pdf", "rb") as pdf_file:
        response = client.post(
            "/api/v1/transcripts/uwo",
            files={"file": ("sample_transcript.pdf", pdf_file, "application/pdf")},
        )
    assert response.status_code == 201
    data = response.json()
    assert "uwo_average_gpa" in data
    assert "count" in data
    assert isinstance(data["uwo_average_gpa"], (int, float))
    assert 0.0 <= data["uwo_average_gpa"] <= 4.0
    assert isinstance(data["count"], int)
    assert data["count"]