import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseFiles.Basehelpers import BaseHelpers

class rules_condition_verification:

    select_workflow = "//a[contains(.,' AUTOMATION PAGE - RULES ENGINE CONDITIONS ')]"

    # S1
    s1_textbox_label = "//label[contains(.,'S1 TextBox ')]"
    s1_textbox_input = "//input[@id='S1_TextBox']"

    # S2
    s2_textbox_label = "//label[contains(.,'S2 TextBox ')]"
    s2_textbox_input = "//input[@id='S2_TextBox']"

    # S3
    s3_textbox_int_label = "//label[contains(.,'S3 TextBox INT ')]"
    s3_textbox_int_input = "//input[@id='S3_TextBox_INT']"

    # S4
    s4_textbox_int_label = "//label[contains(.,'S4 TextBox INT ')]"
    s4_textbox_int_input = "//input[@id='S4_TextBox_INT']"

    # S5
    s5_textbox_int_label = "//label[contains(.,'S5 TextBox INT ')]"
    s5_textbox_int_input = "//input[@id='S5_TextBox_INT']"

    # S6
    s6_textbox_int_label = "//label[contains(.,'S6 TextBox INT ')]"
    s6_textbox_int_input = "//input[@id='S6_TextBox_INT']"

    # S7
    s7_textbox_label = "//label[contains(.,'S7 TextBox ')]"
    s7_textbox_input = "//input[@id='S7_TextBox']"

    # S8
    s8_textbox_label = "//label[contains(.,'S8 TextBox ')]"
    s8_textbox_input = "//input[@id='S8_TextBox']"

    # S9
    s9_textbox_label = "//label[contains(.,'S9 TextBox ')]"
    s9_textbox_input = "//input[@id='S9_TextBox']"

    SUBMIT_BTN = "//button[contains(.,'Submit Form')]"
    ADD_NEW_RECORD_BTN = "//a[contains(.,'Add New')]"

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
    def verify_text_rule(self, textbox_input_locator, rule_name, negative_values=None, positive_values=None,
                         positive_value_caps=None, equal_to_value=None):
        """
        Generic text rule verification for S1 (EQUAL TO) and S2 (NOT EQUAL TO).

        Args:
            textbox_input_locator (str): XPath of the input textbox.
            rule_name (str): Stage name (e.g., S1, S2)
            negative_values (list): Values that should stay in Initiator
            positive_values (list): Values that should move to the stage
            positive_value_caps (str): Optional, for S1: uppercase positive value
            equal_to_value (str): Optional, for S1: value to check equality
        """
        if negative_values is None:
            negative_values = []
        if positive_values is None:
            positive_values = []

        print(f"⚠️ {rule_name} Negative values to test: {', '.join(negative_values)}")
        print(f"⚠️ {rule_name} Positive values to test: {', '.join(positive_values)}")
        if positive_value_caps:
            print(f"⚠️ {rule_name} CAPS Positive value to test: {positive_value_caps}")

        # ---------------- Negative values ----------------
        for neg_val in negative_values:
            print(f"➡️ Testing value: '{neg_val}' (Negative)")
            self.base.enter_text(textbox_input_locator, neg_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(2)
            latest_id, current_status = self.get_latest_record_status()

            if rule_name == "S1" and equal_to_value and neg_val == equal_to_value:
                expected_status = f"{rule_name}(EQUAL TO)"
            elif rule_name == "S2":
                expected_status = "Initiator"
            else:
                expected_status = "Initiator"

            if current_status != "Initiator":
                raise AssertionError(f"❌ Negative value '{neg_val}' wrongly moved to {current_status}")
            print(f"💚  ✅ Negative value '{neg_val}' correctly stayed in Initiator stage")

            # Reopen same record for next negative test
            self.base.click(f"//td[@data-title='ID' and @currecordid='{latest_id}']",
                            f"Reopen Record ID {latest_id}")
            time.sleep(2)
            self.base.verify_form_page()
            time.sleep(2)

        # ---------------- Positive values ----------------
        for idx, pos_val in enumerate(positive_values):
            print(f"➡️ Testing value: '{pos_val}' (Positive)")

            # First positive value uses current record; subsequent values create new record
            if idx > 0:
                print("➡️ Creating new record for next positive value...")
                self.base.click(self.ADD_NEW_RECORD_BTN, "Add New Record")
                time.sleep(2)

            self.base.enter_text(textbox_input_locator, pos_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(2)
            latest_id, current_status = self.get_latest_record_status()

            # Determine expected status
            if rule_name == "S1":
                expected_status = f"{rule_name}(EQUAL TO)"
            elif rule_name == "S2":
                expected_status = f"{rule_name}(NOT EQUAL TO)"
            else:
                expected_status = "UNKNOWN"

            if current_status == expected_status:
                print(f"💚  ✅ Positive value '{pos_val}' correctly moved to {current_status}")
            else:
                error_message = f"❌ Positive value '{pos_val}' failed → stayed in {current_status} instead of {expected_status}"
                print(error_message)
                raise AssertionError(error_message)

        # ---------------- CAPS Positive for S1 ----------------
        if rule_name == "S1" and positive_value_caps:
            print(f"➡️ Testing value (CAPS): '{positive_value_caps}'")
            self.base.click(self.ADD_NEW_RECORD_BTN, "Add New Record")
            time.sleep(2)
            self.base.enter_text(textbox_input_locator, positive_value_caps, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(2)
            latest_id, current_status = self.get_latest_record_status()
            expected_status = f"{rule_name}(EQUAL TO)"
            if current_status == expected_status:
                print(f"💚  ✅ CAPS Positive value '{positive_value_caps}' correctly moved to {current_status}")
            else:
                error_message = f"❌ CAPS Positive value '{positive_value_caps}' failed → stayed in {current_status} instead of {expected_status}"
                print(error_message)
                raise AssertionError(error_message)

    def verify_numeric_rule(self, textbox_input_locator, rule_name, comparison, negative_values=None,
                            positive_values=None):
        """
        Generic numeric rule verification for S3, S4, S5, S6 stages.

        Args:
            textbox_input_locator (str): XPath of the input textbox.
            rule_name (str): Stage name (e.g., S3, S4, S5, S6)
            comparison (str): Comparison type: "<", "<=", ">", ">="
            negative_values (list): Values that should stay in Initiator
            positive_values (list): Values that should move to the stage
        """
        if negative_values is None:
            negative_values = []

        if positive_values is None:
            positive_values = []

        print(f"⚠️ {rule_name} Negative values to test: {', '.join(map(str, negative_values))}")
        print(f"⚠️ {rule_name} Positive values to test: {', '.join(map(str, positive_values))}")

        # 🔹 Negative values
        for neg_val in negative_values:
            print(f"➡️ Testing negative value: {neg_val}")
            self.base.enter_text(textbox_input_locator, str(neg_val), f"{rule_name} TextBox INT")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")

            latest_id, current_status = self.get_latest_record_status()
            if current_status != "Initiator":
                raise AssertionError(f"❌ {rule_name} Negative value '{neg_val}' wrongly moved to {current_status}")
            print(f"✅ {rule_name} Negative value '{neg_val}' correctly stayed in Initiator stage")

            # Reopen record
            self.base.click(f"//td[@data-title='ID' and @currecordid='{latest_id}']", f"Reopen Record ID {latest_id}")
            time.sleep(2)
            self.base.verify_form_page()
            time.sleep(2)

        # 🔹 Positive values
        for idx, pos_val in enumerate(positive_values):
            print(f"➡️ Testing positive value: {pos_val}")

            # First positive value uses current record; subsequent values create new record
            if idx > 0:
                self.base.click(self.ADD_NEW_RECORD_BTN, "Add New Record")
                time.sleep(2)

            self.base.enter_text(textbox_input_locator, str(pos_val), f"{rule_name} TextBox INT")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(3)
            self.scroll_to_element("//span[contains(.,'Current Status')]")

            latest_id, current_status = self.get_latest_record_status()
            expected_status = f"{rule_name}({self._comparison_to_text(comparison)})"
            if current_status == expected_status:
                print(f"💚  ✅ Positive value '{pos_val}' correctly moved to {current_status}")
            else:
                error_message = f"❌ {rule_name} Positive value '{pos_val}' failed → Record stayed in {current_status} instead of {expected_status}"
                print(error_message)
                raise AssertionError(error_message)

    # Helper to convert comparison symbols to text for status
    def _comparison_to_text(self, comparison):
        mapping = {
            "<": "LESS THAN",
            "<=": "LESS THAN OR EQUAL TO",
            ">": "GREATER THAN",
            ">=": "GREATER THAN OR EQUAL TO"
        }
        return mapping.get(comparison, "UNKNOWN")

    def verify_contains_rule(self,textbox_input_locator,rule_name,match_values=None,negative_values=None):
        """
        Generic text rule verification for S7 (CONTAINS) and S8 (DOES NOT CONTAIN).

        Args:
            textbox_input_locator (str): XPath of the input textbox.
            rule_name (str): Stage name (e.g., S7, S8)
            match_values (list): Values that should move to the stage
            negative_values (list): Values that should stay in Initiator
        """
        if match_values is None:
            match_values = []
        if negative_values is None:
            negative_values = []

        print(f"⚠️ {rule_name} Negative values to test: {', '.join(negative_values)}")
        print(f"⚠️ {rule_name} Positive values to test: {', '.join(match_values)}")

        # 🔹 Negative values
        for neg_val in negative_values:
            print(f"➡️ Testing negative value: '{neg_val}' (Negative)")
            self.base.enter_text(textbox_input_locator, neg_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(2)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            latest_id, current_status = self.get_latest_record_status()

            if current_status != "Initiator":
                raise AssertionError(f"❌ {rule_name} Negative value '{neg_val}' wrongly moved to {current_status}")
            print(f"💚  ✅  Negative value '{neg_val}' correctly stayed in Initiator stage")

            # Reopen record for next negative test
            self.base.click(f"//td[@data-title='ID' and @currecordid='{latest_id}']", f"Reopen Record ID {latest_id}")
            time.sleep(2)
            self.base.verify_form_page()
            time.sleep(2)

        # 🔹 Positive values
        for idx, pos_val in enumerate(match_values):
            print(f"➡️ Testing positive value: '{pos_val}' (Positive)")

            if idx > 0:
                print("➡️ Creating new record for next positive value...")
                self.base.click(self.ADD_NEW_RECORD_BTN, "Add New Record")
                time.sleep(2)

            self.base.enter_text(textbox_input_locator, pos_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(2)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            latest_id, current_status = self.get_latest_record_status()

            # Determine expected status
            expected_status = f"{rule_name}({'CONTAINS' if rule_name == 'S7' else 'DOES NOT CONTAINS'})"
            if current_status == expected_status:
                print(f"💚  ✅  Positive value '{pos_val}' correctly moved to {current_status}")
            else:
                error_message = f"❌ Positive value '{pos_val}' failed → stayed in {current_status} instead of {expected_status}"
                print(error_message)
                raise AssertionError(error_message)

    def verify_partial_match_rule(self, textbox_input_locator, rule_name, partial_value, negative_values=None,
                                  positive_values=None):
        """
        Verify Partial Match rule for a stage (S9):
        - Negative values should stay in Initiator
        - Positive values containing the partial_value should move to the stage
        """
        if negative_values is None:
            negative_values = ["random1", "random2", "demo", "  "]
        if positive_values is None:
            positive_values = ["Dinesh", "ARAVINTHDINESHARAVINTH", "dinesh123"]

        expected_status = f"{rule_name}(PARTIAL MATCH)"

        print(f"⚠️ {rule_name} Negative values to test: {', '.join(negative_values)}")
        print(f"⚠️ {rule_name} Positive values to test: {', '.join(positive_values)}")
        print(f"⚠️ {rule_name} Partial match target: '{partial_value}'")

        # 🔹 Negative values
        for neg_val in negative_values:
            print(f"➡️  Testing negative value: '{neg_val}'")
            self.base.enter_text(textbox_input_locator, neg_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(2)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(1)

            latest_id, current_status = self.get_latest_record_status()
            if current_status != "Initiator":
                raise AssertionError(f"❌ Negative value '{neg_val}' wrongly moved to {current_status}")
            print(f"💚  ✅  Negative value '{neg_val}' correctly stayed in Initiator stage")

            # Reopen same record for next negative test
            self.base.click(f"//td[@data-title='ID' and @currecordid='{latest_id}']", f"Reopen Record ID {latest_id}")
            time.sleep(1)
            self.base.verify_form_page()
            time.sleep(1)

        # 🔹 Positive values
        for idx, pos_val in enumerate(positive_values):
            print(f"➡️  Testing positive value: '{pos_val}'")
            if idx > 0:
                print("➡️  Creating new record for next positive value...")
                self.base.click(self.ADD_NEW_RECORD_BTN, "Add New Record")
                time.sleep(1)

            self.base.enter_text(textbox_input_locator, pos_val, f"{rule_name} TextBox")
            self.base.click(self.SUBMIT_BTN, "Submit Form")
            time.sleep(2)
            self.scroll_to_element("//span[contains(.,'Current Status')]")
            time.sleep(1)

            latest_id, current_status = self.get_latest_record_status()
            # Case-insensitive partial match check
            if partial_value.lower() in pos_val.lower():
                if current_status == expected_status:
                    print(f"💚  ✅  Positive value '{pos_val}' correctly moved to {current_status}")
                else:
                    print(f"⚠️  Positive value '{pos_val}' contains '{partial_value}' but status is {current_status}")
            else:
                error_message = f"❌ Positive value '{pos_val}' failed → does not contain '{partial_value}'"
                print(error_message)
                raise AssertionError(error_message)


