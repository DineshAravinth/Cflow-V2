import pytest
from time import sleep
from PageObjects.B_stage_creation import CreateWorkflow

class Test_002_Stage_Creation:

    def test_stage_Creation(self, login, region):
        # ✅ Use logged-in driver from fixture
        driver = login

        # ✅ Create Workflow object
        cw = CreateWorkflow(driver)

        # ✅ Perform Workflow Creation
        cw.open_workflow_setup()
        sleep(3)

        cw.click_add_new_workflow()
        sleep(3)

        workflow_name = cw.enter_unique_workflow_name("Test Automate")
        cw.click_create_workflow()
        sleep(3)

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

        sleep(10)
        driver.refresh()
        cw.form_creation()

        # ✅ Verification Example
        print(f"✅ Workflow '{workflow_name}' created successfully in {region} region")