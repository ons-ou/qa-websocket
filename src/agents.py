from crewai import Agent
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool

search_tool = SerperDevTool()


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

    functional_testing_agent = Agent(
        role='Form and Button Feedback Generator',
        goal='Analyze provided issues related to unclickable buttons and problematic forms on a webpage. Based on the input, '
             'generate a global score, detailed feedback, and suggestions for improvement.',
        backstory='You are a QA specialist focusing on forms and buttons in web functionality testing. You will receive a '
                  'preprocessed list of unclickable buttons and form-related issues as input, along with a global score. '
                  'If the global score is 1, confirm everything is working perfectly and return only positive feedback. '
                  'If the score is below 1, analyze the provided issues, classify them by severity, and offer constructive '
                  'feedback. Return a JSON containing the global score, feedback, and a structured list of issues, each '
                  'with a description, severity level, and recommendations.',
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
        llm=llm_8b,
        max_iters=1
    )

    text_content_evaluator = Agent(
        role='Content Evaluator',
        goal='Analyze webpage text for language, grammar, spelling, and structure. Provide feedback to improve '
             'readability and professionalism.',
        backstory='You are a textual analysis expert helping refine web content. Focus on language detection, '
                  'grammar issues, structural coherence, and audience engagement. '
                  'If the overall structure is good return a number closer to 1, else one closer to 0.'
                  'Return a JSON with a score'
                  'of the overall webpage content on a scale of 0-1, grammar and spelling issues, text structure evaluation, and actionable feedback.',
        verbose=True,
        llm=llm_70b,
        max_iters=1
    )

    information_architecture_agent = Agent(
        role='Information Architecture Evaluator',
        goal='Evaluate the information architecture of a website by identifying its type and assessing how easy it is '
             'to locate key elements such as contact information, login forms, and other relevant content. Take into '
             'account that not all elements are available on all website types (e.g., company sites may lack login '
             'forms).',
        backstory='You are a web usability expert specializing in analyzing website information architecture. Your '
                  'task is to classify the type of website (e.g., company site, e-commerce, blog, etc.) based on the '
                  'provided data and evaluate how intuitive and efficient the information architecture is for '
                  'locating important elements. '
                  'Provide feedback on usability, identify missing elements where applicable, and score the '
                  'architecture based on its ability to meet user needs effectively.',
        verbose=True,
        llm=llm_70b,
        tools=[search_tool],
        max_iters=1
    )

    return [html_bug_checker, functional_testing_agent, html_accessibility_tester, text_content_evaluator, information_architecture_agent]
