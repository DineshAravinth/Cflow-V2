import pytest
from PageObjects.B_stage_creation import CreateWorkflow
from PageObjects.C_form_creation import FormCreation
from selenium.webdriver.common.by import By
from BaseFiles.Basehelpers import BaseHelpers
from time import sleep


# ---------- Workflow Setup ----------
@pytest.mark.order(1)
class Test_001_WorkflowSetup:
    def test_create_workflow(self, login, region):

        driver = login
        base = BaseHelpers(driver)
        cw = CreateWorkflow(driver)


        cw.open_workflow_setup()
        base.verify_workflow_setup_page()

        cw.click_add_new_workflow()

        workflow_name = cw.enter_unique_workflow_name("Test Automate")
        cw.click_create_workflow()

        # Store workflow_name for later tests (pytest cache or fixture)
        pytest.workflow_name = workflow_name
        print(f"✅ Workflow '{workflow_name}' created in {region} region")
        assert workflow_name, "❌ Workflow name is empty"

        base.verify_stage_creation_page()

# ---------- Stage Creation (Stage 1 + Stage 2) ----------
@pytest.mark.order(2)
class Test_002_StageCreation:
    def test_create_stage1_and_stage2(self, login):
        driver = login
        base = BaseHelpers(driver)
        cw = CreateWorkflow(driver)

        # Stage 1
        sleep(3)
        driver.refresh()
        cw.click_add_stage_button_s1()
        cw.select_add_stage_s1()
        cw.enter_stage_name_s1("PS1")
        cw.save_stage_s1()
        sleep(2)
        driver.refresh()

        print("✅ Stage 1 created successfully")

        # Stage 2
        cw.click_add_stage_button_s2()
        cw.select_add_stage_s2()
        cw.enter_stage_name_s2("PS2")
        cw.save_stage_s2()
        sleep(2)
        driver.refresh()
        print("✅ Stage 2 created successfully")

        # Stage 3
        cw.click_add_stage_button_s3()
        cw.select_add_stage_s3()
        cw.enter_stage_name_s3("PS3")
        cw.save_stage_s3()
        sleep(2)
        driver.refresh()
        print("✅ Stage 2 created successfully")



# ---------- Main Section Form ----------
@pytest.mark.order(3)
class Test_003_FormMainSection:
    def test_form_main_section(self, login):
        driver = login
        base = BaseHelpers(driver)
        cw = CreateWorkflow(driver)

        cw.form_creation()
        base.verify_form_creation_page()

        fc = FormCreation(driver)

        # Main Section
        fc.add_section_dragdrop()

        section_name = "Main Section"
        fc.section_name(section_name)
        fc.save_section()
        sleep(2)

        base.verify_section_present(section_name)

        # Basic Fields
        fc.add_dropdown()
        fc.add_textbox()
        fc.add_email()
        fc.add_checkbox()
        fc.add_decimal()
        fc.add_url()
        fc.add_ip_address()
        fc.add_radio_button()
        fc.add_file_uploader()
        fc.add_signature()
        fc.add_number()
        fc.add_ms_dropdown()
        fc.add_checkbox_list()
        fc.add_textarea()
        fc.add_currency()
        fc.add_date()
        fc.add_time()
        fc.add_html_editor()
        fc.add_terms_and_conditions()
        fc.add_identity()

        print("✅ Main Section created with fields")


# ---------- Table Section Form ----------
@pytest.mark.order(4)
class Test_004_FormTableSection:
    def test_form_table_section(self, login):
        driver = login
        base = BaseHelpers(driver)
        fc = FormCreation(driver)

        # Table Section
        fc.add_table_section_dragdrop()
        table_section_name = "Table Section"
        fc.table_section_name(table_section_name)
        fc.save_table_section()
        sleep(2)

        base.verify_section_present(table_section_name)

        # Table Fields
        sleep(2)
        fc.add_signature_table()
        fc.add_textbox_table()
        fc.add_email_table()
        fc.add_checkbox_table()
        fc.add_decimal_table()
        fc.add_number_table()
        fc.add_textarea_table()
        fc.add_currency_table()
        fc.add_date_table()
        fc.add_time_table()
        fc.add_url_table()
        fc.add_file_uploader_table()
        fc.add_ms_dropdown_table()
        fc.add_ip_address_table()
        fc.add_dropdown_table()

        print("✅ Table Section created with fields")

        fc.click_publish()
        sleep(3)
        driver.refresh()
        fc.click_go_to_workflow()
        sleep(3)
        base.verify_page_by_element(
            (By.XPATH, "(//span[contains(.,'Form')])[2]"),
            "verify_form-submission_page"
        )
