from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


async def functionality_tests(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        print(f"Page loaded: {url}")
        time.sleep(5)

        buttons = driver.find_elements(By.TAG_NAME, "button")
        links = driver.find_elements(By.TAG_NAME, "a")
        forms = driver.find_elements(By.TAG_NAME, "form")

        print(f"Found {len(buttons)} buttons, {len(links)} links, {len(forms)} forms.")

        unclickable_buttons = []
        for button in buttons:
            if button.get_attribute("disabled") or button.value_of_css_property("display") == "none":
                button_id = button.get_attribute("id") or button.get_attribute("name") or button.get_attribute("class") or "Unnamed Button"
                unclickable_buttons.append(f"Button: {button_id}")

        form_issues = []
        for form in forms:
            try:
                form_name = form.get_attribute("name") or form.get_attribute("id") or "Unnamed Form"
                inputs = form.find_elements(By.TAG_NAME, "input")
                input_count = len(inputs)
                if input_count == 0:
                    form_issues.append(f"{form_name}: Form has no input fields.")
                try:
                    form.submit()
                except Exception as e:
                    print(f"Error submitting form '{form_name}': {e}")
                    form_issues.append(f"{form_name}: Form submission failed.")
            except Exception as e:
                print(f"Error processing form: {e}")

        unclickable_buttons_ratio = 1 - (len(unclickable_buttons) / max(len(buttons), 1))
        form_issues_ratio = 1 - (len(form_issues) / max(len(forms), 1))

        response = {
            "global_score": round(unclickable_buttons_ratio * 0.3 + form_issues_ratio * 0.7, 2),
            "unclickable_buttons": unclickable_buttons,
            "form_issues": form_issues
        }

        print(response)
        return response

    except Exception as e:
        print(f"An error occurred during functionality tests: {e}")
        return "Error"

    finally:
        driver.quit()
        print("WebDriver closed.")

