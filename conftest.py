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
from datetime import datetime
from py.xml import html


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
        base.verify_dashboard_page()

    except Exception as e:
        print(f"❌ Login failed: {e}")
        driver = None

    yield driver  # logged-in driver for tests


# conftest.py (root folder)
  # required for pytest-html v3.x

# ---------- Set HTML report title ----------
@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "🚀 Cflow Automation Test Report"

# ---------- Custom attractive single-line environment info ----------
@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    """Custom attractive single-line environment info styled as a status bar"""
    timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    # CLI info or defaults
    projectname = "Cflow Automation 🏆"
    modulename = "Workflow Creation and Submission"
    tester = "Dinesh Aravinth ⚡"
    browser = "chrome"
    region = "ME"

    # Status bar row style
    style = (
        "background: linear-gradient(90deg, #e0f7fa, #b2ebf2);"
        "padding:10px 14px;"  # slightly larger padding
        "border-radius:8px;"
        "font-family:Arial, sans-serif;"
        "font-size:18px;"  # increased from 18px to 20px
        "color:#000;"
        "display:flex;"
        "align-items:center;"
    )

    # Separator style
    separator_style = "margin:0 10px; font-weight:bold; color:#555;"

    metadata_html = html.tr([
        html.td([
            html.span("📝 Project Name: ", style="font-weight:bold; color:#1976d2;"),
            html.span(projectname, style="font-weight:800; color:#1976d2;"),
            html.span(" | ", style=separator_style),

            html.span("📂 Module Name: ", style="font-weight:bold; color:#388e3c;"),
            html.span(modulename, style="font-weight:800; color:#388e3c;"),
            html.span(" | ", style=separator_style),

            html.span("👤 Tester: ", style="font-weight:bold; color:#f57c00;"),
            html.span(tester, style="font-weight:800; color:#f57c00;"),
            html.span(" | ", style=separator_style),

            html.span("🌐 Browser: ", style="font-weight:bold; color:#00796b;"),
            html.span(browser, style="font-weight:800; color:#00796b;"),
            html.span(" | ", style=separator_style),

            html.span("🌍 Region: ", style="font-weight:bold; color:#512da8;"),
            html.span(region, style="font-weight:800; color:#512da8;"),
            html.span(" | ", style=separator_style),

            html.span("⏰ Execution Time: ", style="font-weight:bold; color:#d32f2f;"),
            html.span(timestamp, style="font-weight:800; color:#d32f2f;")
        ], style=style)
    ])

    prefix.append(metadata_html)

