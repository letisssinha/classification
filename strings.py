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
    'Performance measurement models',
    'Performance measurement model',
    'model',
    'Balanced Scorecard',
    'BCS'
}

