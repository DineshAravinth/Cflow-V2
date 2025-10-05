from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseFiles.Basehelpers import BaseHelpers
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException


class lookup_creation:

    side_nav_lookups = "(//span[contains(.,'Lookups')])[2]"
    select_lookup = "//p[contains(.,'Lookup Test Automation--04-10-2025-(13:46) to Workflow')]"

    # Lookup creation
    create_lookup_button = "//button[contains(.,'Create Lookup')]"
    enter_new_lookup_name = "//input[@placeholder='Enter Name']"
    create_lookupname_button = "(//button[contains(.,'Create')])[2]"
    publish_lookup_button = "//button[contains(.,'Publish')]"

    # Field locators
    add_field_button = "//button[contains(.,'Add Field')]"
    add_field_button_lookup = "//a[.//span[contains(.,'Add Field')]]"
    display_name_label = "//label[contains(.,'Display Name ')]"
    enter_display_name_input = "//input[@formcontrolname='fieldDispName']"
    enter_valid_values_input = "//input[@placeholder='Valid Values']"
    save_button = "//button[contains(.,'Save')]"
    field_type_label = "//label[contains(.,'Field Type')]"

    add_row_button ="//button[contains(.,'Add Row')]"



    textbox_label = "(//label[contains(.,'TextBox')])[1]"
    textbox_input = "//input[@id='TextBox']"

    email_label = "//label[contains(.,'Email')]"
    email_input = "//input[@id='Email']"

    checkbox_label = "(//label[contains(.,'CheckBox')])[1]"
    checkbox_input = "//input[@id='CheckBox']"

    decimal_label = "(//label[contains(.,'Decimal')])[1]"
    decimal_input = "//input[@id='Decimal']"

    dropdown_label = "(//label[contains(.,'DropDown List')])[1]"
    dropdown_input = f"{dropdown_label}/following::div[@class='ng-input']//input[@role='combobox']"

    ms_dropdown_label = "//label[contains(.,'MS DropDown List')]"
    ms_dropdown_input = f"{ms_dropdown_label}/following::div[contains(@class,'ng-input')]//input[@role='combobox']"

    ip_address_label = "//label[contains(.,'IP Address')]"
    ip_address_input = "//input[@id='IP_Address']"

    radio_label_template = "(//label[contains(.,'{label_text}')])[1]"
    radio_input_template = "//input[@id='{input_id}']"

    url_label = "//label[contains(.,'URL')]"
    url_input = "//input[@id='URL']"

    numbers_label = "//label[contains(.,'Number')]"
    numbers_input = "//input[@id='Number']"

    text_area_label = "//label[contains(.,'TextBox MultiLine')]"
    text_area_input = "//textarea[@id='TextBox_MultiLine']"

    currency_label = "//label[contains(.,'Currency')]"
    currency_input = "//input[@id='Currency']"

    date_label = "//label[contains(.,'Date')]"
    date_input = "//input[@id='Date']"

    html_editor_label = "//label[contains(.,'HTML Editor')]"
    html_editor_input = "//div[contains(@class,'angular-editor-textarea') and @contenteditable='true']"


    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base = BaseHelpers(driver, timeout)

    def click_lookup(self):
        self.base.click(self.select_lookup, "lookup selected")


    # ---------------- Lookup navigation methods ----------------
    def open_lookups(self):
        self.base.click(self.side_nav_lookups, "Lookups")

    def click_create_lookup(self):
        self.base.click(self.create_lookup_button, "Create Lookup button")

    def enter_lookup_name(self, name):
        self.base.enter_text(self.enter_new_lookup_name, name, "New Lookup Name")

    def click_create_lookup_name(self):
        self.base.click(self.create_lookupname_button, "Create Lookup Name button")

    def click_publish_lookup(self):
        self.base.click(self.publish_lookup_button, "Publish Lookup button")

    def click_add_row(self):
        """Click the 'Add Row' button."""
        self.base.click(self.add_row_button, "Add Row Button")

    def enter_unique_lookup_name(self, base_name="Lookup Test Automation"):
        """Generate a unique Lookup name with timestamp and enter it"""
        current_time = datetime.now().strftime("%d-%m-%Y-(%H:%M)")
        unique_name = f"{base_name}--{current_time}"
        self.base.enter_text(self.enter_new_lookup_name, unique_name, "Workflow Name")
        print(f"⚡ Lookup Created: {unique_name}")
        return unique_name

    # ---------------- Field methods ----------------
    def click_add_field_button(self):
        self.base.click(self.add_field_button, "Add Field button")

    def click_add_field_button_lookup(self):
        self.base.click(self.add_field_button_lookup, "Add Field button in Lookup")

    def click_save_button(self):
        self.base.click(self.save_button, "Save button")

    def click_field_type_label(self):
        self.base.click(self.field_type_label, "Field Type label")

    def enter_field_display_name(self, name, locator=None):
        """Enter text into the Display Name textbox"""
        locator_to_use = locator or self.enter_display_name_input
        self.base.enter_text(locator_to_use, name, "Display Name")
        sleep(2)

    def enter_valid_values_lookup(self, values):
        """Enter comma-separated valid values into the 'Valid Values' textbox"""
        value_str = ",".join(values)
        self.base.enter_text(self.enter_valid_values_input, value_str, "Valid Values")
        sleep(2)

    def select_field_type(self, field_name):
        """Select a value from the Field Type dropdown"""
        dropdown = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//ng-select[@formcontrolname='fieldType']//div[contains(@class,'ng-select-container')]"
        )))
        dropdown.click()
        sleep(1)

        option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//span[normalize-space(text())='{field_name}']"
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()
        sleep(2)

    # ---------------- Unified add_field method ----------------
    def add_field(self, display_name, field_type=None, valid_values=None, click_add_field=True):
        """
        Add a new field in the Lookup.

        Args:
            display_name (str): Display Name of the field
            field_type (str, optional): Field type (e.g., TextBox, CheckBox)
            valid_values (list, optional): List of valid values (for dropdowns, checkbox lists)
            click_add_field (bool): Whether to click 'Add Field' after saving
        """
        self.enter_field_display_name(display_name)

        if field_type:
            self.select_field_type(field_type)

        if valid_values:
            self.enter_valid_values_lookup(valid_values)

        self.click_save_button()

        print(f"✅  Lookup field - '{display_name}' created successfully!")

        if click_add_field:
            self.click_add_field_button_lookup()


    def textbox(self, value):
        self.base.scroll_to_label(self.textbox_label, "TextBox")
        self.base.enter_text(self.textbox_input, value, "TextBox Input")

    def email(self, value):
        self.base.scroll_to_label(self.email_label, "Email")
        self.base.enter_text(self.email_input, value, "Email Input")

    def checkbox(self, check=True):
        """Check or uncheck the checkbox safely."""
        self.base.scroll_to_label(self.checkbox_label, "Checkbox")
        element = self.base.wait.until(EC.presence_of_element_located((By.XPATH, self.checkbox_input)))

        if check and not element.is_selected():
            element.click()
            print("✅ Checkbox checked – Checkbox")
        elif not check and element.is_selected():
            element.click()
            print("✅ Checkbox unchecked – Checkbox")
        else:
            print("ℹ️ Checkbox already in desired state – Checkbox")

    def decimal(self, value):
        self.base.scroll_to_label(self.decimal_label, "Decimal")
        self.base.enter_text(self.decimal_input, value, "Decimal Input")

    def ip_address(self, value):
        self.base.scroll_to_label(self.ip_address_label, "IP Address")
        self.base.enter_text(self.ip_address_input, value, "IP Address Input")

    def url(self, value):
        self.base.scroll_to_label(self.url_label, "URL")
        self.base.enter_text(self.url_input, value, "URL Input")

    def number(self, value):
        self.base.scroll_to_label(self.numbers_label, "Number")
        self.base.enter_text(self.numbers_input, value, "Number Input")

    def text_area(self, value):
        self.base.scroll_to_label(self.text_area_label, "TextBox MultiLine")
        self.base.enter_text(self.text_area_input, value, "TextArea Input")

    def currency(self, value):
        self.base.scroll_to_label(self.currency_label, "Currency")
        self.base.enter_text(self.currency_input, value, "Currency Input")

    def html_editor(self, value):
        self.base.scroll_to_label(self.html_editor_label, "HTML Editor")
        self.base.enter_text(self.html_editor_input, value, "HTML Editor Input")

    def select_lookup_dropdown(self, field_value):
        """
        Select a value from a Lookup ng-select dropdown.
        """
        try:
            # Scroll to the dropdown label
            self.base.scroll_to_label(self.dropdown_label, "DropDown List")

            # Click dropdown input
            dropdown_input = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, self.dropdown_input)))
            dropdown_input.click()
            sleep(0.5)

            # Type the value to filter
            dropdown_input.clear()
            dropdown_input.send_keys(field_value)
            sleep(0.5)

            # Click the option
            option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{field_value}']"
            option = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            sleep(0.5)

            # Finalize selection
            dropdown_input.send_keys(Keys.TAB)
            print(f"✅ Lookup Dropdown selected: {field_value}")

        except Exception as e:
            raise AssertionError(f"❌ Failed to select Lookup dropdown value '{field_value}': {e}")

    file_uploader_label = "//label[contains(.,'File')]"
    file_upload_icon = "//a[contains(@class,'upload') and (contains(@title,'Upload') or @title='')]"
    file_input = "//input[@type='file' and @id='attachmentFiles']"
    file_upload_button = "//div[contains(@class,'crt-pop-footer')]//button[contains(text(),'Upload')]"

    def file_uploader(self, file_path):
        """
        Upload a file in Workflow or Lookup form.
        Works for both popups since the input id is the same.
        """
        try:
            # Scroll to File Uploader label
            self.base.scroll_to_label(self.file_uploader_label, "File Uploader")

            # Click the Upload Icon using BaseHelpers click (handles JS fallback)
            self.base.click(self.file_upload_icon, "Upload Icon")
            sleep(1)  # wait for modal to open

            # Wait for file input to be present and send file path
            file_input_elem = self.base.wait.until(
                EC.presence_of_element_located((By.XPATH, self.file_input))
            )
            file_input_elem.send_keys(file_path)
            print(f"✅ File selected: {file_path}")
            sleep(1)

            # Click the Upload button
            self.base.click(self.file_upload_button, "Upload Button")
            sleep(2)
            print("✅ File uploaded successfully")

        except TimeoutException:
            raise AssertionError("❌ File uploader flow failed (element not found or not clickable)")
        except Exception as e:
            raise AssertionError(f"❌ File uploader failed: {str(e)}")

    def radio_button_lookup(self, option, label_text="Radio Button List"):
        """
        Select a radio button in the Lookup form.

        Args:
            option (str): The option to select (e.g., "A", "B", "C", "D")
            label_text (str): The label of the radio button group
        """
        try:
            # Scroll to the radio group label
            label_xpath = f"//label[contains(.,'{label_text}')]"
            self.base.scroll_to_label(label_xpath, label_text)

            # Build xpath for the specific option label
            option_label_xpath = f"//div[@name='{label_text.replace(' ', '_')}']//input[@id='{label_text.replace(' ', '_')}{option}']/following-sibling::label"
            option_label = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, option_label_xpath)))
            option_label.click()

            # Verify radio button is selected
            radio_input_xpath = f"//input[@id='{label_text.replace(' ', '_')}{option}']"
            radio_input = self.base.wait.until(EC.presence_of_element_located((By.XPATH, radio_input_xpath)))
            assert radio_input.is_selected(), f"❌ Radio button '{option}' not selected in '{label_text}'"

            print(f"✅ Radio button '{option}' selected successfully under '{label_text}'")

        except TimeoutException:
            raise AssertionError(f"❌ Radio button '{option}' under '{label_text}' not found or clickable")

    def select_checkboxes_lookup(self, checkbox_values, label_text="CheckBox List"):
        """
        Select multiple checkboxes in the Lookup form.

        Args:
            checkbox_values (list): List of values to select, e.g., ["A", "B", "C", "D"]
            label_text (str): The label of the checkbox group
        """
        try:
            # Scroll to the checkbox group label
            label_xpath = f"//label[contains(.,'{label_text}')]"
            self.base.scroll_to_label(label_xpath, label_text)
            sleep(1)

            for value in checkbox_values:
                # Checkbox input locator based on name and value
                checkbox_xpath = f"//input[@name='CheckBox_List' and @value='{value}']"
                checkbox_label_xpath = f"//label[@for='CheckBox_List{value}']"

                # Scroll to checkbox label
                self.base.scroll_to_label(checkbox_label_xpath, f"{label_text} '{value}'")

                checkbox = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))

                if not checkbox.is_selected():
                    checkbox.click()
                    sleep(1.5)
                    print(f"✅ Checked '{value}' in {label_text}")
                else:
                    print(f"ℹ️ '{value}' already selected in {label_text}")

        except TimeoutException:
            raise AssertionError(f"❌ Checkbox List '{label_text}' not found or clickable for values: {checkbox_values}")

    def select_ms_dropdown_lookup(self, ms_dropdown_values, label_text="MS DropDown List"):
        """
        Select multiple values from a Lookup MS Dropdown.
        """
        try:
            # Scroll to MS Dropdown label
            label_xpath = f"//label[contains(.,'{label_text}')]"
            self.base.scroll_to_label(label_xpath, label_text)

            # Verify the label
            label = self.base.wait.until(EC.visibility_of_element_located((By.XPATH, label_xpath)))
            if label.text.strip() != label_text:
                print(f"ℹ️ Label found but not MS Dropdown: {label.text.strip()}")
                return
            print(f"✅ Found label: {label_text}")

            # Locate dropdown input
            dropdown_input = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, self.ms_dropdown_input)))
            dropdown_input.click()
            sleep(0.5)

            # Select all values
            for value in ms_dropdown_values:
                dropdown_input.send_keys(value)
                option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{value}']"
                option = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                option.click()
                sleep(0.5)
                print(f"✅ Selected '{value}' in {label_text}")

            # Finalize selection
            dropdown_input.send_keys(Keys.TAB)

        except TimeoutException:
            raise AssertionError(f"❌ MS Dropdown '{label_text}' not found or clickable")

    def select_date_lookup(self, date_to_select, label_text="Date"):
        """
        Select a date in the Lookup date picker.

        Args:
            date_to_select (str): Date in format 'YYYY-MM-DD', e.g., '2025-10-04'
            label_text (str): Label of the date field
        """
        try:
            # Scroll to the label
            label_xpath = f"//label[contains(.,'{label_text}')]"
            self.base.scroll_to_label(label_xpath, label_text)

            # Locate the input element and click to open date picker
            input_xpath = f"{label_xpath}/following::input[contains(@class,'flatpickr-input')]"
            input_element = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            input_element.click()
            print(f"✅ Clicked Date input for '{label_text}'")

            # Split date
            year, month, day = map(int, date_to_select.split('-'))
            month -= 1  # Flatpickr months are 0-indexed

            # Select year
            year_input_xpath = "//input[contains(@class,'cur-year')]"
            year_input = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, year_input_xpath)))
            year_input.clear()
            year_input.send_keys(str(year))
            year_input.send_keys(Keys.ENTER)

            # Select month
            month_select_xpath = "//select[contains(@class,'flatpickr-monthDropdown-months')]"
            month_select = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, month_select_xpath)))
            month_select.send_keys(Keys.HOME)
            for _ in range(month):
                month_select.send_keys(Keys.ARROW_DOWN)
            month_select.send_keys(Keys.ENTER)

            # Select day
            day_xpath = f"//span[contains(@class,'flatpickr-day') and text()='{day}' and not(contains(@class,'prevMonthDay')) and not(contains(@class,'nextMonthDay'))]"
            day_element = self.base.wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
            day_element.click()

            print(f"✅ Selected date '{date_to_select}' for '{label_text}'")

        except TimeoutException:
            raise AssertionError(f"❌ Failed to select date '{date_to_select}' for '{label_text}'")

    # ---------- Common Table Value Helper ----------

    def get_table_value_by_id(self, column_label, target_id=1):
        """
        Fetch a table cell value dynamically by column label and row ID.
        Works even if there's only one row in the table.

        Args:
            column_label (str): Header name of the column to fetch (e.g., 'decimal')
            target_id (int): The ID value in the table row to match (default=1)

        Returns:
            str | None: The cell value as string, or None if not found
        """
        try:
            # 1️⃣ Find all header elements in the table
            headers = self.driver.find_elements(By.XPATH, "//th")
            column_index = None

            # 2️⃣ Determine the index of the column that matches the given label
            for idx, header in enumerate(headers, start=1):  # XPath is 1-based
                header_text = header.text.strip()
                if header_text.lower() == column_label.lower():
                    column_index = idx
                    break

            if column_index is None:
                print(f"❌ Column '{column_label}' not found in table headers.")
                return None

            # 3️⃣ Locate the table row where first cell (ID) matches target_id
            rows = self.driver.find_elements(
                By.XPATH,f"//tr[td//*[normalize-space(text())='{target_id}'] or td[normalize-space(text())='{target_id}']]")
            if not rows:
                print(f"❌ No row found with ID '{target_id}'.")
                return None

            # 4️⃣ Extract the specific cell using the dynamic column index
            cell_xpath = f"td[{column_index}]"
            cell = rows[0].find_element(By.XPATH, cell_xpath)
            cell_value = cell.text.strip()

            print(f"✅ Retrieved value '{cell_value}' from column '{column_label}' for row ID '{target_id}'.")
            return cell_value

        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"⛔ Error retrieving value from column '{column_label}': {e}")
            return None