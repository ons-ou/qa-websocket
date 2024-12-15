from crewai import Task
from agents import agents
from utils.accessibility_tests import accessibility_test
from utils.get_html import get_html, html_to_text
from utils.get_html_bugs import count_html_bugs


def tasks(llm_8b, llm_70b, url):
    """
    job_requirements_research - Find the relevant skills, projects and experience
    resume_swot_analysis- understand the report and the resume based on this make a swot analysis
    """

    html = get_html(url)
    bugs_report = count_html_bugs(html)
    accessibility_violations = accessibility_test(url)
    text_content = html_to_text(html)

    html_bug_checker_agent, accessibility_advisor, text_content_evaluator, information_architecture_evaluator = agents(
        llm_8b, llm_70b)

    html_bugs_feedback = Task(
        name='HtmlEvaluation',
        description=
        f'Given these details about HTML bugs of an HTML page: '
        f'1. "global_score": {bugs_report["global_score"]} - Highest score is 1 which means no issues at all. '
        f'2. "unclosed_tags_details": {bugs_report["unclosed_tags"]} - An array of the lines causing problems. If '
        f'empty then there are no issues. '
        f'3. "repeated_css_details": {bugs_report["repeated_css"]} - An array of the lines causing problems. If '
        f'empty then there are no issues. '
        f'Generate a feedback for each bug type.'
        f'If there are no issues, just provide a positive feedback and move on. If there are issues, then in the '
        f'json, add an array of lines where they are happening and how to fix them in one feedback.',
        expected_output=(
            "The expected output is a JSON object with the following structure:"
            "The expected output is a JSON object that represents the HTML bug feedback with the following structure:"
            "{\"global_score\": (float),  # A score representing the overall HTML bug status. It has the same value as the one in input."
            "  \"feedback\": (string),  # A string providing a general overview of the feedback on the HTML structure as well as suggestions on how to fix it."
            "  \"issues\": ["
            "    {"
            "      \"issue_type\": (string),  # Type of the bug or issue, e.g., \"Unclosed Tags\", \"Repeated CSS\"."
            "      \"lines\": ["
            "        (int)  # Line numbers where the issue occurs (e.g., [5, 7, 10])."
            "      ]"
            "    }"
            "  ]"
            "}"
        ),
        agent=html_bug_checker_agent
    )

    html_accessibility_task = Task(
        name="AccessibilityEvaluation",
        description=(
            f'Input: {accessibility_violations}'
            f'Analyze the provided accessibility data and generate a comprehensive report. The analysis should include: '
            f'1. A global accessibility score based on the severity and number of issues detected.'
            f'2. Feedback on the accessibility of the website, highlighting its strengths and areas for improvement.'
            f'3. A list of identified issues, including their descriptions and severity levels.'
        ),
        expected_output=(
            "The expected output is a JSON object with the following structure:"
            "{"
            "  \"global_score\": (float),  # A score representing the overall accessibility status of the website. Value is the same as the one in the input."
            "  \"feedback\": (string),  # General feedback on the accessibility, including strengths and areas for improvement."
            "  \"issues\": ["
            "    {"
            "      \"description\": (string),  # A description of the accessibility issue detected."
            "      \"impact\": (string),  # A string representing the severity of the issue (e.g., \"high\", \"medium\", \"low\")."
            "      \"affected_elements_count\": (int)  # The number of elements affected by the issue."
            "    }"
            "  ]"
            "}"
        ),
        agent=accessibility_advisor
    )

    text_content_analysis_task = Task(
        name="TextEvaluation",
        description=(
            f'Analyze the provided text content of a webpage to evaluate its quality. The analysis should include:'
            f'1. An analysis of grammar and language issues, including the type and number of mistakes detected.'
            f'2. An evaluation of the overall structure, including logical organization and clarity.'
            f'3. Specific feedback to improve the text’s readability, grammar, and structure.'
            f'Input: {text_content}'
        ),
        expected_output=(
            "The expected output is a JSON object with the following structure:"
            "{"
            "  \"grammar_and_spelling_issues\": {"
            "      \"score\": (int),  # Grammar and spelling score (0-1 scale)."
            "      \"details\": (string)  # A description of the specific grammar or spelling issues detected."
            "  },"
            "  \"text_structure_evaluation\": (string),  # Evaluation of the overall structure (e.g., logical organization, clarity)."
            "  \"feedback\": ["
            "    (string)  # Specific feedback on how to improve grammar, structure, and readability."
            "  ]"
            "}"

        ),
        agent=text_content_evaluator
    )

    information_architecture_task = Task(
        name="InformationArchitectureEvaluation",
        description=(
            f'Analyze the provided webpage to evaluate its information architecture. The analysis should include:'
            f'1. Identification of the website type (e.g., e-commerce, corporate, blog, etc.).'
            f'2. An assessment of the presence and adequacy of key elements for the identified website type (e.g., '
            f'navigation menus, headers, footers, content organization). '
            f'3. An evaluation of how well the website’s structure supports usability and user experience.'
            f'4. A calculation of an overall information architecture score based on the completeness and quality of '
            f'the elements. '
            f'5. Specific feedback to improve the website’s information architecture.'
            f'Input: {text_content}'
        ),
        expected_output=(
            "The expected output is a JSON object that represents the information architecture feedback with the following structure:"
            "{'website_type': (string),  # The type of website (e.g., 'e-commerce', 'corporate', 'blog')."
            "  'information_architecture_score': (float),  # A score indicating the quality of the website's information architecture."
            "  'assessment': {"
            "    (key): (value),  # Key elements that were assessed (e.g., navigation menus, headers, footers)."
            "  },"
            "  'feedback': ["
            "    (string)  # Feedback on how to improve the website's information architecture (e.g., better navigation, clearer content structure)."
            "  ]"
            "}"
        ),
        agent=information_architecture_evaluator
    )

    return [html_bugs_feedback, html_accessibility_task, text_content_analysis_task]
