import pytest
from time import sleep
from selenium.webdriver.common.by import By
from PageObjects.B_stage_creation import CreateWorkflow
from BaseFiles.Basehelpers import BaseHelpers

class Test_002_Stage_Creation:

    def test_stage_Creation(self, login, region):
        driver = login

        # Initialize BaseHelpers for verification methods
        base = BaseHelpers(driver)

        # ✅ Verify Login URL
        expected_login_url = f"https://{region.lower()}.cflowapps.com/cflow/login"
        base.verify_page_url(expected_login_url, f"test_loginpage_url_{region}")

        # ✅ Verify Dashboard page by unique element
        base.verify_page_by_element(
            (By.XPATH, "//p[contains(.,'Dashboard')]"),
            method_name="verify_dashboard_after_login"
        )

        # Initialize Workflow page object
        cw = CreateWorkflow(driver)

        # ✅ Perform Workflow Creation
        cw.open_workflow_setup()
        sleep(3)

        # Verify workflow setup page is loaded
        base.verify_page_by_element(
            (By.XPATH, "(//div[contains(.,'Workflow Setup')])[5]"),
            "verify_workflow_setup_page"
        )

        # Create new workflow
        cw.click_add_new_workflow()
        sleep(3)

        workflow_name = cw.enter_unique_workflow_name()
        cw.click_create_workflow()
        sleep(3)

        # Verify stage creation page is loaded
        base.verify_page_by_element(
            (By.XPATH, "//button[contains(.,'Stage Creation')]"),
            "verify_stage_creation_page"
        )

        # ✅ Stage 1
        cw.click_add_stage_button_s1()
        cw.select_add_stage_s1()
        cw.enter_stage_name_s1("PS1")
        cw.save_stage_s1()
        sleep(3)

        # ✅ Stage 2
        cw.click_add_stage_button_s2()
        cw.select_add_stage_s2()
        cw.enter_stage_name_s2("PS2")
        cw.save_stage_s2()

        # ✅ Stage 3
        cw.click_add_stage_button_s3()
        cw.select_add_stage_s3()
        cw.enter_stage_name_s3("PS3")
        cw.save_stage_s3()

        sleep(5)
        driver.refresh()
        cw.form_creation()

        # Verify form creation page is loaded
        base.verify_page_by_element(
            (By.XPATH, "//button[contains(.,'Form Creation')]"),
            "verify_form_creation_page"
        )

        print(f"✅ Workflow '{workflow_name}' created successfully in {region} region")
