import asyncio

from crewai import Task
from agents import agents
from utils.functional_tests import functionality_tests
from utils.accessibility_tests import accessibility_test
from utils.get_html import get_html, html_to_text
from utils.get_html_bugs import count_html_bugs
from models import *


async def tasks(llm_8b, llm_70b, url):
    html = get_html(url)
    final_tasks = [
        count_html_bugs(html),
        functionality_tests(url),
        accessibility_test(url),
        html_to_text(html),
    ]

    bugs_report, test_report, accessibility_violations, text_content = await asyncio.gather(*final_tasks)

    html_bug_checker_agent, functional_testing_agent, accessibility_advisor, text_content_evaluator, information_architecture_agent = agents(
        llm_8b, llm_70b)

    html_bugs_feedback = Task(
        name='HtmlEvaluation',
        description=(
            f'Given these details about HTML bugs of an HTML page: '
            f'1. "global_score": {bugs_report["global_score"]} - Highest score is 1 which means no issues at all. '
            f'2. "unclosed_tags_details": {bugs_report["unclosed_tags"]} - An array of the lines causing problems. If '
            f'empty then there are no issues. '
            f'3. "repeated_css_details": {bugs_report["repeated_css"]} - An array of the lines causing problems. If '
            f'empty then there are no issues. '
            f'Generate a feedback for each bug type. '
            f'If there are no issues, just provide positive feedback and move on. If there are issues, then in the '
            f'JSON, add an array of lines where they are happening and how to fix them in one feedback.'
        ),
        expected_output=(
            "The expected output is a JSON object summarizing the feedback and issues detected in the HTML."
        ),
        output_json=HtmlEvaluation,
        agent=html_bug_checker_agent
    )

    functional_testing_task = Task(
            name='FunctionalTestingEvaluation',
            description=(
                f'Given these details about functional testing of a webpage: '
                f'1. "global_score": {test_report["global_score"]} - Highest score is 1 which means no issues at all. '
                f'2. "unclickable_buttons": {test_report["unclickable_buttons"]} - An array of button names or IDs that are '
                f'unclickable. If empty then there are no issues. '
                f'3. "form_issues": {test_report["form_issues"]} - An array of descriptions of issues in forms. If empty then '
                f'there are no issues. '
                f'Generate feedback for each issue type. If there are no issues, provide positive feedback and move on.'
                f'If there are issues, include detailed feedback for each issue type in the JSON, specifying the problematic '
                f'items and suggestions for fixing them.'
            ),
            expected_output=(
                "The expected output is a JSON object summarizing the feedback and issues detected in the functional testing."
            ),
            output_json=FunctionalTestingEvaluation,
            agent=functional_testing_agent
        )

    html_accessibility_task = Task(
        name="AccessibilityEvaluation",
        description=(
            f'Input: {accessibility_violations}'
            f'Analyze the provided accessibility data and generate a comprehensive report. The analysis should include: '
            f'1. A global accessibility score based on the severity and number of issues detected. '
            f'2. Feedback on the accessibility of the website, highlighting its strengths and areas for improvement. '
            f'3. A list of identified issues, including their descriptions and severity levels.'
        ),
        expected_output=(
            "The expected output is a JSON object summarizing the accessibility feedback, strengths, and issues."
        ),
        output_json=AccessibilityEvaluation,
        agent=accessibility_advisor
    )

    text_content_analysis_task = Task(
        name="TextEvaluation",
        description=(
            f'Analyze the provided text content of a webpage to evaluate its quality. The analysis should include: '
            f'1. A score of the page content overall.'
            f'2. An analysis of grammar and language issues, including the type and number of mistakes detected. '
            f'3. An evaluation of the overall structure, including logical organization and clarity. '
            f'4. Specific feedback to improve the text’s readability, grammar, and structure. '
            f'Input: {text_content}'
        ),
        expected_output=(
            "The expected output is a JSON object summarizing the analysis of grammar, structure, and feedback."
        ),
        output_json=TextEvaluation,
        agent=text_content_evaluator
    )

    information_architecture_task = Task(
        name='InformationArchitectureEvaluation',
        description=(
            f'Input: {url}'
            f'Analyze the provided website data using the WebsiteSearchTool and evaluate its information architecture. '
            f'1. Determine the type of website (e.g., company site, e-commerce, blog). '
            f'2. Evaluate how easy it is to locate the following key elements: contact information, login form, navigation menus, and relevant content sections. '
            f'3. Provide feedback on usability and information organization, highlighting strengths and weaknesses. '
            f'4. Consider that some elements may not apply to all websites (e.g., company sites may not have login forms). '
        ),
        expected_output=(
            f'Return a JSON object summarizing: '
            f'(a) Website type. '
            f'(b) Usability score (0-1). '
            f'(c) A detailed breakdown of element accessibility with suggestions for improvement.'
        ),
        output_json=InformationArchitectureEvaluation,
        agent=information_architecture_agent
    )

    return [html_bugs_feedback, functional_testing_task, html_accessibility_task, text_content_analysis_task]

