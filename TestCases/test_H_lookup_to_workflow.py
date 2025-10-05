from time import sleep
import pytest
from PageObjects.H_lookup_to_workflow_populate import lookup_to_workflow_values

@pytest.mark.order(1)
def test_lookup_to_workflow_value_populate(login):

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

    # Example: loop 15 fields
    fields_to_select = [
        ("CheckBox", "Checkbox"),
        ("Decimal", "Decimal"),
        ("Number", "Number"),
        # ...add more pairs
    ]

    for idx, (target, current) in enumerate(fields_to_select, start=1):
        lw.select_populate_target_workflow(target, row_index=idx)
        lw.select_populate_current_workflow(current, row_index=idx)
        if idx != len(fields_to_select):
            lw.click_add_new_button_for_fields()



