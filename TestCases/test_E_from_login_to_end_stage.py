import pytest
from PageObjects.B_stage_creation import CreateWorkflow
from PageObjects.C_form_creation import FormCreation
from PageObjects.D_FormSubmission import FormSubmission
from selenium.webdriver.common.by import By
from BaseFiles.Basehelpers import BaseHelpers
from time import sleep


# ---------- Workflow Setup ----------
@pytest.mark.order(1)
class Test_001_WorkflowSetup:
    def test_create_workflow(self, login, region):

        driver = login
        base = BaseHelpers(driver)

        # ✅ Verify Dashboard page by unique element
        base.verify_page_by_element(
            (By.XPATH, "//p[contains(.,'Dashboard')]"),
            method_name="verify_dashboard_after_login")

        cw = CreateWorkflow(driver)

        cw.open_workflow_setup()

        cw.click_add_new_workflow()

        workflow_name = cw.enter_unique_workflow_name("Test Automate")
        cw.click_create_workflow()

        # Store workflow_name for later tests (pytest cache or fixture)
        pytest.workflow_name = workflow_name
        print(f"✅ Workflow '{workflow_name}' created in {region} region")
        assert workflow_name, "❌ Workflow name is empty"

        base.verify_page_by_element(
            (By.XPATH, "//button[contains(.,'Stage Creation')]"),
            "verify_stage_creation_page")


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
        print("✅ Stage 3 created successfully")


# ---------- Main Section Form ----------
@pytest.mark.order(3)
class Test_003_FormMainSection:
    def test_form_main_section(self, login):
        driver = login
        base = BaseHelpers(driver)
        cw = CreateWorkflow(driver)

        cw.form_creation()

        base.verify_page_by_element(
            (By.XPATH, "//button[contains(.,'Form Creation')]"),
            "verify_form_creation_page"
        )

        fc = FormCreation(driver)

        # Main Section
        fc.add_section_dragdrop()

        section_name = "Main Section"
        fc.section_name(section_name)
        fc.save_section()

        sleep(2)

        base.verify_element_present(
            (By.XPATH, f"//p[contains(.,'{section_name}')]"),
            f"verify_section-{section_name.replace(' ', '_')}")

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

        base.verify_element_present(
            (By.XPATH, f"//p[contains(.,'{table_section_name}')]"),
            f"verify_table-section-{table_section_name.replace(' ', '_')}")

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


@pytest.mark.order(5)
class Test_005_Workflow_Form_submission:
    def test_form_submission(self, login, region):
        driver = login
        base = BaseHelpers(driver)
        fs = FormSubmission(driver)

        # --- Open workflow and start new record ---
        # fs.open_workflow()
        # sleep(2)
        # fs.click_workflow()
        # fs.click_add_new_record()

        # --- Form field sequence ---
        sleep(3)
        fs.textbox(value="Test Automation")
        sleep(2)
        fs.email("dinesh@yopmail.com")
        sleep(2)
        fs.checkbox()
        sleep(2)
        fs.decimal("123.45")
        sleep(2)
        fs.select_dropdown(dropdown_value="B")
        sleep(2)
        fs.ip_address(value="192.168.1.1")
        sleep(2)
        fs.radio_button(option ="B")
        sleep(2)
        fs.url(value="https://example.com")
        sleep(2)
        fs.file_uploader(r"D:\DOWNLOADS (D)\Fat_Loss_Plan.pdf")
        sleep(2)
        fs.numbers(value="12345")
        sleep(2)
        fs.select_ms_dropdown(ms_dropdown_values=["B", "C"])
        sleep(2)
        fs.signature_upload(r"C:\Users\Venka\Downloads\Dinesh Aravinth Signature.jpg")
        sleep(2)
        fs.text_area(value="This is a test text area")
        sleep(2)
        fs.currency(value="1000")
        sleep(2)
        fs.select_date("2026-01-01")
        sleep(2)
        fs.select_time(time_to_select="14:30")
        sleep(2)
        fs.select_checkboxes(["B","C"])
        sleep(2)
        fs.html_editor(value="This is test HTML content")
        sleep(2)
        fs.agree_terms_and_conditions()
        sleep(2)

        fs.click_table_add_new_button()
        sleep(2)

        # fs.click_table_add_new_button()
        # sleep(2)

        # 1️⃣ Table TextBox
        fs.table_textbox("table test automation")
        sleep(2)

        # 2️⃣ Table Email
        fs.table_email("test@example.com")
        sleep(2)

        # 3️⃣ Table Signature
        fs.table_signature_upload(r"C:\Users\Venka\Downloads\Dinesh Aravinth Signature.jpg")
        sleep(2)

        # 5️⃣ Table Number
        fs.table_numbers("12345")
        sleep(2)

        fs.table_decimal("12.45")
        sleep(2)

        # 6️⃣ Table Text Area
        fs.table_text_area("This is a test text area")
        sleep(2)

        # 7️⃣ Table Currency
        fs.table_currency("1000")
        sleep(2)

        # 8️⃣ Table Date
        fs.table_select_date("2026-01-01")
        sleep(2)

        # 9️⃣ Table Time
        fs.table_select_time("14:30")
        sleep(2)

        # 🔟 Table URL
        fs.table_url("https://example.com")
        sleep(2)

        # 11️⃣ Table File Uploader
        fs.table_file_uploader(r"D:\DOWNLOADS (D)\Fat_Loss_Plan.pdf")
        sleep(2)

        # 12️⃣ Table Multi-Select Dropdown
        fs.table_ms_dropdown(["B", "C"])
        sleep(3)

        # 13️⃣ Table IP Address
        fs.table_ip_address("192.168.1.1")
        sleep(2)

        fs.select_table_dropdown(dropdown_value="B")
        sleep(2)

        fs.table_checkbox(check=True)
        sleep(2)

        fs.click_submit_form_button()
        sleep(5)

        base.verify_page_by_element(
            (By.XPATH, "(//span[contains(.,'Initiator')])[2]"),
            "verify_initiator_stage_inbox_page")

        # 1️⃣ Submit the form
        # ------------------- PS1 -------------------
        latest_ps1 = fs.process_latest_record_in_stage("PS1")
        print(f"✅ PS1 processed, latest record ID: {latest_ps1}")

        # ------------------- PS2 -------------------
        latest_ps2 = fs.process_latest_record_in_stage("PS2")
        print(f"✅ PS2 processed, latest record ID: {latest_ps2}")

        # ------------------- PS3 -------------------
        latest_ps3 = fs.process_latest_record_in_stage("PS3")
        print(f"✅ PS3 processed, latest record ID: {latest_ps3}")

        # ------------------- End Stage -------------------
        fs.process_latest_record_in_stage("End", verify_in_end=True, latest_id=latest_ps3)
        print(f"✅ Verified record ID {latest_ps3} reached End stage")
