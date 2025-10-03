import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseFiles.Basehelpers import BaseHelpers

class rules_condition_verification:

    select_workflow = "//a[contains(.,' AUTOMATION PAGE - RULES ENGINE CONDITIONS ')]"

    s1_textbox_input = "//input[@id='S1_TextBox']"
    SUBMIT_BTN = "//button[contains(.,'Submit Form')]"

    # Table / Record locators
    CURRENT_STATUS_CELL = "//td[@data-title='Current Status']"
    ID_CELLS = "//td[@data-title='ID' and @currecordid]"

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base = BaseHelpers(driver, timeout)

    def click_workflow(self):
        self.base.click(self.select_workflow, "AUTOMATION PAGE - RULES ENGINE CONDITIONS --- WORKFLOW")

    # ---------------- Helper ---------------- #
    def scroll_to_element(self, locator, timeout=10):
        """Scroll to an element after waiting for it to appear."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
            )
            print(f"✅ Scrolled to element: {locator}")
        except Exception as e:
            print(f"❌ Failed to scroll to element: {locator} | Error: {e}")

    def get_latest_record_status(self, status_column_name="Current Status"):
        """Fetch the latest record ID and Current Status from table."""
        status_cells = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//td[@data-title='{status_column_name}']"))
        )

        record_map = {}
        for cell in status_cells:
            cur_id = cell.get_attribute("currecordid")
            if cur_id and cur_id.isdigit():
                record_map[int(cur_id)] = cell

        if not record_map:
            raise AssertionError("❌ No records found for Current Status")

        latest_id = max(record_map.keys())
        latest_cell = record_map[latest_id]
        badge_span = latest_cell.find_element(By.TAG_NAME, "span")
        current_status = badge_span.text.strip()

        print(f"✅ Latest Record ID: {latest_id}, Current Status: {current_status}")
        return latest_id, current_status

    # ---------------- S1 Rule Verification ---------------- #
    def verify_equal_to_rule_s1(self, negative_values=None, positive_value="dinesh"):
        """
        Verify Equal To Rule for S1 stage:
        - Negative values should stay in Initiator
        - Positive value should move to S1(EQUAL TO)
        """
        if negative_values is None:
            negative_values = ["aravinth", "testuser", "demo", "  "]

        print(f"⚠️ Negative values to test: {', '.join(negative_values)}")

        # 🔹 Negative value checks
        for neg_val in negative_values:
            print(f"➡️  Trying negative value: {neg_val}")
            self.base.enter_text(self.s1_textbox_input, neg_val, "S1 TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.base.verify_initiator_stage_page()
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(2)  # wait for table update

            latest_id, current_status = self.get_latest_record_status()
            if current_status != "Initiator":
                raise AssertionError(f"❌ Negative value '{neg_val}' wrongly moved to {current_status}")
            print(f"☹️ ❌  Negative value '{neg_val}' correctly stayed in Initiator stage")

            # Reopen latest record for retry
            self.base.click(f"//td[@data-title='ID' and @currecordid='{latest_id}']", f"Reopen Record ID {latest_id}")
            time.sleep(2)
            self.base.verify_form_page()
            time.sleep(3)

        # 🔹 Positive value check
        print(f"➡️ ✅  Trying positive value: {positive_value}")
        self.base.enter_text(self.s1_textbox_input, positive_value, "S1 TextBox")
        self.base.click(self.SUBMIT_BTN, "Submit Form")
        self.scroll_to_element("//span[contains(.,'Current Status')]")
        time.sleep(2)

        latest_id, current_status = self.get_latest_record_status()
        if current_status == "S1(EQUAL TO)":
            print(f"💚 🏆 Equal To Rule Passed → Record moved to {current_status}🏆 ✨")
        else:
            error_message = f"❌ Equal To Rule Failed → Record stayed in {current_status} instead of S1(EQUAL TO)"
            print(error_message)  # print to console
            raise AssertionError(error_message)