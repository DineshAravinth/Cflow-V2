from time import sleep
import pytest
from PageObjects.H_lookup_to_workflow_populate import lookup_to_workflow_values


@pytest.mark.order(1)
class Test_001_new_workflow_creation:
    def test_lookup_to_workflow_setup(self, login, region):

        driver = login
        lw = lookup_to_workflow_values(driver)

        lw.open_workflow_setup()
        sleep(2)
        lw.click_workflow()
        sleep(2)
        driver.refresh()
        sleep(2)
        lw.click_advanced_button()
        sleep(2)
        lw.click_lookup_side_nav()
        sleep(2)
        lw.click_add_new_button()
        sleep(2)
        lw.select_workflow_lookup_field("Lookup Test Automation--04-10-2025-(13:46) to Workflow")
        sleep(2)
        lw.enter_description("Test Automation lookup")
        sleep(2)
        lw.select_target_workflow_lookup_field("TextBox")
        sleep(3)
        lw.select_current_workflow_field("TextBox")
        sleep(3)
        lw.populate_all_fields()
        sleep(2)
        lw.save_button_lookup()
        sleep(2)
        print("Lookup to workflow setup saved successfully")
        lw.click_go_to_workflow()
        sleep(2)
        lw.textbox("Test Automation")
        sleep(2)

    # def test_lookup_to_workflow_value_submission(self, login, region):
    #
    #     driver = login
    #     lw = lookup_to_workflow_values(driver)
    #
    #
    #     lw.click_go_to_workflow()
    #     sleep(2)
    #     lw.textbox("Test Automation")





