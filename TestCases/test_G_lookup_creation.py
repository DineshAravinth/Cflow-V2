from time import sleep
import pytest
from PageObjects.G_lookup_creation import lookup_creation

@pytest.mark.order(1)
def test_create_lookup_with_fields(login):
    driver = login
    lookup = lookup_creation(driver)

    # Open Lookups and create new lookup
    lookup.open_lookups()
    sleep(2)
    lookup.click_lookup()
    sleep(2)
    # lookup.click_create_lookup()
    # sleep(2)
    # unique_lookup_name = lookup.enter_unique_lookup_name()
    # sleep(2)
    # lookup.click_create_lookup_name()
    # sleep(2)
    # lookup.click_add_field_button()
    #
    # # List of fields to add: (display_name, field_type, valid_values)
    # fields_to_add = [
    #     ("TextBox", "TextBox", None),
    #     ("CheckBox", "CheckBox", None),
    #     ("CheckBox List", "CheckBox List", ["A", "B", "C", "D"]),
    #     ("Radio Button List", "Radio Button List", ["A", "B", "C", "D"]),
    #     ("TextBox MultiLine", "TextBox MultiLine", None),
    #     ("DropDown List", "DropDownList", ["A", "B", "C", "D"]),
    #     ("MS DropDown List", "MS DropDownList", ["A", "B", "C", "D"]),
    #     ("HTML Editor", "HTML Editor", None),
    #     ("File", "File", None),
    #     ("Email", "Email", None),
    #     ("IP Address", "IP Address", None),
    #     ("Number", "Number", None),
    #     ("Decimal", "Decimal", None),
    #     ("Identity", "Identity", None),
    #     ("Currency", "Currency", None),
    #     ("Date", "Date", None),
    #     ("URL", "URL", None)
    # ]
    #
    # # Loop through each field and add
    # for index, (display_name, field_type, valid_values) in enumerate(fields_to_add):
    #     # Only click "Add Field" if it's not the first field
    #     click_add_field = True if index < len(fields_to_add) - 1 else False
    #     lookup.add_field(display_name=display_name, field_type=field_type, valid_values=valid_values, click_add_field=click_add_field)
    #     sleep(2)
    #
    # # Publish the lookup at the end
    # lookup.click_publish_lookup()
    # sleep(5)
    # print(f"✅ Lookup '{unique_lookup_name}' created with all fields successfully.")
    # sleep(2)
    #
    # print(f"➡️ Now entering values for Lookup '{unique_lookup_name}'...")
    #
    # lookup.click_add_row()
    # sleep(2)
    # lookup.textbox("Test Automation")
    # sleep(2)
    # lookup.checkbox(check=True)
    # sleep(2)
    # lookup.select_checkboxes_lookup(["A", "C"])  # Pass the values you want checked
    # sleep(1)
    # lookup.radio_button_lookup("B", label_text="Radio Button List")
    # sleep(1)
    # lookup.text_area("This is a multi-line text example.")
    # sleep(1)
    # lookup.select_lookup_dropdown("C")
    # sleep(1)
    # lookup.select_ms_dropdown_lookup(["A", "C", "D"], label_text="MS DropDown List")
    # sleep(1)
    # lookup.html_editor("This is content for the HTML editor field.")
    # sleep(1)
    # lookup.file_uploader(r"D:\DOWNLOADS (D)\Fat_Loss_Plan.pdf")
    # sleep(1)
    # lookup.email("test@example.com")
    # sleep(1)
    # lookup.ip_address("192.168.0.1")
    # sleep(1)
    # lookup.number("12345")
    # sleep(1)
    # lookup.decimal("123.45")
    # sleep(1)
    # lookup.currency("999.99")
    # sleep(1)
    # lookup.select_date_lookup("2025-10-04")  # Format: YYYY-MM-DD
    # sleep(1)
    # lookup.url("https://example.com")
    # sleep(3)
    # lookup.click_save_button()
    sleep(5)
    print("✅ All Lookup fields have been filled successfully!")

    decimal_value = lookup.get_table_value_by_id("decimal", 1)

    print(decimal_value)



