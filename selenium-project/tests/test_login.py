"""
Test Suite: Authentication & Login Page Automation Tests.
Tests valid login, invalid credentials, and boundary input scenarios.
"""
import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage

class TestLogin:

    @pytest.mark.smoke
    def test_valid_admin_login(self, driver, base_url):
        """TC-LOG-01: Verify successful login with valid admin credentials."""
        login_page = LoginPage(driver)
        registration_page = RegistrationPage(driver)

        login_page.open(base_url)
        login_page.login("admin", "Admin@123")

        # Assertion 1: Verify redirect to dashboard
        assert registration_page.is_at_dashboard(), "User was not redirected to /dashboard upon valid login!"
        
        # Assertion 2: Verify active user badge displays logged username
        assert "admin" in registration_page.get_logged_username().lower()

        # Capture proof screenshot
        login_page.take_screenshot("TC_LOG_01_ValidLogin_Success")

    def test_valid_student_login(self, driver, base_url):
        """TC-LOG-02: Verify successful login with secondary valid student credentials."""
        login_page = LoginPage(driver)
        registration_page = RegistrationPage(driver)

        login_page.open(base_url)
        login_page.login("student", "Student@123")

        assert registration_page.is_at_dashboard(), "Student user was not redirected to /dashboard!"
        assert "student" in registration_page.get_logged_username().lower()

    def test_invalid_password(self, driver, base_url):
        """TC-LOG-03: Verify error message when logging in with incorrect password."""
        login_page = LoginPage(driver)

        login_page.open(base_url)
        login_page.login("admin", "WrongPassword999")

        # Assertion: Verify error banner is visible and has correct message
        assert login_page.is_error_displayed(), "Error banner was not displayed for invalid password!"
        error_text = login_page.get_error_message()
        assert "Invalid username or password" in error_text, f"Unexpected error text: '{error_text}'"

        login_page.take_screenshot("TC_LOG_03_InvalidPassword_Error")

    def test_invalid_username(self, driver, base_url):
        """TC-LOG-04: Verify error message when logging in with non-existent username."""
        login_page = LoginPage(driver)

        login_page.open(base_url)
        login_page.login("unknown_user", "AnyPassword@123")

        assert login_page.is_error_displayed(), "Error banner was not displayed for non-existent user!"
        assert "Invalid username or password" in login_page.get_error_message()

    def test_empty_credentials(self, driver, base_url):
        """TC-LOG-05: Verify error message when attempting to submit blank login fields."""
        login_page = LoginPage(driver)

        login_page.open(base_url)
        # Using JS form submit to bypass HTML5 native popup if needed
        driver.execute_script("document.getElementById('loginForm').submit();")

        assert login_page.is_error_displayed(), "Error banner was not displayed for empty credentials!"
        error_text = login_page.get_error_message()
        assert "cannot be empty" in error_text.lower() or "invalid" in error_text.lower()
