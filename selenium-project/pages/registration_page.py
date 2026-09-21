"""
Page Object Model for the Dashboard & Student Registration Page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    # Header & Navigation Locators
    LOGGED_USER = (By.ID, "loggedUsername")
    LOGOUT_BUTTON = (By.ID, "btnLogout")

    # Form Field Locators
    FULL_NAME_INPUT = (By.ID, "fullName")
    EMAIL_INPUT = (By.ID, "studentEmail")
    ROLL_NUMBER_INPUT = (By.ID, "rollNumber")
    AGE_INPUT = (By.ID, "age")
    PASSWORD_INPUT = (By.ID, "password")
    DEPARTMENT_DROPDOWN = (By.ID, "department")

    # Button Locators
    SUBMIT_BUTTON = (By.ID, "btnSubmit")
    CLEAR_BUTTON = (By.ID, "btnClear")

    # Feedback Alert Locators
    SUCCESS_ALERT = (By.ID, "alertSuccess")
    ERROR_ALERT = (By.ID, "alertError")

    # Table & Stats Locators
    TOTAL_STUDENTS_COUNT = (By.ID, "totalStudentsCount")
    STUDENTS_TABLE_ROWS = (By.CSS_SELECTOR, "#studentsTableBody tr")

    def is_at_dashboard(self, timeout=10):
        """Verify the user is on the dashboard page with explicit wait."""
        try:
            self.wait_for_url_contains("/dashboard", timeout=timeout)
            return self.is_element_visible(self.LOGGED_USER, custom_timeout=timeout)
        except Exception:
            return False

    def get_logged_username(self):
        """Retrieve logged-in user display text."""
        return self.get_text(self.LOGGED_USER)

    def logout(self):
        """Click sign-out button to end session."""
        self.click(self.LOGOUT_BUTTON)

    def fill_form(self, full_name=None, email=None, roll_number=None, age=None, password=None, department=None):
        """Populate the registration form fields."""
        if full_name is not None:
            self.send_keys(self.FULL_NAME_INPUT, str(full_name))
        if email is not None:
            self.send_keys(self.EMAIL_INPUT, str(email))
        if roll_number is not None:
            self.send_keys(self.ROLL_NUMBER_INPUT, str(roll_number))
        if age is not None:
            self.send_keys(self.AGE_INPUT, str(age))
        if password is not None:
            self.send_keys(self.PASSWORD_INPUT, str(password))
        if department is not None:
            self.select_dropdown_by_visible_text(self.DEPARTMENT_DROPDOWN, str(department))

    def submit(self):
        """Click the submit button to register student."""
        self.click(self.SUBMIT_BUTTON)

    def clear(self):
        """Click the clear form button."""
        self.click(self.CLEAR_BUTTON)

    def get_success_message(self):
        """Get the text of the success banner."""
        return self.get_text(self.SUCCESS_ALERT)

    def get_error_message(self):
        """Get the text of the error banner."""
        return self.get_text(self.ERROR_ALERT)

    def is_success_displayed(self):
        """Check if success banner is visible."""
        return self.is_element_visible(self.SUCCESS_ALERT)

    def is_error_displayed(self):
        """Check if error banner is visible."""
        return self.is_element_visible(self.ERROR_ALERT)

    def get_total_students_count(self):
        """Return numeric total from statistics card."""
        text = self.get_text(self.TOTAL_STUDENTS_COUNT)
        return int(text)

    def get_table_rows_count(self):
        """Return the number of rows currently in the students table."""
        rows = self.find_elements(self.STUDENTS_TABLE_ROWS)
        return len(rows)

    def get_field_value(self, locator):
        """Get current value of an input field."""
        element = self.find_element(locator)
        return element.get_attribute("value")
