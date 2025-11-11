from pydantic import BaseModel
from typing import List, Optional

class Course(BaseModel):
    term: str
    course_code: str
    course_name: str
    credits_attempted: float
    credits_earned: float
    grade: int

class GPAStatistics(BaseModel):
    total_courses: int
    total_credits: float
    weighted_average: float
    highest_grade: int
    lowest_grade: int

class TranscriptResponse(BaseModel):
    courses: List[Course]
    statistics: GPAStatistics