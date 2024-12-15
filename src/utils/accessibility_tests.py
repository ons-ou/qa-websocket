from selenium import webdriver
from axe_selenium_python import Axe
from selenium.webdriver.chrome.options import Options


def accessibility_test(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        axe = Axe(driver)
        axe.inject()
        results = axe.run()

        # Extract violations
        violations = results['violations']
        if not violations:
            print("No accessibility violations found!")
            return []

        extracted_violations = []

        for violation in violations:
            issue = {
                "description": violation['description'],
                "impact": violation['impact'],
                "affected_elements_count": len(violation['nodes'])
            }
            extracted_violations.append(issue)

        print(extracted_violations)
        return extracted_violations
    finally:
        driver.quit()


if __name__ == '__main__':
    print(accessibility_test("https://www.facebook.com/"))
