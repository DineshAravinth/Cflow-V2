from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BaseFiles.Basehelpers import BaseHelpers
from datetime import datetime

class lookup_creation:

    side_nav_lookups = "(//span[contains(.,'Lookups')])[2]"

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

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base = BaseHelpers(driver, timeout)

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

        if click_add_field:
            self.click_add_field_button_lookup()
