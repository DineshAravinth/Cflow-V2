from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from BaseFiles.Basehelpers import BaseHelpers
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

class FormCreation(BaseHelpers):
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
    Table_section_drop_field_here = "(//div[contains(.,' Drop field here.. ')])[12]"
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

    # Publish button
    Publish_button = "//button[contains(.,'Publish')]"

    # Go to workflow
    go_to_workflow_button = "//button[contains(.,'Go to Workflow')]"

    # ---------- Section Flow ----------
    def add_section_dragdrop(self):
        sleep(3)
        self.drag_and_drop_element(self.add_section, self.drop_section, "Section")
        sleep(3)
        try:
            self.wait.until(
                lambda d: d.find_element(By.XPATH, self.enter_section_name).is_displayed()
            )
            print("✅ Section modal opened successfully.")
        except TimeoutException:
            raise AssertionError("❌ Section modal did not open after drag-drop")

    def section_name(self, section_name="Main Section"):
        self.enter_text(self.enter_section_name, section_name, "Section Name")

    def save_section(self):
        try:
            save_btn = self.wait.until(lambda d: d.find_element(By.XPATH, self.button_save_section))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            try:
                save_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", save_btn)
            print("✅ Section saved successfully")
        except TimeoutException:
            raise AssertionError("❌ Save Section button not clickable")

    # ---------- Field Methods ----------
    def add_textbox(self):
        self.drag_and_drop_element(self.textbox_field, self.drop_field_here, "TextBox")
        self._save("TextBox")

    def add_email(self):
        self.drag_and_drop_element(self.email_field, self.drop_field_here, "Email")
        self._save("Email")

    def add_checkbox(self):
        self.drag_and_drop_element(self.checkbox_field, self.drop_field_here, "CheckBox")
        self._save("CheckBox")

    def add_decimal(self):
        self.drag_and_drop_element(self.decimal_field, self.drop_field_here, "Decimal")
        self._save("Decimal")

    def add_number(self):
        self.drag_and_drop_element(self.number_field, self.drop_field_here, "Number")
        self._save("Number")

    def add_textarea(self):
        self.drag_and_drop_element(self.textarea_field, self.drop_field_here, "TextArea")
        self._save("TextArea")

    def add_currency(self):
        self.drag_and_drop_element(self.currency_field, self.drop_field_here, "Currency")
        self._save("Currency")

    def add_date(self):
        self.drag_and_drop_element(self.date_field, self.drop_field_here, "Date")
        self._save("Date")

    def add_time(self):
        self.drag_and_drop_element(self.time_field, self.drop_field_here, "Time")
        self._save("Time")

    def add_url(self):
        self.drag_and_drop_element(self.url_field, self.drop_field_here, "URL")
        self._save("URL")

    def add_file_uploader(self):
        self.drag_and_drop_element(self.file_uploader_field, self.drop_field_here, "FileUploader")
        self._save("FileUploader")

    def add_radio_button(self, values=["A", "B", "C"]):
        self.drag_and_drop_element(self.radio_button_field, self.drop_field_here, "RadioButton")
        self.click(self.tab_controls_radio_button, "RadioButton Tab")
        self._add_values(values, "RadioButton")

    def add_ms_dropdown(self, values=["A", "B", "C"]):
        self.drag_and_drop_element(self.ms_dropdown_field, self.drop_field_here, "MS Dropdown")
        self.click(self.tab_controls_MS_Dropdown, "MS Dropdown Tab")
        self._add_values(values, "MS Dropdown")

    def add_checkbox_list(self, values=["A", "B", "C"]):
        self.drag_and_drop_element(self.checkbox_list_field, self.drop_field_here, "CheckboxList")
        self.click(self.tab_controls_checkbox_list, "CheckboxList Tab")
        self._add_values(values, "CheckboxList")

    def add_ip_address(self):
        self.drag_and_drop_element(self.IP_Address_field, self.drop_field_here, "IPAddress")
        self._save("IPAddress")

    def add_signature(self):
        self.drag_and_drop_element(self.Signature_field, self.drop_field_here, "Signature")
        self._save("Signature")

    def add_identity(self):
        self.drag_and_drop_element(self.identity_field, self.drop_field_here, "Identity")
        self._save("Identity")

    def add_html_editor(self):
        self.drag_and_drop_element(self.html_editor_field, self.drop_field_here, "HTMLEditor")
        self._save("HTMLEditor")

    def add_terms_and_conditions(self):
        self.drag_and_drop_element(self.terms_and_conditons_field, self.drop_field_here, "TermsAndConditions")
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


    # ---------- Internal Helpers ----------
    def _save(self, label):
        try:
            save_btn = self.wait.until(lambda d: d.find_element(By.XPATH, self.button_save_field))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            try:
                save_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", save_btn)
            print(f"✅ {label} field saved successfully")
        except TimeoutException:
            raise AssertionError(f"❌ Save {label} button not clickable")

    def _add_values(self, values, label):
        for idx, val in enumerate(values):
            self.wait.until(lambda d: d.find_elements(By.XPATH, self.enter_values))
            all_inputs = self.driver.find_elements(By.XPATH, self.enter_values)
            last_input = all_inputs[-1]
            self.enter_text(self.enter_values, val, f"{label} Value")
            if idx != len(values) - 1:
                self.click(self.button_add_new, "Add New Value")
                sleep(0.3)

    # ---------- Table Section ----------
    def add_table_section_dragdrop(self):
        sleep(3)
        self.drag_and_drop_element(self.Table_add_section, self.Table_drop_section, "Table Section")
        sleep(3)
        try:
            self.wait.until(lambda d: d.find_element(By.XPATH, self.Table_enter_section_name).is_displayed())
            print("✅ Table Section modal opened successfully.")
        except TimeoutException:
            raise AssertionError("❌ Table Section modal did not open after drag-drop")

    def table_section_name(self, section_name="Table Section"):
        self.enter_text(self.Table_enter_section_name, section_name, "Table Section Name")

    def save_table_section(self):
        try:
            save_btn = self.wait.until(lambda d: d.find_element(By.XPATH, self.Table_button_save_section))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            try:
                save_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", save_btn)
            print("✅ Table Section saved successfully")
        except TimeoutException:
            raise AssertionError("❌ Table Section save button not clickable")

    # ---------- Publish & Navigation ----------
    def click_publish(self):
        self.click(self.Publish_button, "Publish Button")

    def click_go_to_workflow(self):
        self.click(self.go_to_workflow_button, "Go to Workflow Button")
