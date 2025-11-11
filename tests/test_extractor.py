import pytest
from app.services.extractor import extract_text_from_pdf, extract_courses_from_transcript

def test_extract_text_from_pdf():
    # Test with a sample PDF file
    pdf_path = 'tests/sample_transcript.pdf'  # Ensure this sample PDF exists for testing
    text = extract_text_from_pdf(pdf_path)
    assert isinstance(text, str)
    assert len(text) > 0  # Ensure some text is extracted

def test_extract_courses_from_transcript():
    sample_text = """
    2022 Fall/Winter
    CS 101 Introduction to Computer Science 3.0 3.0 85
    MATH 101 Calculus I 3.0 3.0 90
    PHYS 101 Physics I 3.0 3.0 75
    """
    courses = extract_courses_from_transcript(sample_text)
    assert len(courses) == 3
    assert courses[0]['course_code'] == 'CS 101'
    assert courses[1]['grade'] == 90
    assert courses[2]['credits_attempted'] == 3.0

def test_extract_courses_from_transcript_invalid_grade():
    sample_text = """
    2022 Fall/Winter
    CS 101 Introduction to Computer Science 3.0 3.0 IPR
    """
    courses = extract_courses_from_transcript(sample_text)
    assert len(courses) == 0  # No courses should be extracted due to invalid grade