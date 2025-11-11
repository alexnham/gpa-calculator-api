from typing import List, Dict
import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        text = "\n".join(text_parts)
    return text

def extract_courses_from_transcript(text: str) -> List[Dict]:
    courses = []
    pattern = r'([A-Z]+)\s+(\d+[A-Z]?)\s+(.+?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+|IPR|[A-Z]+)'
    lines = text.split('\n')
    current_term = None
    
    for line in lines:
        if re.search(r'\d{4}\s+(Fall/Winter|Summer)', line):
            current_term = line.strip()
        
        match = re.search(pattern, line)
        if match:
            dept, code, name, attempted, earned, grade = match.groups()
            if not grade.isdigit():
                continue
            
            courses.append({
                'term': current_term,
                'course_code': f"{dept} {code}",
                'course_name': name.strip(),
                'credits_attempted': float(attempted),
                'credits_earned': float(earned),
                'grade': int(grade)
            })
    
    return courses