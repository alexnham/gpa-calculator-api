import re
from typing import List, Dict, Optional

def calculate_statistics(courses: List[Dict]) -> Dict:
    """Calculate GPA and other statistics from courses."""
    if not courses:
        return {
            "total_courses": 0,
            "total_credits": 0,
            "weighted_average": 0.0,
            "highest_grade": None,
            "lowest_grade": None
        }
    
    total_credits = sum(c['credits_earned'] for c in courses)
    weighted_sum = sum(c['grade'] * c['credits_earned'] for c in courses)
    average = weighted_sum / total_credits if total_credits > 0 else 0
    
    return {
        'total_courses': len(courses),
        'total_credits': total_credits,
        'weighted_average': round(average, 2),
        'highest_grade': max(c['grade'] for c in courses),
        'lowest_grade': min(c['grade'] for c in courses)
    }