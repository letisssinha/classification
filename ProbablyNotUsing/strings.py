##FIND A WAY TO IGNORE PLURAL 
import re

indicator_patterns = [
    r"\bperformance indicators?\b",
    r"\bperformance measures?\b",
    r"\bmeasure[s]? of performance\b",
    r"\bperformance metrics?\b",
    r"\bmetrics? of performance\b",
    r"\bKPIs?\b",
    r"\bkey performance indicators?\b",
    r"\bindicators? of performance\b"
]

MODEL = {
    'self-assessment excellence',
    'EFQM',
    'Cross and Lynch',
    'SMART',
    'Performance Prism', 
    'SCOR',
    'Activity-Based Costing',
    'ABC',
    'Objectives and Key Results',
    'OKRs',
    '360-Degree Feedback'
}

MODELS_PATTERN = r"\b(?:self[- ]?assessment excellences?|EFQMs?|Cross and Lynch(?:es)?|SMARTs?|Performance Prisms?|SCORs?|Activity[- ]Based Costings?|ABCs?|Objectives? and Key Results?|OKRs?|360[- ]Degree Feedbacks?)\b"


