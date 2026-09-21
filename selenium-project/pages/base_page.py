"""
Base Page Object containing reusable methods and explicit waits.
"""
import os
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

logger = logging.getLogger("SeleniumAutomation")

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        """Wait for element to be present and visible before returning."""
        logger.info(f"Waiting for element: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """Wait for elements to be present."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Wait for element to be clickable and click it."""
        logger.info(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text, clear_first=True):
        """Send keystrokes to an input element."""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        logger.info(f"Typing text into {locator}")
        element.send_keys(text)

    def get_text(self, locator):
        """Get element inner text."""
        element = self.find_element(locator)
        return element.text.strip()

    def select_dropdown_by_visible_text(self, locator, text):
        """Select an option from a <select> dropdown by visible text."""
        logger.info(f"Selecting '{text}' from dropdown: {locator}")
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def is_element_visible(self, locator, custom_timeout=3):
        """Check if an element is visible within a custom timeout."""
        try:
            WebDriverWait(self.driver, custom_timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, fragment, timeout=10):
        """Wait until current URL contains fragment."""
        logger.info(f"Waiting for URL to contain: '{fragment}'")
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))

    def get_current_url(self):
        """Get current browser URL."""
        return self.driver.current_url

    def take_screenshot(self, name_prefix="screenshot"):
        """Save a screenshot in the screenshots directory."""
        screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name_prefix}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
