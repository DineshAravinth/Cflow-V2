import pytest
from PageObjects.A_loginpage import LoginPage


class Test_001_Login:

    def test_homepage(self, login, region):

        driver = login  # logged-in driver from fixture
        lp = LoginPage(driver)



