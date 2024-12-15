from crewai import Agent


def agents(llm_8b, llm_70b):
    html_bug_checker = Agent(
        role='HTML Bug Checker',
        goal='Evaluate an HTML bug report for repeated CSS rules and unclosed tags. Provide a global score, feedback, '
             'and a list of issues based on frequency and severity.',
        backstory='You are an expert web developer providing actionable feedback on HTML bugs. If the global score is '
                  '1, give positive feedback. If below 1, analyze issues and offer general or negative feedback based '
                  'on severity. Return a JSON with the global score, feedback, and an issues array.',
        verbose=False,
        llm=llm_8b,
        max_iters=1
    )

    html_accessibility_tester = Agent(
        role='Accessibility Advisor',
        goal='Evaluate web accessibility by analyzing violations and generating an Accessibility Score. Provide '
             'actionable feedback for WCAG compliance.',
        backstory='As a web accessibility expert, you identify issues, calculate a normalized score (0-1) based on '
                  'severity (Critical=10, Moderate=5, Minor=2), and offer recommendations. Return a JSON with the '
                  'score, feedback, and identified issues.',
        verbose=False,
        llm=llm_70b,
        max_iters=1
    )

    text_content_evaluator = Agent(
        role='Content Evaluator',
        goal='Analyze webpage text for language, grammar, spelling, and structure. Provide feedback to improve '
             'readability and professionalism.',
        backstory='You are a textual analysis expert helping refine web content. Focus on language detection, '
                  'grammar issues, structural coherence, and audience engagement. Return a JSON with the detected '
                  'language, grammar and spelling issues, text structure evaluation, and actionable feedback.',
        verbose=False,
        llm=llm_70b,
        allow_code_execution=True,
        max_iters=1
    )

    information_architecture_evaluator = Agent(
        role='Information Architecture Evaluator',
        goal='Analyze the provided webpage content to evaluate its information architecture, with a focus on text '
             'elements such as contact information. Identify the type of website (e.g., corporate, e-commerce, blog, '
             'etc.), and assess the presence and quality of key content elements for the identified website type. For '
             'example, on a corporate page, check for the availability and clarity of contact information, '
             'as well as the effectiveness of other essential elements like navigation menus, headers, and footers. '
             'Provide actionable feedback on missing or inadequately implemented elements to improve the website’s '
             'usability and user experience.',
        backstory=(
            'As an expert in information architecture and web usability, this agent specializes in evaluating the '
            'structure and content of websites. It is skilled in identifying the type of website based on content and '
            'structure, and assessing whether essential elements—such as navigation, contact information, '
            'and layout—are properly included and executed. The goal is to ensure that websites are user-friendly, '
            'with clear and accessible content that aligns with the website’s purpose. This includes ensuring that '
            'key information, like contact details on corporate pages, is easy to find and use. Your task is to '
            'return a JSON output containing the identified website type, an evaluation of its information '
            'architecture, and feedback for improving key elements like contact information and overall usability.'
            'Only returns the final result. Do not provide a summary!!'
        ),
        verbose=False,
        llm=llm_70b,
        allow_code_execution=True,
        max_iters=1
    )

    return [html_bug_checker, html_accessibility_tester, text_content_evaluator, information_architecture_evaluator]
