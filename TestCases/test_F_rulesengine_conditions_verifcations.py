import pytest
from PageObjects.D_FormSubmission import FormSubmission
from PageObjects.F_rules_engine_condition_verification import rules_condition_verification
from BaseFiles.Basehelpers import BaseHelpers
from time import sleep

@pytest.mark.order(1)
class Test_001_rulesengine_conditions_verifications:

    def test_s1_equal_to(self, login, region):

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
        rc.verify_equal_to_rule_s1()
