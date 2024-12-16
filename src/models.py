from pydantic import BaseModel, Field
from typing import List, Optional


class Issue(BaseModel):
    issue_type: str = Field(..., description="Type of the bug or issue, e.g., 'Unclosed Tags', 'Repeated CSS'.")
    lines: List[int] = Field(..., description="Line numbers where the issue occurs.")


class HtmlEvaluation(BaseModel):
    global_score: float = Field(..., description="A score representing the overall HTML bug status. 1 means no issues.")
    feedback: List[str] = Field(...,
                                description="General feedback on the HTML structure and suggestions for improvement.")
    issues: List[Issue] = Field(..., description="List of identified issues, including type and line numbers.")


class FunctionalIssue(BaseModel):
    issue_type: str = Field(...,
                            description="Type of the issue, e.g., 'Broken Links', 'Unclickable Buttons', 'Form Issues'.")
    items: List[str] = Field(...,
                             description="List of problematic items, such as links, button labels, or form descriptions.")
    suggestion: str = Field(..., description="Suggestions for fixing the issue.")


class FunctionalTestingEvaluation(BaseModel):
    global_score: float = Field(...,
                                description="A score representing the overall functional status. 1 means no issues.")
    feedback: List[str] = Field(...,
                                description="General feedback on the functionality and suggestions for improvement.")
    issues: List[FunctionalIssue] = Field(..., description="List of identified functional issues with their details.")


class AccessibilityIssue(BaseModel):
    description: str = Field(..., description="A description of the accessibility issue detected.")
    impact: str = Field(..., description="Severity of the issue, e.g., 'high', 'medium', 'low'.")
    affected_elements_count: int = Field(..., description="The number of elements affected by the issue.")


class AccessibilityEvaluation(BaseModel):
    global_score: float = Field(...,
                                description="A score representing the overall accessibility status of the website.")
    feedback: List[str] = Field(..., description="General feedback on the accessibility of the website.")
    issues: List[AccessibilityIssue] = Field(...,
                                             description="List of identified issues with descriptions, impact, and counts.")


class TextEvaluation(BaseModel):
    score: int = Field(..., description="Global score for text structure and overall grammar errors on a scale of 0-1.")
    grammar_and_spelling_issues: List[str] = Field(...,
                                                   description="Description of specific grammar or spelling issues detected.")
    text_structure_evaluation: str = Field(...,
                                           description="Evaluation of the overall structure, e.g., logical organization, clarity.")
    feedback: List[str] = Field(..., description="Specific feedback on improving grammar, structure, and readability.")


class ElementEvaluation(BaseModel):
    element: str = Field(...,
                         description="The name of the element being evaluated, e.g., 'Contact Info', 'Login Form', 'Navigation Menu'.")
    found: bool = Field(..., description="Indicates whether the element was found on the website.")
    usability: Optional[str] = Field(None,
                                     description="A description of the usability of the element, e.g., 'intuitive', 'difficult', or None if not applicable.")


class InformationArchitectureEvaluation(BaseModel):
    website_type: str = Field(..., description="The type of website, e.g., 'Company Site', 'E-commerce', 'Blog'.")
    usability_score: float = Field(...,
                                   description="A score between 0 and 1 representing the overall usability of the website.")
    element_evaluations: List[ElementEvaluation] = Field(...,
                                                         description="A list of evaluations for individual elements like contact info, login form, etc.")
    feedback: List[str] = Field(...,
                                                      description="General feedback summarizing strengths, weaknesses, and suggestions.")
