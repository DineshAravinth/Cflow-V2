import pytest
from PageObjects.B_stage_creation import CreateWorkflow
from PageObjects.C_form_creation  import FormCreation
from PageObjects.D_FormSubmission import FormSubmission
from selenium.webdriver.common.by import By
from time import sleep

# ---------- Workflow Setup ----------
@pytest.mark.order(1)
class Test_004_Workflow_Form_submission:
    def test_form_submission(self, login, region):
        driver = login
        fs = FormSubmission(driver)

        # --- Open workflow and start new record ---
        fs.open_workflow()
        sleep(2)
        fs.click_workflow()
        fs.click_add_new_record()

        # --- Form field sequence ---
        sleep(2)
        fs.textbox(value="Test Automation")
        sleep(3)
        fs.email("dinesh@yopmail.com")
        sleep(3)
        fs.checkbox()
        sleep(3)
        fs.decimal("123.45")
        sleep(3)
        fs.select_dropdown(dropdown_value="B")
        sleep(3)
        fs.ip_address(value="192.168.1.1")
        sleep(3)
        fs.radio_button(option ="B")
        sleep(3)
        fs.url(value="https://example.com")
        sleep(3)
        fs.file_uploader(r"D:\DOWNLOADS (D)\Fat_Loss_Plan.pdf")
        sleep(3)
        fs.numbers(value="12345")
        sleep(3)
        fs.select_ms_dropdown(ms_dropdown_values=["B", "C"])
        sleep(3)
        fs.signature_upload(r"C:\Users\Venka\Downloads\Dinesh Aravinth Signature.jpg")
        sleep(3)
        fs.text_area(value="This is a test text area")
        sleep(3)
        fs.currency(value="1000")
        sleep(3)
        fs.select_date("2026-01-01")
        sleep(3)
        fs.select_time(time_to_select="14:30")
        sleep(3)
        fs.select_checkboxes(["B","C"])
        sleep(3)
        fs.html_editor(value="This is test HTML content")
        sleep(3)
        fs.agree_terms_and_conditions()
        sleep(3)

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
        sleep(3)

        fs.click_submit_form_button()
        sleep(5)

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

