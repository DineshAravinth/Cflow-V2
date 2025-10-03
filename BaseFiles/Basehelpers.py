import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

class BaseHelpers:

    dashboard_page_xpath = "//p[contains(.,'Dashboard')]"
    workflow_setup_xpath = "(//div[contains(.,'Workflow Setup')])[5]"
    stage_creation_xpath = "//button[contains(.,'Stage Creation')]"
    form_creation_xpath = "//button[contains(.,'Form Creation')]"
    form_page_xpath = "(//span[contains(.,'Form')])[2]"

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def verify_dashboard_page(self):
        locator = (By.XPATH, self.dashboard_page_xpath)
        self.verify_page_by_element(locator, "verify_dashboard_page")

    def verify_workflow_setup_page(self):
        locator = (By.XPATH, self.workflow_setup_xpath)
        self.verify_page_by_element(locator, "verify_workflow_setup_page")

    def verify_stage_creation_page(self):
        locator = (By.XPATH, self.stage_creation_xpath)
        self.verify_page_by_element(locator, "verify_stage_creation_page")

    def verify_form_creation_page(self):
        locator = (By.XPATH, self.form_creation_xpath)
        self.verify_page_by_element(locator, "verify_form_creation_page")

    def verify_section_present(self, section_name):
        """
        Verify that a section (e.g., Main Section, Table Section) is present on the page.
        """
        locator = (By.XPATH, f"//p[contains(.,'{section_name}')]")
        method_name = f"verify_section_present_{section_name.replace(' ', '_')}"
        self.verify_element_present(locator, method_name)

    def verify_initiator_stage_page(self):
        locator = (By.XPATH, "(//span[contains(.,'Initiator')])[2]")
        self.verify_page_by_element(locator, "verify_initiator_stage_inbox_page")

    def verify_form_page(self):
        locator = (By.XPATH, self.form_page_xpath)
        self.verify_page_by_element(locator, "verify_form_page")

    def verify_stage_inbox_page(self, stage_name):
        locator = (By.XPATH, f"(//span[contains(.,'{stage_name}')])[2]")
        method_name = f"verify_{stage_name}_stage_inbox_page"
        self.verify_page_by_element(locator, method_name)



    def click(self, xpath, description="element", retries=3):
        """Click an element safely, handling intercepted clicks and stale elements."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                try:
                    element.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", element)
                print(f"✅ Clicked: {description}")
                return
            except StaleElementReferenceException:
                print(f"⚠️ StaleElementReference, retrying {description} ({attempt + 1}/{retries})")
                time.sleep(0.3)
            except TimeoutException:
                raise AssertionError(f"❌ Timeout: {description} not clickable")
            except NoSuchElementException:
                raise AssertionError(f"❌ Not Found: {description}")

        raise Exception(f"❌ Failed to click {description} after {retries} retries")

    def enter_text(self, xpath, text, description="textbox", retries=3):
        """Enter text safely into an element, retrying on stale references."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                element.clear()
                element.send_keys(text)
                print(f"✅ Entered '{text}' into {description}")
                return
            except StaleElementReferenceException:
                print(f"⚠️ StaleElementReference, retrying {description} ({attempt + 1}/{retries})")
                time.sleep(0.3)
            except TimeoutException:
                raise AssertionError(f"❌ Timeout: {description} not found")
            except NoSuchElementException:
                raise AssertionError(f"❌ Not Found: {description}")

        raise Exception(f"❌ Failed to enter text into {description} after {retries} retries")

    def scroll_to_label(self, label_xpath, friendly_name=None):
        """Scroll to the label and print friendly log instead of raw XPath, centered in viewport."""
        try:
            label = self.wait.until(EC.visibility_of_element_located((By.XPATH, label_xpath)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", label
            )
            log_name = friendly_name if friendly_name else (label.text.strip() or "Label")
            print(f"✅ Label visible – {log_name}")
            return label
        except TimeoutException:
            raise AssertionError(f"❌ Label not found: {label_xpath}")

    def save_screenshot(self, method_name):
        """
        Save a screenshot with timestamp and log the failure.
        """
        d = datetime.now().strftime("%d-%m-%Y-(%H-%M-%S)")  # replace ':' with '-' for file names
        screenshot_path = f"D:/CFLOW-V2/Screenshots/{method_name}-{d}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"❌ {method_name} failed. Screenshot saved at: {screenshot_path}")
        return f"Screenshot saved to {screenshot_path}"

    def verify_page_url(self, expected_url_part, method_name):
        actual_url = self.driver.current_url
        if expected_url_part not in actual_url:
            screenshot_path = self.save_screenshot(method_name)
            print(
                f"⛔ {method_name}: Expected URL to contain '{expected_url_part}', but got '{actual_url}'. Screenshot: {screenshot_path}")
            raise AssertionError(f"URL verification failed. Screenshot: {screenshot_path}")
        else:
            print(f"💚 🏆 ✨ {method_name}: URL verification passed: {actual_url}")

    def verify_page_by_element(self, element_locator, method_name):
        try:
            self.wait.until(EC.visibility_of_element_located(element_locator))
            print(f"💚 🏆 ✨ {method_name}: Page verification passed. Element found: {element_locator[1]}")
        except Exception as e:
            screenshot_path = self.save_screenshot(method_name)
            print(
                f"⛔ {method_name}: Page verification failed. Element not found: {element_locator[1]}")
            raise AssertionError(f"Page verification failed: {str(e)}. Screenshot: {screenshot_path}")

    def verify_element_present(self, element_locator, method_name="verify_element"):
        """
        Verify that a specific element (field, button, label, etc.) is present on the page.

        :param element_locator: tuple like (By.XPATH, "//input[@id='username']")
        :param method_name: friendly name for logging and screenshots
        """
        try:
            self.wait.until(EC.presence_of_element_located(element_locator))
            print(f"💚 🏆 ✨ {method_name}: Element found: {element_locator[1]}")
        except Exception as e:
            screenshot_path = self.save_screenshot(method_name)
            print(f"⛔ {method_name}: Element not found: {element_locator[1]}")
            raise AssertionError(f"Element verification failed: {str(e)}. Screenshot: {screenshot_path}")


