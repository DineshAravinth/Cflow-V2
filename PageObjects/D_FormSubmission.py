import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from BaseFiles.Basehelpers import BaseHelpers

class FormSubmission:

    # ---------- Workflow Navigation ----------
    side_nav_workflows = "//a[contains(.,'Workflows')]"
    workflow_link_test_automation_form = "//a[contains(.,' test automation workflow form  ')]"
    add_new_record_button = "//a[contains(.,'Add New')]"

    # ---------- Form Fields ----------
    textbox_label = "//label[contains(.,'TextBox')]"
    textbox_input = "//input[@id='TextBox']"


    email_label = "//label[contains(.,'Email')]"
    email_input = "//input[@id='Email']"

    checkbox_label = "(//label[contains(.,'Checkbox')])[1]"
    checkbox_input = "//input[@id='Checkbox']"

    checkbox_list_label = "//label[contains(.,'Checkbox List')]"
    checkbox_list_input_template = "//input[@name='Checkbox_List' and @value='{value}']"

    decimal_label = "(//label[contains(.,'Decimal')])[1]"
    decimal_input = "//input[@id='Decimal']"

    dropdown_label = "(//label[contains(.,'Dropdown')])[1]"
    dropdown_input = "//ng-select[@id='Dropdown']"

    ip_address_label = "//label[contains(.,'IP Address')]"
    ip_address_input = "//input[@id='IP_Address']"

    radio_label_template = "(//label[contains(.,'{label_text}')])[1]"
    radio_input_template = "//input[@id='{input_id}']"

    url_label = "//label[contains(.,'URL')]"
    url_input = "//input[@id='URL']"

    numbers_label = "//label[contains(.,'Number')]"
    numbers_input = "//input[@id='Number']"

    time_label = "//label[contains(.,'Time')]"
    time_input = "//input[@id='Time']"

    text_area_label = "//label[contains(.,'Text Area')]"
    text_area_input = "//textarea[@id='Text_Area']"

    currency_label = "//label[contains(.,'Currency')]"
    currency_input = "//input[@id='Currency']"

    date_label = "//label[contains(.,'Date')]"
    date_input = "//input[@id='Date']"

    html_editor_label = "//label[contains(.,'HTML Editor')]"
    html_editor_input = "//div[contains(@class,'angular-editor-textarea') and @contenteditable='true']"

    terms_and_conditions_label = "(//label[contains(.,'Terms And Conditions ')])[1]"
    terms_and_conditions_input = "(//label[contains(.,' I agree to the above Terms And Conditions ')])[1]"

    signature_label = "//label[contains(.,'Signature')]"
    signature_upload_link = "(//a[contains(.,'Upload')])[1]"
    drop_signature = "//input[@id='file']"  # hidden file input where file path is sent
    signature_upload_button = "(//div[contains(@class,'crt-pop-footer')]//button[contains(text(),'Upload')])[1]"

    # ---------- File Upload Locators ----------
    file_uploader_label = "//label[contains(.,'File Uploader')]"
    file_upload_icon = "//a[contains(@class, 'upload') and @title='Upload']"
    file_input = "//input[@type='file' and @id='attachmentFiles']"
    file_upload_button = "//div[contains(@class,'crt-pop-footer')]//button[contains(text(),'Upload')]"


    # ---------- Table Form Fields ---------
    table_add_new_button = "// a[contains(., '+Add New')]"

    # ---------- Table Form Fields ----------
    table_textbox_label = "//span[contains(.,'TextBox')]"
    table_textbox_input = "//input[@id='T_01_TextBox']"

    table_email_label = "//span[contains(.,'Email')]"
    table_email_input = "//input[@id='T_01_Email']"

    table_checkbox_label = "//span[contains(.,'Checkbox')]"
    table_checkbox_input = "//input[@id='T_01_Checkbox']"

    table_decimal_label = "//span[contains(.,'Decimal')]"
    table_decimal_input = "//input[@id='T_01_Decimal']"

    table_dropdown_label = "//span[contains(.,'Dropdown')]"
    table_dropdown_input = "//ng-select[@id='T_01_Dropdown']"

    table_ip_address_label = "//span[contains(.,'IP Address')]"
    table_ip_address_input = "//input[@id='T_01_IP_Address']"

    table_url_label = "//span[contains(.,'URL')]"
    table_url_input = "//input[@id='T_01_URL']"

    table_numbers_label = "//span[contains(.,'Number')]"
    table_numbers_input = "//input[@id='T_01_Number']"

    table_time_label = "(//span[contains(.,'Time')])[3]"
    table_time_input = "(//input[@id='T_01_Time'])[1]"

    table_date_label = "//span[contains(.,'Date')]"
    table_date_input = "//input[@id='T_01_Date']"

    table_currency_label = "//span[contains(.,'Currency')]"
    table_currency_input = "//input[@id='T_01_Currency']"

    table_text_area_label = "//span[contains(.,'Text Area')]"
    table_text_area_input = "//textarea[@id='T_01_Text_Area']"

        # ---------- Table Signature ----------
    table_signature_label = "//span[contains(.,'Signature')]"
    table_signature_upload_link = "(//a[contains(.,'Upload')])[2]"
    table_drop_signature = "//input[@id='file']"
    table_signature_upload_button = "(//div[contains(@class,'crt-pop-footer')]//button[contains(text(),'Upload')])[1]"

    # ---------- Table File Uploader ----------
    table_file_uploader_label = "//span[contains(.,'File Uploader')]"
    table_file_upload_icon = "(//a[contains(@class, 'upload') and @title='Upload'])[4]"
    table_file_input = "//input[@id='attachmentFiles']"
    table_file_upload_button = "(//div[contains(@class,'crt-pop-footer')]//button[contains(text(),'Upload')])"

    table_ms_dropdown_label = "//span[contains(.,'MS Dropdown')]"

    submit_form_button = "//button[contains(.,'Submit Form')]"

    Change_process_stage_button = "//button[contains(.,' Change Process Stage ')]"
    stage_option = "//button[@ngbdropdownitem and normalize-space(text())='{stage_name}']"

    # ---------- Initialization ----------
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base = BaseHelpers(driver, timeout)

    # ---------- Generic Helpers ----------
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
                time.sleep(0.3)  # short wait before retry
            except TimeoutException:
                raise AssertionError(f"❌ Timeout: {description} not clickable")
            except NoSuchElementException:
                raise AssertionError(f"❌ Not Found: {description}")

        raise Exception(f"❌ Failed to click {description} after {retries} retries")

    def enter_text(self, xpath, text, description="textbox", retries=3):
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
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", label)
            log_name = friendly_name if friendly_name else (label.text.strip() or "Label")
            print(f"✅ Label visible – {log_name}")
            return label
        except TimeoutException:
            raise AssertionError(f"❌ Label not found: {label_xpath}")

    # ---------- Workflow Navigation Methods ----------
    def open_workflow(self):
        self.click(self.side_nav_workflows, "Workflows")

    def click_workflow(self):
        self.click(self.workflow_link_test_automation_form, "test automation workflow form")

    def click_add_new_record(self):
        self.click(self.add_new_record_button, "Add New Workflow button")

    def click_table_add_new_button(self):
        self.click(self.table_add_new_button, "Add New Workflow button")

    def click_submit_form_button(self):
        self.click(self.submit_form_button,"submit form button")

    # ---------- Form Field Methods ----------
    def textbox(self, value):
        self.scroll_to_label(self.textbox_label, "TextBox")
        self.enter_text(self.textbox_input, value, "TextBox Input")

    def email(self, value):
        self.scroll_to_label(self.email_label, "Email")
        self.enter_text(self.email_input, value, "Email Input")

    def decimal(self, value):
        self.scroll_to_label(self.decimal_label, "Decimal")
        self.enter_text(self.decimal_input, value, "Decimal Input")

    def ip_address(self, value):
        self.scroll_to_label(self.ip_address_label, "IP Address")
        self.enter_text(self.ip_address_input, value, "IP Address")

    def url(self, value):
        self.scroll_to_label(self.url_label, "URL")
        self.enter_text(self.url_input, value, "URL Input")

    def text_area(self, value):
        self.scroll_to_label(self.text_area_label, "Text Area")
        self.enter_text(self.text_area_input, value, "Text Area Input")

    def currency(self, value):
        self.scroll_to_label(self.currency_label, "Currency")
        self.enter_text(self.currency_input, value, "Currency Input")

    def html_editor(self, value):
        self.scroll_to_label(self.html_editor_label, "HTML Editor")
        self.enter_text(self.html_editor_input, value, "HTML Editor Input")

    def numbers(self, value):
        self.scroll_to_label(self.numbers_label, "Number")
        self.enter_text(self.numbers_input, value, "Number Input")

    def checkbox(self, check=True):
        self.scroll_to_label(self.checkbox_label, "Checkbox")
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.checkbox_input)))

        if check and not element.is_selected():
            element.click()
            print("✅ Checkbox checked – Checkbox")
        elif not check and element.is_selected():
            element.click()
            print("✅ Checkbox unchecked – Checkbox")
        else:
            print("ℹ️ Checkbox already in desired state – Checkbox")

    def agree_terms_and_conditions(self, check=True):
        try:
            self.scroll_to_label(self.terms_and_conditions_label, "Terms And Conditions")
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.terms_and_conditions_input)))
            if check and not element.is_selected():
                element.click()
                print("✅ Terms and Conditions checkbox checked")
            elif not check and element.is_selected():
                element.click()
                print("✅ Terms and Conditions checkbox unchecked")
            else:
                print("ℹ️ Terms and Conditions checkbox already in desired state")
        except TimeoutException:
            raise AssertionError("❌ Terms and Conditions checkbox not found or not clickable")

    def select_dropdown(self, dropdown_value):
        try:
            dropdown_input = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ng-input input[role='combobox']"))
            )
            dropdown_input.click()
            dropdown_input.clear()
            dropdown_input.send_keys(dropdown_value)

            option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{dropdown_value}']"
            option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            dropdown_input.send_keys(Keys.TAB)

            time.sleep(1)  # optional small wait
            print(f"✅ Dropdown '{dropdown_value}' selected")

        except TimeoutException:
            raise AssertionError("❌ Failed to select dropdown value")


    def radio_button(self, option, label_text="Radio Button"):
        try:
            label_xpath = self.radio_label_template.format(label_text=label_text)
            self.scroll_to_label(label_xpath, label_text)

            option_label_xpath = f"{label_xpath}/following::input[@id='Radio_Button{option}']/following-sibling::label"
            option_label = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_label_xpath)))
            option_label.click()

            radio_id = option_label.get_attribute("for")
            input_xpath = self.radio_input_template.format(input_id=radio_id)
            radio_input = self.wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
            assert radio_input.is_selected(), f"❌ Radio button '{option}' not selected"

            print(f"✅ Radio button '{option}' selected successfully under '{label_text}'")

        except TimeoutException:
            raise AssertionError(f"❌ Radio button '{option}' under '{label_text}' not found or clickable")

    def file_uploader(self, file_path):
        try:
            self.scroll_to_label(self.file_uploader_label, "File Uploader")
            self.click(self.file_upload_icon, "Upload Icon")
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.file_input)))
            file_input.send_keys(file_path)
            print(f"✅ File selected: {file_path}")
            time.sleep(2)
            upload_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.file_upload_button)))
            upload_btn.click()
            time.sleep(2)
            print("✅ File uploaded successfully")
        except TimeoutException:
            raise AssertionError("❌ File uploader flow failed (element not found or not clickable)")

    def select_ms_dropdown(self, ms_dropdown_values, label_text="MS Dropdown"):
        try:
            label_xpath = f"//label[contains(.,'{label_text}')]"
            self.scroll_to_label(label_xpath, label_text)

            label = self.wait.until(EC.visibility_of_element_located((By.XPATH, label_xpath)))
            actual_label_text = label.text.strip()

            if actual_label_text != label_text:
                print(f"ℹ️ Label found but not MS Dropdown: {actual_label_text}")
                return
            else:
                print(f"✅ Found label: {label_text}")

            dropdown_input_xpath = f"{label_xpath}/following::div[contains(@class,'ng-value-container')]//input[@role='combobox']"
            dropdown_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_input_xpath)))
            dropdown_input.click()

            for value in ms_dropdown_values:
                dropdown_input.send_keys(value)
                option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{value}']"
                option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                option.click()
                time.sleep(2)
                print(f"✅ Selected '{value}' in MS Dropdown")
                dropdown_input.send_keys(Keys.TAB)
                dropdown_input.click()

            dropdown_input.send_keys(Keys.TAB)

        except TimeoutException:
            raise AssertionError(f"❌ MS Dropdown '{label_text}' not found or clickable")

    def select_checkboxes(self, checkbox_values):
        try:
            for value in checkbox_values:
                checkbox_xpath = f"//input[@name='Checkbox_List' and @value='{value}']"
                checkbox_label_xpath = f"{checkbox_xpath}/following-sibling::label"

                self.scroll_to_label(checkbox_label_xpath, f"Checkbox '{value}'")
                checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))

                if not checkbox.is_selected():
                    checkbox.click()
                    time.sleep(2)
                    print(f"✅ Checked '{value}' in Checkbox List")
                else:
                    print(f"ℹ️ '{value}' already selected in Checkbox List")

        except TimeoutException:
            raise AssertionError(f"❌ Checkbox List not found or clickable for values: {checkbox_values}")

    def signature_upload(self, file_path):
        try:
            self.scroll_to_label(self.signature_label, "Signature")
            self.click(self.signature_upload_link, "Signature Upload Link")
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.drop_signature)))
            file_input.send_keys(file_path)
            print(f"✅ Signature file selected: {file_path}")
            time.sleep(2)
            upload_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.signature_upload_button)))
            upload_btn.click()
            print("✅ Signature uploaded successfully")
        except TimeoutException:
            raise AssertionError("❌ Signature upload flow failed (element not found or not clickable)")

    def select_date(self, date_to_select):
        try:
            self.scroll_to_label(self.date_label, "Date")
            input_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.date_input)))
            input_element.click()
            print(f"✅ Clicked Date input to open date picker")

            year, month, day = map(int, date_to_select.split('-'))
            month -= 1

            year_input_xpath = "//input[contains(@class,'cur-year')]"
            year_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, year_input_xpath)))
            year_input.clear()
            year_input.send_keys(str(year))
            year_input.send_keys(Keys.ENTER)

            month_select_xpath = "//select[contains(@class,'flatpickr-monthDropdown-months')]"
            month_select = self.wait.until(EC.element_to_be_clickable((By.XPATH, month_select_xpath)))
            month_select.send_keys(Keys.HOME)
            for _ in range(month):
                month_select.send_keys(Keys.ARROW_DOWN)
            month_select.send_keys(Keys.ENTER)

            day_xpath = f"//span[contains(@class,'flatpickr-day') and text()='{day}']"
            day_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
            day_element.click()

            print(f"✅ Selected date: {date_to_select}")

        except TimeoutException:
            raise AssertionError(f"❌ Failed to select date: {date_to_select}")

    def select_time(self, time_to_select):
        try:
            self.scroll_to_label(self.time_label, "Time")
            input_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.time_input)))
            input_element.click()
            print("✅ Clicked Time input to open time picker")

            hour, minute = map(int, time_to_select.split(":"))
            am_pm = "AM"
            if hour >= 12:
                am_pm = "PM"
                if hour > 12:
                    hour -= 12
            elif hour == 0:
                hour = 12

            hour_input_xpath = "//input[contains(@class,'flatpickr-hour')]"
            hour_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, hour_input_xpath)))
            hour_input.clear()
            hour_input.send_keys(str(hour))

            minute_input_xpath = "//input[contains(@class,'flatpickr-minute')]"
            minute_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, minute_input_xpath)))
            minute_input.clear()
            minute_input.send_keys(str(minute).zfill(2))

            am_pm_toggle_xpath = "//span[contains(@class,'flatpickr-am-pm')]"
            am_pm_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, am_pm_toggle_xpath)))
            current_am_pm = am_pm_element.text.strip()
            if current_am_pm != am_pm:
                am_pm_element.click()

            minute_input.send_keys(Keys.ENTER)
            input_element.send_keys(Keys.TAB)

            print(f"✅ Time selected: {time_to_select} ({am_pm})")

        except TimeoutException:
            raise AssertionError(f"❌ Failed to select time: {time_to_select}")


    # ---------- Table TextBox Method ----------

    # ---------- Table Field Methods ----------

    def table_textbox(self, value):
        self.scroll_to_label(self.table_textbox_label, "Table TextBox")
        self.enter_text(self.table_textbox_input, value, "Table TextBox Input")

    def table_email(self, value):
        self.scroll_to_label(self.table_email_label, "Table Email")
        self.enter_text(self.table_email_input, value, "Table Email Input")

    # ---------- Table Dropdown and Decimal Method ----------
    def select_table_dropdown(self, dropdown_value):
        """
        Selects a value from the table dropdown.
        """
        try:
            self.scroll_to_label(self.table_dropdown_label, "Table Dropdown")

            dropdown_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"{self.table_dropdown_input}//input[@role='combobox']"))
            )
            dropdown_input.click()
            dropdown_input.clear()
            dropdown_input.send_keys(dropdown_value)

            option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{dropdown_value}']"
            option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            dropdown_input.send_keys(Keys.TAB)

            time.sleep(1)  # optional small wait
            print(f"✅ Table Dropdown '{dropdown_value}' selected")

        except TimeoutException:
            raise AssertionError(f"❌ Table Dropdown '{dropdown_value}' not found or clickable")

    # ---------- Table Decimal Input ----------
    def table_decimal(self, decimal_value):
        """
        Enters a decimal value into the table decimal input.
        """
        try:
            decimal_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.table_decimal_input))
            )
            decimal_input.clear()
            decimal_input.send_keys(decimal_value)

            print(f"✅ Table Decimal '{decimal_value}' entered")

        except TimeoutException:
            raise AssertionError(f"❌ Table Decimal input not found or clickable")

    def table_ip_address(self, value):
        self.scroll_to_label(self.table_ip_address_label, "Table IP Address")
        self.enter_text(self.table_ip_address_input, value, "Table IP Address Input")

    def table_url(self, value):
        self.scroll_to_label(self.table_url_label, "Table URL")
        self.enter_text(self.table_url_input, value, "Table URL Input")

    def table_numbers(self, value):
        self.scroll_to_label(self.table_numbers_label, "Table Number")
        self.enter_text(self.table_numbers_input, value, "Table Number Input")

    # ---------- Table Date Picker ----------
    def table_select_date(self, date_to_select):
        """
        Selects a date in the table form field using Flatpickr.
        Works reliably for table date pickers with multiple Flatpickr instances.
        :param date_to_select: Date in 'YYYY-MM-DD' format
        """
        try:
            # 1️⃣ Scroll to the Table Date field
            self.scroll_to_label(self.table_date_label, "Table Date")

            # 2️⃣ Click the table input to open the date picker
            input_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.table_date_input))
            )
            input_element.click()
            print(f"✅ Clicked Table Date input to open date picker")

            # 3️⃣ Parse the date
            year, month, day = map(int, date_to_select.split('-'))
            month -= 1  # Flatpickr months are 0-based in select

            # 4️⃣ Select the year
            year_input_xpath = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//input[contains(@class,'cur-year')]"
            year_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, year_input_xpath)))
            year_input.clear()
            year_input.send_keys(str(year))
            year_input.send_keys(Keys.ENTER)

            # 5️⃣ Select the month
            month_select_xpath = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]//select[contains(@class,'flatpickr-monthDropdown-months')]"
            month_select = self.wait.until(EC.element_to_be_clickable((By.XPATH, month_select_xpath)))
            month_select.send_keys(Keys.HOME)
            for _ in range(month):
                month_select.send_keys(Keys.ARROW_DOWN)
            month_select.send_keys(Keys.ENTER)

            # 6️⃣ Select the day (only in the visible calendar)
            day_xpath = (
                f"//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"
                f"//span[contains(@class,'flatpickr-day') and text()='{day}'"
                f" and not(contains(@class,'prevMonthDay')) and not(contains(@class,'nextMonthDay'))]"
            )
            day_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", day_element)
            day_element.click()

            print(f"✅ Selected Table date: {date_to_select}")

        except Exception as e:
            print(f"❌ Failed to select Table date: {date_to_select}. Error: {e}")

        except Exception as e:
            print(f"❌ Failed to select Table date: {date_to_select}. Error: {e}")

        except TimeoutException:
            raise AssertionError(f"❌ Failed to select Table date: {date_to_select}")

    # ---------- Table Time Picker ----------
    def table_select_time(self, time_to_select):
        try:
            label = self.table_time_label
            input_box = self.table_time_input
            section = "Table Time"

            # Scroll to label and click input (force JS click to avoid redirect to main)
            self.scroll_to_label(label, section)
            input_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_box)))
            self.driver.execute_script("arguments[0].click(); arguments[0].focus();", input_element)
            print(f"✅ Clicked {section} input to open time picker")

            # Wait for calendar to open for THIS input
            calendar_xpath = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, calendar_xpath)))

            # Split input time
            hour, minute = map(int, time_to_select.split(":"))
            am_pm = "AM"
            if hour >= 12:
                am_pm = "PM"
                if hour > 12:
                    hour -= 12
            elif hour == 0:
                hour = 12

            # Get elements inside the open calendar
            hour_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"{calendar_xpath}//input[contains(@class,'flatpickr-hour')]")))
            minute_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"{calendar_xpath}//input[contains(@class,'flatpickr-minute')]")))
            am_pm_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"{calendar_xpath}//span[contains(@class,'flatpickr-am-pm')]")))

            # Fill values using JS + send_keys
            self.driver.execute_script("arguments[0].value = '';", hour_input)
            hour_input.send_keys(str(hour))

            self.driver.execute_script("arguments[0].value = '';", minute_input)
            minute_input.send_keys(str(minute).zfill(2))

            if am_pm_element.text.strip() != am_pm:
                am_pm_element.click()

            minute_input.send_keys(Keys.ENTER)
            input_element.send_keys(Keys.TAB)

            print(f"✅ {section} selected: {time_to_select} ({am_pm})")

        except Exception as e:
            print(f"❌ Error selecting {section}: {e}")

    def table_currency(self, value):
        self.scroll_to_label(self.table_currency_label, "Table Currency")
        self.enter_text(self.table_currency_input, value, "Table Currency Input")

    def table_text_area(self, value):
        self.scroll_to_label(self.table_text_area_label, "Table Text Area")
        self.enter_text(self.table_text_area_input, value, "Table Text Area Input")

    # ---------- Table Signature Upload Method ----------
    def table_signature_upload(self, file_path):
        try:
            self.scroll_to_label(self.table_signature_label, "Table Signature")
            self.click(self.table_signature_upload_link, "Table Signature Upload Link")
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.table_drop_signature)))
            file_input.send_keys(file_path)
            print(f"✅ Table Signature file selected: {file_path}")
            time.sleep(2)
            upload_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_signature_upload_button)))
            upload_btn.click()
            time.sleep(2)
            print("✅ Table Signature uploaded successfully")
        except TimeoutException:
            raise AssertionError("❌ Table Signature upload flow failed (element not found or not clickable)")

    # ---------- Table File Uploader Method ----------
    def table_file_uploader(self, file_path):
        try:
            # Scroll to uploader label
            self.scroll_to_label(self.table_file_uploader_label, "Table File Uploader")

            # Click upload icon (opens file dialog)
            self.click(self.table_file_upload_icon, "Table Upload Icon")

            # Send file to input
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.table_file_input)))
            file_input.send_keys(file_path)
            print(f"✅ Table File selected: {file_path}")

            time.sleep(2)  # optional: wait for file to register in UI

            # Click Upload button
            upload_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.table_file_upload_button)))
            upload_btn.click()
            time.sleep(2)
            print("✅ Table File uploaded successfully")

        except TimeoutException:
            raise AssertionError("❌ Table File uploader flow failed (element not found or not clickable)")

    def table_ms_dropdown(self, ms_dropdown_values, label_text="MS Dropdown"):
        label_xpath = f"//span[contains(.,'{label_text}')]"
        self.scroll_to_label(label_xpath, f"Table {label_text}")

        dropdown_input_xpath = f"{label_xpath}/following::div[contains(@class,'ng-value-container')]//input[@role='combobox']"
        dropdown_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_input_xpath)))
        dropdown_input.click()

        for value in ms_dropdown_values:
            dropdown_input.send_keys(value)
            option_xpath = f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option') and normalize-space()='{value}']"
            option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            print(f"✅ Selected '{value}' in Table MS Dropdown")
            dropdown_input.send_keys(Keys.TAB)
            dropdown_input.click()

    def table_checkbox(self, check=True):
        """
        Scrolls to the Table Checkbox label and checks/unchecks it based on the 'check' argument.
        """
        try:
            # Scroll to the label first
            self.scroll_to_label(self.table_checkbox_label, "Table Checkbox")

            # Locate the checkbox input
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.table_checkbox_input)))

            # Check or uncheck based on the 'check' argument
            if check and not element.is_selected():
                element.click()
                print("✅ Table Checkbox checked")
            elif not check and element.is_selected():
                element.click()
                print("✅ Table Checkbox unchecked")
            else:
                print("ℹ️ Table Checkbox already in desired state")

        except TimeoutException:
            raise AssertionError("❌ Table Checkbox not found or clickable")

    CHANGE_STAGE_BTN = "//button[contains(.,'Change Process Stage')]"
    STAGE_OPTION = "//button[@ngbdropdownitem and normalize-space(text())='{stage}']"
    ID_CELLS = "//td[@data-title='ID' and @currecordid]"
    APPROVE_BTN = "//label[contains(.,'Approved')]"
    SUBMIT_BTN = "//button[contains(.,'Submit Form')]"

    def process_latest_record_in_stage(self, stage_name, verify_in_end=False, latest_id=None):
        """
        Generic method to go to a stage, select latest record, approve & submit (if not End),
        and optionally verify latest_id in End stage.
        """
        print(f"➡️ Navigating to {stage_name} stage...")

        # 1. Click Change Process Stage
        self.click(self.CHANGE_STAGE_BTN, "Change Process Stage button")
        time.sleep(5)

        # 2. Select stage
        self.click(self.STAGE_OPTION.format(stage=stage_name), f"{stage_name} stage option")
        time.sleep(3)

        self.base.verify_page_by_element(
            (By.XPATH, f"(//span[contains(.,'{stage_name}')])[2]"),
            f"verify_{stage_name}_stage_inbox_page")

        # 3. Wait for ID cells
        rows = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, self.ID_CELLS))
        )

        # 4. Extract IDs
        record_ids = [int(td.get_attribute("currecordid")) for td in rows
                      if td.get_attribute("currecordid") and td.get_attribute("currecordid").isdigit()]

        if not record_ids:
            raise AssertionError(f"❌ No records found in {stage_name} stage inbox")

        if stage_name != "End":
            # 5. Latest record in this stage
            latest_stage_id = max(record_ids)
            print(f"✅ Latest record id found in {stage_name}: {latest_stage_id}")

            # 6. Click the latest record
            latest_xpath = f"//td[@data-title='ID' and @currecordid='{latest_stage_id}']"
            self.click(latest_xpath, f"Record ID {latest_stage_id}")
            time.sleep(2)

            # 7. Approve & Submit
            self.click(self.APPROVE_BTN, f"Record ID {latest_stage_id} -- Approved in {stage_name}")
            time.sleep(2)
            self.click(self.SUBMIT_BTN, f"Record ID {latest_stage_id} -- Submitted in {stage_name}")
            time.sleep(3)

            return latest_stage_id
        else:
            # ✅ Only verify latest_id exists in End stage
            if latest_id is None:
                raise ValueError("latest_id must be provided to verify in End stage")

            print(f"🔹 Verifying if Record ID {latest_id} exists in End stage...")
            if latest_id in record_ids:
                print(f"✅ Record ID {latest_id} is present in End stage")
            else:
                raise AssertionError(f"❌ Record ID {latest_id} not found in End stage")
            return None
