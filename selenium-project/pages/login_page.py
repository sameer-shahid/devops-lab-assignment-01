"""
Page Object Model for the Login Page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "btnLogin")
    ERROR_ALERT = (By.ID, "loginError")

    def open(self, base_url):
        """Navigate to the login page."""
        url = f"{base_url.rstrip('/')}/login"
        self.driver.get(url)

    def enter_username(self, username):
        """Type username into the username field."""
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Type password into the password field."""
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click the sign-in button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Convenience method to execute full login flow."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Retrieve the text from the error alert."""
        return self.get_text(self.ERROR_ALERT)

    def is_error_displayed(self):
        """Check if the error banner is displayed."""
        return self.is_element_visible(self.ERROR_ALERT)
