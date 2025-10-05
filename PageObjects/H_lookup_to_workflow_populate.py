from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseFiles.Basehelpers import BaseHelpers
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException


class lookup_to_workflow_values:

    button_advanced = "//button[normalize-space(text())='Advanced']"
    lookup_side_nav = "(//span[contains(.,'Lookups')])[2]"
    add_new_button = "//button[contains(.,'Add New')]"
    enter_description_text = "//textarea[@rows='2' and contains(@class,'txt-area-control') and @cfvalidate='']"
    sidenav_workflow_setup = "(//span[contains(.,'Workflow Setup')])[1]"
    select_workflow = "//td[contains(normalize-space(.), 'Test Automate--04-10-2025') and contains(., 'from lookup')]"
    add_new_button_lookup = "(//a[contains(.,'Add New')])[2]"

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base = BaseHelpers(driver, timeout)

    # ---------- Navigation & Basic Actions ----------
    def click_advanced_button(self):
        """Clicks the Advanced button."""
        self.base.click(self.button_advanced, "Advanced button")

    def click_lookup_side_nav(self):
        """Clicks the Lookups option in side navigation."""
        self.base.click(self.lookup_side_nav, "Lookup side navigation")

    def click_add_new_button(self):
        """Clicks the Add New button."""
        self.base.click(self.add_new_button, "Add New button")

    def enter_description(self, description_text):
        """Enters text into the Description textarea."""
        self.base.enter_text(self.enter_description_text, description_text, "Description textarea")

    def open_workflow_setup(self):
        """Opens Workflow Setup section."""
        self.base.click(self.sidenav_workflow_setup, "Workflow Setup")

    def click_workflow(self):
        """Selects a workflow record."""
        self.base.click(self.select_workflow, "Test automation workflow form")

    def click_add_new_button_lookup(self):
        """Clicks the Add New button for Lookup."""
        self.base.click(self.add_new_button_lookup, "Add New Lookup button")

    # ---------- Dropdown Selections (Main + Table) ----------
    def select_workflow_lookup_field(self, option_text, description="Select Workflow/Lookup Field", retries=3):
        """Selects an option from the first Workflow/Lookup Field dropdown (outside the table)."""
        for attempt in range(retries):
            try:
                dropdown_xpath = "//label[contains(.,'Select Workflow/Lookup')]/following::ng-select[1]"
                dropdown_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

                # Open dropdown
                container = dropdown_element.find_element(By.XPATH, ".//div[contains(@class,'ng-select-container')]")
                try:
                    container.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", container)
                sleep(0.5)

                # Search input
                try:
                    search_input = dropdown_element.find_element(By.XPATH, ".//input[@type='text']")
                    search_input.clear()
                    search_input.send_keys(option_text)
                    sleep(1)
                except NoSuchElementException:
                    search_input = None

                # Select option
                option_xpath = f"//div[contains(@class,'ng-option')]//span[normalize-space(text())='{option_text}']"
                option_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
                try:
                    option_element.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", option_element)

                # Tab out
                (search_input or container).send_keys(Keys.TAB)
                print(f"✅ Selected '{option_text}' in '{description}'")
                return
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed for '{description}': {e}")
                sleep(0.5)
        raise Exception(f"Could not select '{option_text}' from '{description}' after {retries} retries")

    def select_target_workflow_lookup_field(self, option_text, description="Target Workflow/Lookup Field", retries=3):
        """Selects an option from Target Workflow/Lookup Field dropdown inside the table."""
        for attempt in range(retries):
            try:
                dropdown_xpath = "//tbody[@formarrayname='mappingFields']//ng-select[1]"
                dropdown_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

                # Open dropdown
                container = dropdown_element.find_element(By.XPATH, ".//div[contains(@class,'ng-select-container')]")
                try:
                    container.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", container)
                sleep(0.5)

                # Search input
                try:
                    search_input = dropdown_element.find_element(By.XPATH, ".//input[@type='text']")
                    search_input.clear()
                    search_input.send_keys(option_text)
                    sleep(1)
                except NoSuchElementException:
                    search_input = None

                # Select exact match
                options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'ng-option')]//span")))
                for opt in options:
                    if opt.text.strip() == option_text:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                        try:
                            opt.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", opt)
                        break
                else:
                    raise Exception(f"Option '{option_text}' not found in dropdown")

                (search_input or container).send_keys(Keys.TAB)
                print(f"✅ Selected '{option_text}' in '{description}'")
                return
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed for '{description}': {e}")
                sleep(0.5)
        raise Exception(f"Could not select '{option_text}' from '{description}' after {retries} retries")

    def select_current_workflow_field(self, option_text, description="Current Workflow Field", row_index=1, retries=3):
        """Selects an option from Current Workflow Field dropdown inside the table."""
        for attempt in range(retries):
            try:
                dropdown_xpath = f"//tbody[@formarrayname='mappingFields']/tr[{row_index}]/td[3]//ng-select"
                dropdown_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

                container = dropdown_element.find_element(By.XPATH, ".//div[contains(@class,'ng-select-container')]")
                try:
                    container.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", container)
                sleep(0.5)

                try:
                    search_input = dropdown_element.find_element(By.XPATH, ".//input[@type='text']")
                    search_input.clear()
                    search_input.send_keys(option_text)
                    sleep(1)
                except NoSuchElementException:
                    search_input = None

                options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'ng-option')]//span")))
                for opt in options:
                    if opt.text.strip() == option_text:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                        try:
                            opt.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", opt)
                        break
                else:
                    raise Exception(f"Option '{option_text}' not found in dropdown")

                (search_input or container).send_keys(Keys.TAB)
                print(f"✅ Selected '{option_text}' in '{description}' (row {row_index})")
                return
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed for '{description}' (row {row_index}): {e}")
                sleep(0.5)
        raise Exception(f"Could not select '{option_text}' from '{description}' after {retries} retries")

    # ---------- Table Dropdown Generic ----------
    def _select_table_dropdown(self, table_name, row_index, column_index, option_text, description, retries=3):
        """Generic method to select an option from any ng-select inside a table."""
        for attempt in range(retries):
            try:
                dropdown_xpath = f"//tbody[@formarrayname='{table_name}']/tr[{row_index}]/td[{column_index}]//ng-select"
                dropdown_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

                container = dropdown_element.find_element(By.XPATH, ".//div[contains(@class,'ng-select-container')]")
                try:
                    container.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", container)
                sleep(0.5)

                try:
                    search_input = dropdown_element.find_element(By.XPATH, ".//input[@type='text']")
                    search_input.clear()
                    search_input.send_keys(option_text)
                    sleep(1)
                except NoSuchElementException:
                    search_input = None

                options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'ng-option')]//span")))
                for opt in options:
                    if opt.text.strip() == option_text:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                        try:
                            opt.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script("arguments[0].click();", opt)
                        break
                else:
                    raise Exception(f"Option '{option_text}' not found in dropdown")

                (search_input or container).send_keys(Keys.TAB)
                print(f"✅ Selected '{option_text}' in '{description}' (row {row_index})")
                return
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed for '{description}' (row {row_index}): {e}")
                sleep(0.5)
        raise Exception(f"Could not select '{option_text}' from '{description}' after {retries} retries")

    def select_populate_target_workflow(self, option_text, row_index=1, retries=3):
        """Selects a Target Workflow / Lookup Field option inside populateFields table."""
        description = "Target Workflow / Lookup Field"
        actual_row = row_index + 1  # skip first row
        self._select_table_dropdown("populateFields", actual_row, 2, option_text, description, retries)

    def select_populate_current_workflow(self, option_text, row_index=1, retries=3):
        """Selects a Current Workflow Field option inside populateFields table."""
        description = "Current Workflow Field"
        actual_row = row_index + 1
        self._select_table_dropdown("populateFields", actual_row, 4, option_text, description, retries)

    def click_add_new_button_for_fields(self, retries=3):
        """
        Click the 'Add New' button reliably with retries and scroll into view.
        """
        button_xpath = "(//a[contains(@title,'Add New') or contains(.,'Add New')])[2]"

        for attempt in range(retries):
            try:
                button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                sleep(0.5)

                # Try clicking directly or via JS if blocked
                try:
                    button.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", button)

                print("✅ Clicked 'Add New' button")
                return  # success, exit the loop

            except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException,
                    NoSuchElementException) as e:
                print(f"⚠️ Attempt {attempt + 1} failed to click 'Add New': {e}")
                sleep(1)

        # If all retries fail
        raise Exception("❌ Could not click 'Add New' button after multiple retries")
