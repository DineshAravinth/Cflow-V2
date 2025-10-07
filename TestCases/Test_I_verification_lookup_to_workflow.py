from time import sleep
import pytest
from PageObjects.H_lookup_to_workflow_populate import lookup_to_workflow_values
from PageObjects.G_lookup_creation import lookup_creation


@pytest.mark.order(1)
class Test_001_verify_lookup_to_workflow:
    def test_verification_lookup_to_workflow_setup(self, login, region):
        driver = login
        lookup = lookup_creation(driver)

        lw = lookup_to_workflow_values(driver)
        lw.open_workflow_setup()

        lookup.open_lookups()
        sleep(2)
        lookup.click_lookup()
        sleep(3)

        decimal_value = lookup.get_table_value_by_id("decimal", 1)
        print(decimal_value)

        sleep(5)
        lw.open_workflow()
        sleep(2)
        lw.open_workflow_lookup1()
        sleep(2)
        lw.click_add_new_record()
        sleep(3)
        lw.textbox("Test Automation")
        sleep(5)
        lw.click_submit_form_button()
        sleep(3)
        latest_ps1 = lw.process_latest_record_in_stage("PS1")

        if decimal_value is not None:
            # Step 3: Call the verification method with label and expected value
            lw.verify_decimal_workflow(label_text="Decimal", expected_value=float(decimal_value))
        else:
            print("❌ Could not retrieve expected decimal value from the table")



