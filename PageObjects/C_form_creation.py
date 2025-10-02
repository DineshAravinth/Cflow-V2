from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class FormCreation:
    # ---------- Section Locators - Main section ----------
    add_section = "//p[normalize-space()='Section']"
    drop_section = "//div[@class='wid-100 drop-item ng-star-inserted']//div[contains(text(),'Drop section here')]"
    enter_section_name = "//input[@title='sectionName' or @placeholder='Enter your section name']"
    button_save_section = "//button[contains(.,'Save')]"

    # ---------- Section Locators - Table section ----------
    Table_add_section = "//p[normalize-space()='Table']"
    Table_drop_section = "//div[@class='wid-100 drop-item ng-star-inserted']//div[contains(text(),'Drop section here')]"
    Table_enter_section_name = "//input[@title='sectionName' or @placeholder='Enter your section name']"
    Table_button_save_section = "//button[contains(.,'Save')]"

    # ---------- Generic Drop Target ----------
    drop_field_here = "(//div[contains(.,' Drop field here.. ')])[8]"
    Table_section_drop_field_here = "//div[@class='cdk-drop-list form-row scroll-table ng-star-inserted']//div[contains(text(),'Drop field here..')]"
    button_save_field = "//button[contains(.,'Save')]"

    # ---------- Field Locators ----------
    textbox_field = "//p[contains(.,'TextBox')]"
    email_field = "//p[contains(.,'Email')]"
    checkbox_field = "(//p[contains(.,'Checkbox')])[1]"
    dropdown_field = "(//p[contains(.,'Dropdown')])[1]"
    IP_Address_field = "//p[contains(.,'IP Address')]"
    Signature_field = "//p[contains(.,'Signature')]"

    decimal_field = "//p[contains(.,'Decimal')]"
    number_field = "//p[contains(.,'Number')]"
    textarea_field = "//p[contains(.,'Text Area')]"
    currency_field = "//p[contains(.,'Currency')]"
    date_field = "(//p[contains(.,'Date')])[2]"
    time_field = "(//p[contains(.,'Time')])[2]"
    url_field = "//p[contains(.,'URL')]"
    file_uploader_field = "//p[contains(.,'File Uploader')]"
    radio_button_field = "//p[contains(.,'Radio Button')]"
    ms_dropdown_field = "//p[contains(.,'MS Dropdown')]"
    checkbox_list_field = "//p[contains(.,'Checkbox List')]"
    identity_field = "//p[contains(.,'Identity')]"
    html_editor_field = "//p[contains(.,'HTML Editor')]"
    terms_and_conditons_field = "//p[contains(.,'Terms And Conditions')]"

    # Dropdown config
    tab_controls_dropdown = "//a[contains(.,' Controls')]"
    tab_controls_radio_button = "//a[contains(.,' Controls')]"
    tab_controls_MS_Dropdown = "//a[contains(.,' Controls')]"
    tab_controls_checkbox_list = "//a[contains(.,' Controls')]"

    button_add_new = "//button[contains(.,'+ Add New')]"
    enter_values = "//input[@title='validvalues']"

    #Publish button
    Publish_button = "//button[contains(.,'Publish')]"

    #Go to workflow
    go_to_workflow_button = "//button[contains(.,'Go to Workflow')]"


    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Generic Helpers ----------
    def click(self, xpath, description="element"):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
            )
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)
            print(f"✅ Clicked: {description}")
        except TimeoutException:
            raise AssertionError(f"❌ Timeout: {description} not clickable")
        except NoSuchElementException:
            raise AssertionError(f"❌ Not Found: {description}")

    def enter_text(self, xpath, text, description="textbox"):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
            )
            element.clear()
            element.send_keys(text)
            print(f"✅ Entered '{text}' into {description}")
        except TimeoutException:
            raise AssertionError(f"❌ Timeout: {description} not found")
        except NoSuchElementException:
            raise AssertionError(f"❌ Not Found: {description}")

    def drag_and_drop(self, source_xpath, target_xpath=None, label="Element"):
        sleep(3)
        source = self.wait.until(EC.presence_of_element_located((By.XPATH, source_xpath)))
        target = self.wait.until(
            EC.presence_of_element_located((By.XPATH, target_xpath or self.drop_field_here))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", target
        )
        try:
            actions = ActionChains(self.driver)
            (
                actions.click_and_hold(source)
                .pause(0.5)
                .move_to_element(target)
                .pause(0.3)
                .move_by_offset(10, 10)
                .pause(0.2)
                .release()
                .perform()
            )
            print(f"✅ {label} drag-drop simulated step by step.")
        except Exception as e:
            raise AssertionError(f"⚠️ Drag-drop failed for {label}: {e}")

    def drag_and_drop_to_new_row(self, source_xpath, label="Element"):
        sleep(2)
        placeholders = self.driver.find_elements(By.XPATH, "//div[contains(text(),'Drop field here..')]")
        if not placeholders:
            raise AssertionError("❌ No 'Drop field here..' placeholders found.")
        target = placeholders[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", target
        )
        source = self.wait.until(EC.presence_of_element_located((By.XPATH, source_xpath)))
        try:
            actions = ActionChains(self.driver)
            (
                actions.click_and_hold(source)
                .pause(0.5)
                .move_to_element(target)
                .pause(0.3)
                .move_by_offset(10, 10)
                .pause(0.2)
                .release()
                .perform()
            )
            print(f"✅ {label} dropped into NEW row.")
        except Exception as e:
            raise AssertionError(f"⚠️ Failed to drop {label} into new row: {e}")

    # ---------- Section Flow ----------
    def add_section_dragdrop(self):
        sleep(3)
        self.drag_and_drop(self.add_section, self.drop_section, "Section")
        sleep(3)
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'modal-content')]"))
            )
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.enter_section_name)))
            print("✅ Section modal opened successfully.")
        except TimeoutException:
            raise AssertionError("❌ Section modal did not open after drag-drop")

    def section_name(self, section_name="Main Section"):
        self.enter_text(self.enter_section_name, section_name, "Section Name")

    def save_section(self):
        save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_save_section)))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", save_btn
        )
        try:
            save_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_btn)
        print("✅ Section saved successfully")

    # ---------- Field Methods with Explicit Waits ----------
    def add_textbox(self):
        self.drag_and_drop(self.textbox_field, label="TextBox")
        self._save("TextBox")

    def add_email(self):
        self.drag_and_drop(self.email_field, label="Email")
        self._save("Email")

    def add_checkbox(self):
        self.drag_and_drop(self.checkbox_field, label="CheckBox")
        self._save("CheckBox")

    def add_decimal(self):
        self.drag_and_drop(self.decimal_field, label="Decimal")
        self._save("Decimal")

    def add_number(self):
        self.drag_and_drop(self.number_field, label="Number")
        self._save("Number")

    def add_textarea(self):
        self.drag_and_drop(self.textarea_field, label="TextArea")
        self._save("TextArea")

    def add_currency(self):
        self.drag_and_drop(self.currency_field, label="Currency")
        self._save("Currency")

    def add_date(self):
        self.drag_and_drop(self.date_field, label="Date")
        self._save("Date")

    def add_time(self):
        self.drag_and_drop(self.time_field, label="Time")
        self._save("Time")

    def add_url(self):
        self.drag_and_drop_to_new_row(self.url_field, label="URL")
        self._save("URL")

    def add_file_uploader(self):
        self.drag_and_drop(self.file_uploader_field, label="FileUploader")
        self._save("FileUploader")

    def add_radio_button(self, values=["A", "B", "C"]):
        """
        Drag-drop a radio button field and add multiple options reliably.
        Uses the same logic as dropdown: open the tab, type values, and save.
        """
        # 1️⃣ Drag and drop the radio button field
        self.drag_and_drop(self.radio_button_field, label="RadioButton")

        # 2️⃣ Click the tab to show option inputs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_radio_button)))
        self.click(self.tab_controls_radio_button, "RadioButton Tab")

        # 3️⃣ Loop through all options to add them
        for idx, val in enumerate(values):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))

            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]

            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)

            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Added radio option: {val}")

            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Option")
                sleep(0.3)

        # 4️⃣ Save the radio button field
        self._save("RadioButton")

    def add_ms_dropdown(self, values=["A", "B", "C"]):
        """
        Drag-drop a Multi-Select Dropdown field and add multiple values reliably.
        Handles dynamic input fields and ensures each value is typed into the correct box.
        """
        # 1️⃣ Drag and drop the MS Dropdown field
        self.drag_and_drop(self.ms_dropdown_field, label="MS Dropdown")

        # 2️⃣ Click the tab to show value inputs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_MS_Dropdown)))
        self.click(self.tab_controls_MS_Dropdown, "MS Dropdown Tab")

        # 3️⃣ Loop through all values to add them
        for idx, val in enumerate(values):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))

            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]

            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)

            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Entered MS Dropdown value: {val}")

            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Value")
                sleep(0.3)

        # 4️⃣ Save the MS Dropdown field
        self._save("MS Dropdown")

    def add_checkbox_list(self, values=["A", "B", "C"]):
        """
        Drag-drop a Checkbox List field and add multiple values reliably.
        Uses the same flow as dropdown, radio, and MS dropdown.
        """
        # 1️⃣ Drag and drop the checkbox list field
        self.drag_and_drop_to_new_row(self.checkbox_list_field, label="CheckboxList")

        # 2️⃣ Click the tab to show value inputs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_checkbox_list)))
        self.click(self.tab_controls_checkbox_list, "CheckboxList Tab")

        # 3️⃣ Loop through all values to add them
        for idx, val in enumerate(values):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))

            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]

            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)

            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Added checkbox option: {val}")

            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Checkbox Option")
                sleep(0.3)

        # 4️⃣ Save the checkbox list field
        self._save("CheckboxList")

    def add_ip_address(self):
        self.drag_and_drop(self.IP_Address_field, label="IPAddress")
        self._save("IPAddress")

    def add_signature(self):
        self.drag_and_drop_to_new_row(self.Signature_field, label="Signature")
        self._save("Signature")

    def add_identity(self):
        self.drag_and_drop(self.identity_field, label="Identity")
        self._save("Identity")

    def add_html_editor(self):
        self.drag_and_drop_to_new_row(self.html_editor_field, label="HTMLEditor")
        self._save("HTMLEditor")

    def add_terms_and_conditions(self):
        self.drag_and_drop_to_new_row(self.terms_and_conditons_field, label="TermsAndConditions")
        self._save("TermsAndConditions")

    def add_dropdown(self, values=["A", "B", "C"]):
        """
        Drag-drop a dropdown field and add multiple values reliably.
        Handles dynamic input fields and ensures each value is typed into the correct box.
        """

        # 1️⃣ Drag and drop the dropdown field
        self.drag_and_drop(self.dropdown_field, label="Dropdown")

        # 2️⃣ Click the tab to show value inputs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_dropdown)))
        self.click(self.tab_controls_dropdown, "Dropdown Tab")

        # 3️⃣ Loop through all values to add them
        for idx, val in enumerate(values):
            # Wait until at least one input is present
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))

            # Get all current input fields and select the last one (newly created)
            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]

            # Wait until the last input is visible and interactable
            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))

            # Scroll into view before typing
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)

            # Enter the value
            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Entered value: {val}")

            # Click "+ Add New" only if there’s a next value
            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Value")
                # Small pause to allow the next input to render
                sleep(0.3)

        # 4️⃣ Save the dropdown field
        self._save("Dropdown")

    # ---------- Internal Save ----------
    def _save(self, label):
        try:
            save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_save_field)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", save_btn
            )
            try:
                save_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", save_btn)
            print(f"✅ {label} field saved successfully")
        except TimeoutException:
            raise AssertionError(f"❌ Timeout: Save {label} button not clickable")


    # ---------- Table Section Methods ----------

    def add_table_section_dragdrop(self):
        sleep(3)
        self.drag_and_drop(self.Table_add_section, self.Table_drop_section, "Table Section")
        sleep(3)
        try:
            self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'modal-content')]"))
            )
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.Table_enter_section_name)))
            print("✅ Table Section modal opened successfully.")
        except TimeoutException:
            raise AssertionError("❌ Table Section modal did not open after drag-drop")

    def table_section_name(self, section_name="Table Section"):
        self.enter_text(self.Table_enter_section_name, section_name, "Table Section Name")

    def save_table_section(self):
        save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.Table_button_save_section)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
        try:
            save_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", save_btn)
        print("✅ Table Section saved successfully")

    def drag_and_drop_table_field(self, source_xpath, label="Table Field"):
        """
        Drag-drop specifically for fields inside the Table Section.
        Uses the dedicated table section drop area.
        """
        sleep(3)
        source = self.wait.until(EC.presence_of_element_located((By.XPATH, source_xpath)))
        target = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.Table_section_drop_field_here))
        )
        try:
            actions = ActionChains(self.driver)
            (
                actions.click_and_hold(source)
                .pause(0.5)
                .move_to_element(target)
                .pause(0.3)
                .move_by_offset(10, 10)
                .pause(0.2)
                .release()
                .perform()
            )
            print(f"✅ {label} drag-drop into Table Section simulated step by step.")
        except Exception as e:
            raise AssertionError(f"⚠️ Drag-drop into Table Section failed for {label}: {e}")

    def add_textbox_table(self):
        """
        Add a TextBox field inside the Table Section.
        Uses drag_and_drop_table_field to drop into the table-specific area.
        """
        self.drag_and_drop_table_field(self.textbox_field, label="TextBox (Table)")
        self._save("TextBox (Table)")

    def add_email_table(self):
        self.drag_and_drop_table_field(self.email_field, label="Email (Table)")
        self._save("Email (Table)")

    def add_checkbox_table(self):
        self.drag_and_drop_table_field(self.checkbox_field, label="CheckBox (Table)")
        self._save("CheckBox (Table)")

    def add_decimal_table(self):
        self.drag_and_drop_table_field(self.decimal_field, label="Decimal (Table)")
        self._save("Decimal (Table)")

    def add_number_table(self):
        self.drag_and_drop_table_field(self.number_field, label="Number (Table)")
        self._save("Number (Table)")

    def add_textarea_table(self):
        self.drag_and_drop_table_field(self.textarea_field, label="TextArea (Table)")
        self._save("TextArea (Table)")

    def add_currency_table(self):
        self.drag_and_drop_table_field(self.currency_field, label="Currency (Table)")
        self._save("Currency (Table)")

    def add_date_table(self):
        self.drag_and_drop_table_field(self.date_field, label="Date (Table)")
        self._save("Date (Table)")

    def add_time_table(self):
        self.drag_and_drop_table_field(self.time_field, label="Time (Table)")
        self._save("Time (Table)")

    def add_url_table(self):
        self.drag_and_drop_table_field(self.url_field, label="URL (Table)")
        self._save("URL (Table)")

    def add_file_uploader_table(self):
        self.drag_and_drop_table_field(self.file_uploader_field, label="FileUploader (Table)")
        self._save("FileUploader (Table)")

    def add_ms_dropdown_table(self, values=["A", "B", "C"]):
        self.drag_and_drop_table_field(self.ms_dropdown_field, label="MS Dropdown (Table)")

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_MS_Dropdown)))
        self.click(self.tab_controls_MS_Dropdown, "MS Dropdown Tab (Table)")

        for idx, val in enumerate(values):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))
            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]
            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)
            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Entered MS Dropdown value (Table): {val}")

            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Value (Table)")
                sleep(0.3)

        self._save("MS Dropdown (Table)")

    def add_ip_address_table(self):
        self.drag_and_drop_table_field(self.IP_Address_field, label="IPAddress (Table)")
        self._save("IPAddress (Table)")

    def add_signature_table(self):
        self.drag_and_drop_table_field(self.Signature_field, label="Signature (Table)")
        self._save("Signature (Table)")

    def add_dropdown_table(self, values=["A", "B", "C"]):
        self.drag_and_drop_table_field(self.dropdown_field, label="Dropdown (Table)")

        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.tab_controls_dropdown)))
        self.click(self.tab_controls_dropdown, "Dropdown Tab (Table)")

        for idx, val in enumerate(values):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.enter_values)))
            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]
            self.wait.until(EC.visibility_of(last_input))
            self.wait.until(EC.element_to_be_clickable(last_input))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_input)
            last_input.clear()
            last_input.send_keys(val)
            print(f"➕ Entered Dropdown value (Table): {val}")

            if idx != len(values) - 1:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_add_new)))
                self.click(self.button_add_new, "Add New Value (Table)")
                sleep(0.3)

        self._save("Dropdown (Table)")


    # ---------- Publish & Navigation ----------
    def click_publish(self):
        self.click(self.Publish_button, "Publish Button")

    def click_go_to_workflow(self):
        self.click(self.go_to_workflow_button, "Go to Workflow Button")
