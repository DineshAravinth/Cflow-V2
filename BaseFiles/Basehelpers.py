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


class BaseHelpers:
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

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

