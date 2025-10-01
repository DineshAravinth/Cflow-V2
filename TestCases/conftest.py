
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

# PageObjects + Utilities
from PageObjects.A_loginpage import LoginPage
from Utilities.readProperties import ReadConfig


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
def setup(browser):
    """Setup WebDriver once per session"""
    driver = None
    print(f"Starting browser setup: {browser}")

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
    yield driver  # no quit here, browser stays open


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

        lp = LoginPage(driver)
        lp.setClientid(client_id)
        lp.setUserName(username)
        lp.setPassword(password)
        lp.clickLogin()
        sleep(3)
        print("✅ Logged in successfully")

    except Exception as e:
        print(f"❌ Login failed: {e}")
        driver = None

    yield driver  # browser remains open


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
