import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from time import sleep
from BaseFiles.Basehelpers import BaseHelpers
from selenium.webdriver.common.by import By

# PageObjects + Utilities
from PageObjects.A_loginpage import LoginPage
from Utilities.readProperties import ReadConfig


# ---------- Pytest CLI Options ----------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome/firefox/edge"
    )
    parser.addoption(
        "--region",
        action="store",
        default="AP",
        help="Region to run tests on: AP/ME/US/EU"
    )


# ---------- Browser Fixture ----------
@pytest.fixture(scope="session")
def browser(request):
    """Get browser name from CLI"""
    return request.config.getoption("--browser")


# ---------- Region Fixture ----------
@pytest.fixture(scope="session")
def region(request):
    """Get region from CLI"""
    return request.config.getoption("--region")


# ---------- Setup Fixture ----------
@pytest.fixture(scope="session")
def setup(browser, region):
    """Setup WebDriver once per session and verify login URL"""
    driver = None
    print(f"Starting browser setup: {browser} | Region: {region}")

    if browser.lower() == "chrome":
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Prevent auto-close
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif browser.lower() == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    elif browser.lower() == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)

    else:
        raise ValueError(f"Browser '{browser}' not supported!")

    driver.maximize_window()
    print("✅ Browser launched successfully")

    # Initialize BaseHelpers for verification
    base = BaseHelpers(driver)

    # Navigate to login page
    login_url = f"https://{region.lower()}.cflowapps.com/cflow/login"
    driver.get(login_url)

    # ✅ Verify Login URL
    base.verify_page_url(login_url, f"verify_login_url_{region}")

    yield driver  # browser stays open after tests


# ---------- Login Fixture ----------
@pytest.fixture(scope="session")
def login(setup, region):
    """Login once per session and return logged-in driver"""
    driver = setup

    try:
        url = ReadConfig.getURL(region)
        client_id = ReadConfig.getClientID(region)
        username = ReadConfig.getUsername(region)
        password = ReadConfig.getPassword(region)

        print(f"Navigating to URL: {url} for region: {region}")
        driver.get(url)
        sleep(2)

        # Initialize LoginPage object
        lp = LoginPage(driver)

        # Enter credentials
        lp.setClientid(client_id)
        lp.setUserName(username)
        lp.setPassword(password)

        # Click Login
        lp.clickLogin()
        sleep(3)

        # Verify Dashboard page
        base = BaseHelpers(driver)
        base.verify_page_by_element(
            (By.XPATH, "//p[contains(.,'Dashboard')]"),
            method_name=f"verify_dashboard_after_login_{region}"
        )

        print("✅ Logged in successfully")

    except Exception as e:
        print(f"❌ Login failed: {e}")
        driver = None

    yield driver  # logged-in driver for tests
