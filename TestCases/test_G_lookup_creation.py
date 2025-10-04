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
    lookup.click_create_lookup()
    sleep(2)
    unique_lookup_name = lookup.enter_unique_lookup_name()
    sleep(2)
    lookup.click_create_lookup_name()
    sleep(2)
    lookup.click_add_field_button()

    # List of fields to add: (display_name, field_type, valid_values)
    fields_to_add = [
        ("TextBox", "TextBox", None),
        ("CheckBox", "CheckBox", None),
        ("CheckBox List", "CheckBox List", ["A", "B", "C", "D"]),
        ("Radio Button List", "Radio Button List", ["A", "B", "C", "D"]),
        ("TextBox MultiLine", "TextBox MultiLine", None),
        ("DropDown List", "DropDownList", ["A", "B", "C", "D"]),
        ("MS DropDown List", "MS DropDownList", ["A", "B", "C", "D"]),
        ("HTML Editor", "HTML Editor", None),
        ("File", "File", None),
        ("Email", "Email", None),
        ("IP Address", "IP Address", None),
        ("Number", "Number", None),
        ("Decimal", "Decimal", None),
        ("Identity", "Identity", None),
        ("Currency", "Currency", None),
        ("Date", "Date", None),
        ("URL", "URL", None)
    ]

    # Loop through each field and add
    for index, (display_name, field_type, valid_values) in enumerate(fields_to_add):
        # Only click "Add Field" if it's not the first field
        click_add_field = True if index < len(fields_to_add) - 1 else False
        lookup.add_field(display_name=display_name, field_type=field_type, valid_values=valid_values, click_add_field=click_add_field)
        sleep(2)

    # Publish the lookup at the end
    lookup.click_publish_lookup()
    sleep(2)
    print(f"✅ Lookup '{unique_lookup_name}' created with all fields successfully.")
