
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from datetime import datetime


class CreateWorkflow:
    # Locators
    sidenav_workflow_setup = "(//span[contains(.,'Workflow Setup')])[1]"
    button_add_new_workflow = "//a[contains(.,' Add New')]"
    textbox_workflow_name = "//input[@placeholder='Enter Your Workflow Name']"
    button_create_workflow = "//button[contains(.,' Create')]"

    # Stage 1 locators
    button_add_stage_s1 = "//summary[@class ='popover-button']"
    option_add_stage_s1 = "//button[contains(.,'Add Stage')]"
    textbox_stage_name_s1 = "//input[@title='displayName']"
    button_save_stage_s1 = "//button[contains(.,' Save')]"

    # Stage 2 locators
    button_add_stage_s2 = "(//summary[@class ='popover-button'])[2]"
    option_add_stage_s2 = "(//button[contains(.,'Add Stage')])[2]"
    textbox_stage_name_s2 = "//input[@title='displayName']"
    button_save_stage_s2 = "//button[contains(.,' Save')]"

    # Stage 3 locators
    button_add_stage_s3 = "(//summary[@class ='popover-button'])[3]"
    option_add_stage_s3 = "(//button[contains(.,'Add Stage')])[3]"
    textbox_stage_name_s3 = "//input[@title='displayName']"
    button_save_stage_s3 = "//button[contains(.,' Save')]"

    button_form_creation = "(//button[@type='button'])[2]"


    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------------- Generic helpers ---------------- #
    def click(self, xpath, description="element"):
        """Generic click with wait, scroll, and JS fallback"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            try:
                element.click()
            except ElementClickInterceptedException:
                # fallback if blocked by overlay
                self.driver.execute_script("arguments[0].click();", element)

            print(f"✅ Clicked: {description}")
        except TimeoutException:
            print(f"❌ Timeout: {description} not clickable")
            raise
        except NoSuchElementException:
            print(f"❌ Not Found: {description}")
            raise

    def enter_text(self, xpath, text, description="textbox"):
        """Generic send_keys with wait"""
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.clear()
            element.send_keys(text)
            print(f"✅ Entered '{text}' into {description}")
        except TimeoutException:
            print(f"❌ Timeout: {description} not found")
            raise
        except NoSuchElementException:
            print(f"❌ Not Found: {description}")
            raise

    # ---------------- Workflow Actions ---------------- #
    def open_workflow_setup(self):
        self.click(self.sidenav_workflow_setup, "Workflow Setup")

    def click_add_new_workflow(self):
        self.click(self.button_add_new_workflow, "Add New Workflow button")

    def enter_unique_workflow_name(self, base_name="Test Automate"):
        """Generate a unique workflow name with timestamp and enter it"""
        current_time = datetime.now().strftime("%d-%m-%Y,%H:%M")
        unique_name = f"{base_name} -- {current_time}"
        self.enter_text(self.textbox_workflow_name, unique_name, "Workflow Name")
        print(f"⚡ Workflow Created: {unique_name}")
        return unique_name

    def click_create_workflow(self):
        self.click(self.button_create_workflow, "Create Workflow button")

    # ---------------- Stage 1 ---------------- #
    def click_add_stage_button_s1(self):
        self.click(self.button_add_stage_s1, "Add Stage (S1) button")

    def select_add_stage_s1(self):
        self.click(self.option_add_stage_s1, "Add Stage option (S1)")

    def enter_stage_name_s1(self, stage_name="PS1"):
        self.enter_text(self.textbox_stage_name_s1, stage_name, "Stage Name S1")

    def save_stage_s1(self):
        self.click(self.button_save_stage_s1, "Save Stage S1")

    # ---------------- Stage 2 ---------------- #
    def click_add_stage_button_s2(self):
        self.click(self.button_add_stage_s2, "Add Stage (S2) button")

    def select_add_stage_s2(self):
        self.click(self.option_add_stage_s2, "Add Stage option (S2)")

    def enter_stage_name_s2(self, stage_name="PS2"):
        self.enter_text(self.textbox_stage_name_s2, stage_name, "Stage Name S2")

    def save_stage_s2(self):
        self.click(self.button_save_stage_s2, "Save Stage S2")

    def form_creation(self):
        self.click(self.button_form_creation)

    # ---------------- Stage 3 ---------------- #
    def click_add_stage_button_s3(self):
            self.click(self.button_add_stage_s3, "Add Stage (S3) button")

    def select_add_stage_s3(self):
        self.click(self.option_add_stage_s3, "Add Stage option (S3)")

    def enter_stage_name_s3(self, stage_name="PS3"):
        self.enter_text(self.textbox_stage_name_s3, stage_name, "Stage Name S3")

    def save_stage_s3(self):
        self.click(self.button_save_stage_s3, "Save Stage S3")

    def form_creation(self):
        self.click(self.button_form_creation)
