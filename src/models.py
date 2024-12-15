from pydantic import BaseModel
from typing import List


class Issue(BaseModel):
    issue_type: str
    lines: List[int]


class HtmlEvaluation(BaseModel):
    global_score: float
    feedback: str
    issues: List[Issue]


class AccessibilityIssue(BaseModel):
    description: str
    impact: str
    affected_elements_count: int


class AccessibilityEvaluation(BaseModel):
    global_score: float
    feedback: str
    issues: List[AccessibilityIssue]


class GrammarAndSpellingIssues(BaseModel):
    score: int
    details: str


class TextEvaluation(BaseModel):
    grammar_and_spelling_issues: GrammarAndSpellingIssues
    text_structure_evaluation: str
    feedback: List[str]

