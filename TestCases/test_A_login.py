import pytest
from PageObjects.A_loginpage import LoginPage
from Utilities.readProperties import ReadConfig
from time import sleep
from selenium.webdriver.common.by import By

class Test_001_Login:

    def test_homepage(self, setup, region):

        driver = setup

        # Read credentials based on region fixture
        url = ReadConfig.getURL(region)
        client_id = ReadConfig.getClientID(region)
        username = ReadConfig.getUsername(region)
        password = ReadConfig.getPassword(region)

        # Open the login page
        driver.get(url)
        sleep(2)

        # Initialize LoginPage object
        lp = LoginPage(driver)

        # Verify Loginpage URL
        lp.verify_page_url(
            expected_url_part=f"https://{region.lower()}.cflowapps.com/cflow/login",
            method_name=f"verify_loginpage_url_{region.lower()}")

        # Enter credentials
        lp.setClientid(client_id)
        lp.setUserName(username)
        lp.setPassword(password)

        # Click Login Button
        lp.clickLogin()
        sleep(5)

        # Click Verify Dashboard Page
        lp.verify_page_by_element(
            element_locator=(By.XPATH, "//p[contains(.,'Dashboard')]"),
            method_name=f"verify_dashboard_page")


