from BaseFiles.Basehelpers import BaseHelpers
from selenium.webdriver.common.by import By

class LoginPage(BaseHelpers):
    textbox_clientid = "client-id"
    textbox_username = "username"
    textbox_password = "password"
    button_login = "//button[contains(.,'Login')]"

    def __init__(self, driver, timeout=30):
        super().__init__(driver, timeout)  # initialize BaseHelpers


    def setClientid(self, client_id):
        self.enter_text(f"//input[@id='{self.textbox_clientid}']", client_id, "Client ID")

    def setUserName(self, username):
        self.enter_text(f"//input[@id='{self.textbox_username}']", username, "Username")

    def setPassword(self, password):
        self.enter_text(f"//input[@id='{self.textbox_password}']", password, "Password")

    def clickLogin(self):
        self.click(self.button_login, "Login Button")
