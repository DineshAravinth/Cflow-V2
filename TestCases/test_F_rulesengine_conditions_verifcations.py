import pytest
from PageObjects.D_FormSubmission import FormSubmission
from PageObjects.F_rules_engine_condition_verification import rules_condition_verification
from BaseFiles.Basehelpers import BaseHelpers
from time import sleep


@pytest.mark.order(1)
class Test_001_rulesengine_conditions_verifications:

    def test_s1_equal_to(self, login, region):
        print("\n🔹 Starting S1 Equal To Rule Verification 🔹\n")

        driver = login
        base = BaseHelpers(driver)
        fs = FormSubmission(driver)
        rc = rules_condition_verification(driver)

        fs.open_workflow()
        sleep(3)
        base.verify_workflow_list_page()
        rc.click_workflow()
        sleep(2)
        fs.click_add_new_record()
        sleep(2)
        base.verify_form_page()
        sleep(2)

        rc.verify_text_rule(
            textbox_input_locator=rc.s1_textbox_input,
            rule_name="S1",
            negative_values=["aravinth", "testuser", "demo", "  "],
            positive_values=["dinesh"],
            positive_value_caps="DINESH",
            equal_to_value="dinesh"
        )
        sleep(3)
        print("\n🔹 Completed S1 Equal To Rule Verification 🔹\n")

    def test_s2_not_equal_to(self, login, region):
        print("\n🔹 Starting S2 Not Equal To Rule Verification 🔹\n")

        driver = login
        base = BaseHelpers(driver)
        fs = FormSubmission(driver)
        rc = rules_condition_verification(driver)

        fs.click_add_new_record()
        sleep(2)
        base.verify_form_page()
        sleep(2)

        rc.verify_text_rule(
            textbox_input_locator=rc.s2_textbox_input,
            rule_name="S2",
            negative_values=["dinesh", "DINESH", "  "],
            positive_values=["testuser", "demo"]
        )
        print("\n🔹 Completed S2 Not Equal To Rule Verification 🔹\n")

    def test_s3_numeric_rule(self, login):
        print("\n🔹 Starting S3 Less Than Verification 🔹\n")

        driver = login
        rc = rules_condition_verification(driver)
        fs = FormSubmission(driver)

        fs.click_add_new_record()

        rc.verify_numeric_rule(
            textbox_input_locator=rc.s3_textbox_int_input,
            rule_name="S3",
            comparison="<",
            negative_values=[50, 25, 5005],
            positive_values=[20, 0, -50]
        )
        print("\n🔹 Completed S3 Less Than Verification 🔹\n")

    def test_s4_numeric_rule(self, login):
        print("\n🔹 Starting S4 Less Than or Equal to Verification 🔹\n")

        driver = login
        rc = rules_condition_verification(driver)
        fs = FormSubmission(driver)

        fs.click_add_new_record()

        rc.verify_numeric_rule(
            textbox_input_locator=rc.s4_textbox_int_input,
            rule_name="S4",
            comparison="<=",
            negative_values=[50, 100, 5005],
            positive_values=[25, 20, 0, -10]
        )
        print("\n🔹 Completed S4 Less Than or Equal to Verification 🔹\n")

    def test_s5_numeric_rule(self, login):
        print("\n🔹 Starting S5 Greater Than Verification 🔹\n")

        driver = login
        rc = rules_condition_verification(driver)
        fs = FormSubmission(driver)

        fs.click_add_new_record()

        rc.verify_numeric_rule(
            textbox_input_locator=rc.s5_textbox_int_input,
            rule_name="S5",
            comparison=">",
            negative_values=[25, 20, 0, -10],
            positive_values=[51, 500, 555]
        )
        print("\n🔹 Completed S5 Greater Than Verification 🔹\n")

    def test_s6_numeric_rule(self, login):
        print("\n🔹 Starting S6 Greater Than or Equal to Verification 🔹\n")

        driver = login
        rc = rules_condition_verification(driver)
        fs = FormSubmission(driver)

        fs.click_add_new_record()

        rc.verify_numeric_rule(
            textbox_input_locator=rc.s6_textbox_int_input,
            rule_name="S6",
            comparison=">=",
            negative_values=[20, 0, -10],
            positive_values=[50, 51, 1000]
        )
        print("\n🔹 Completed S6 Greater Than or Equal to Verification 🔹\n")
