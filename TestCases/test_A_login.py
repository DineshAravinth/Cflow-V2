import pytest
from PageObjects.A_loginpage import LoginPage
from Utilities.readProperties import ReadConfig
from time import sleep


class Test_001_Login:

    def test_homepage(self, setup, region):
        driver = setup

        # Read credentials based on region fixture
        url = ReadConfig.getURL(region)
        client_id = ReadConfig.getClientID(region)
        username = ReadConfig.getUsername(region)
        password = ReadConfig.getPassword(region)

        driver.get(url)
        sleep(2)

        lp = LoginPage(driver)
        lp.setClientid(client_id)
        lp.setUserName(username)
        lp.setPassword(password)
        lp.clickLogin()
