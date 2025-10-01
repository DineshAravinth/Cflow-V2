
from selenium.webdriver.common.by import By

class LoginPage:
    textbox_clientid = "client-id"
    textbox_username = "username"
    textbox_password = "password"
    button_login = "//button[contains(.,'Login')]"

    def __init__(self, driver):
        self.driver = driver

    def setClientid(self, client_id):
        self.driver.find_element(By.ID, self.textbox_clientid).clear()
        self.driver.find_element(By.ID, self.textbox_clientid).send_keys(client_id)

    def setUserName(self, username):
        self.driver.find_element(By.ID, self.textbox_username).clear()
        self.driver.find_element(By.ID, self.textbox_username).send_keys(username)

    def setPassword(self, password):
        self.driver.find_element(By.ID, self.textbox_password).clear()
        self.driver.find_element(By.ID, self.textbox_password).send_keys(password)

    def clickLogin(self):
        self.driver.find_element(By.XPATH, self.button_login).click()
