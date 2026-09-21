"""
Pytest configuration, fixtures, and hooks for Selenium test suite.
"""
import os
import sys
import logging
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Setup logging to both file and console
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "automation.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SeleniumAutomation")


def pytest_addoption(parser):
    """Add custom command line arguments."""
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run browser in headless mode: true or false (default: true)"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=os.environ.get("BASE_URL", "http://127.0.0.1:5000"),
        help="Base URL of the web application (default: http://127.0.0.1:5000)"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Fixture providing the target application URL, with port auto-detection."""
    url = request.config.getoption("--base-url")
    if url == "http://127.0.0.1:5000" and "BASE_URL" not in os.environ:
        import socket
        # If 5000 is not active or 5001 is active
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # Try port 5001 if 5001 is open
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s2.settimeout(0.5)
                if s2.connect_ex(('127.0.0.1', 5001)) == 0:
                    url = "http://127.0.0.1:5001"
    logger.info(f"Target Base URL: {url}")
    return url


@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes Chrome WebDriver with robust options for both
    local execution and AWS Windows EC2 / CI environments.
    """
    headless_opt = request.config.getoption("--headless").lower()
    is_headless = headless_opt in ("true", "1", "yes")

    chrome_options = Options()
    if is_headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--remote-allow-origins=*")

    logger.info(f"Launching Chrome (Headless: {is_headless})...")
    
    # Try native Selenium 4 driver manager, fallback to ChromeDriverManager
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logger.warning(f"Native Selenium manager failed ({e}), falling back to ChromeDriverManager...")
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.maximize_window()
    driver.implicitly_wait(3)

    yield driver

    # Teardown logic
    try:
        # Check if test failed, capture failure screenshot
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshots_dir = os.path.join(PROJECT_ROOT, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FAIL_{request.node.name}_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)
            driver.save_screenshot(filepath)
            logger.error(f"Test failed! Screenshot captured: {filepath}")
    except Exception as err:
        logger.warning(f"Could not take teardown screenshot: {err}")
    finally:
        logger.info("Quitting Chrome WebDriver session.")
        driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcome for fixtures to inspect failure state."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_html_report_title(report):
    """Customize pytest-html report title."""
    report.title = "DevOps Lab 1 - Selenium Test Automation Report (CUI Lahore)"


def pytest_configure(config):
    """Add environment metadata to HTML report."""
    if hasattr(config, "_metadata"):
        config._metadata["Course"] = "CSC418: DevOps for Cloud Computing"
        config._metadata["Assignment"] = "Lab Assignment 1 (Part C: Selenium Automation)"
        config._metadata["Campus"] = "COMSATS University Islamabad, Lahore Campus"
        config._metadata["Target Host"] = "AWS Windows Server EC2 / Localhost"
        config._metadata["Framework"] = "Page Object Model (POM) + Pytest"
