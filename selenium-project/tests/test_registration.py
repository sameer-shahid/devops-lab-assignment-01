"""
Test Suite: Student Registration & Dashboard Automation Tests.
Tests valid submission, mandatory validations (empty fields, email regex,
password length, numeric bounds, dropdown selection), form clear, and navigation.
"""
import os
import csv
import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage

@pytest.fixture
def logged_in_dashboard(driver, base_url):
    """Helper fixture to log in and navigate to dashboard prior to tests."""
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)

    login_page.open(base_url)
    login_page.login("admin", "Admin@123")
    assert registration_page.is_at_dashboard(), "Prerequisite failed: Not on dashboard!"
    return registration_page


class TestRegistration:

    @pytest.mark.smoke
    def test_successful_student_registration(self, logged_in_dashboard):
        """TC-REG-01: Verify valid student registration completes with success alert and table update."""
        reg_page = logged_in_dashboard
        initial_count = reg_page.get_total_students_count()
        initial_rows = reg_page.get_table_rows_count()

        # Fill all 5 fields and dropdown with valid inputs
        reg_page.fill_form(
            full_name="Sameer Ahmed",
            email="sp23-bse-128@cuilahore.edu.pk",
            roll_number="SP23-BSE-128",
            age="21",
            password="StrongPassword@2026",
            department="Software Engineering"
        )
        reg_page.submit()

        # Assertion 1: Success alert is displayed
        assert reg_page.is_success_displayed(), "Success message was not displayed!"
        success_msg = reg_page.get_success_message()
        assert "Sameer Ahmed" in success_msg
        assert "successfully registered" in success_msg.lower()

        # Assertion 2: Student count incremented
        new_count = reg_page.get_total_students_count()
        assert new_count == initial_count + 1, f"Expected count {initial_count + 1}, got {new_count}"

        # Assertion 3: Table row count incremented
        new_rows = reg_page.get_table_rows_count()
        assert new_rows == initial_rows + 1

        reg_page.take_screenshot("TC_REG_01_Registration_Success")

    def test_empty_fields_validation(self, logged_in_dashboard):
        """TC-REG-02: Mandatory Validation 1 - Verify empty form submission shows validation error."""
        reg_page = logged_in_dashboard

        # Click submit with all fields empty
        reg_page.submit()

        assert reg_page.is_error_displayed(), "Error banner was not shown on empty form submission!"
        error_text = reg_page.get_error_message()
        assert "mandatory" in error_text.lower() or "required" in error_text.lower()

        reg_page.take_screenshot("TC_REG_02_EmptyFields_Validation")

    def test_invalid_email_validation(self, logged_in_dashboard):
        """TC-REG-03: Mandatory Validation 2 - Verify invalid email format shows error."""
        reg_page = logged_in_dashboard

        reg_page.fill_form(
            full_name="Test Student",
            email="invalid-email-address-no-at",
            roll_number="FA23-BCS-999",
            age="22",
            password="ValidPassword@123",
            department="Computer Science"
        )
        reg_page.submit()

        assert reg_page.is_error_displayed(), "Error banner was not shown for invalid email!"
        error_text = reg_page.get_error_message()
        assert "valid email" in error_text.lower()

        reg_page.take_screenshot("TC_REG_03_InvalidEmail_Validation")

    def test_password_length_validation(self, logged_in_dashboard):
        """TC-REG-04: Mandatory Validation 3 - Verify password shorter than 8 characters shows error."""
        reg_page = logged_in_dashboard

        reg_page.fill_form(
            full_name="Test Student",
            email="test@cuilahore.edu.pk",
            roll_number="FA23-BCS-999",
            age="22",
            password="123",  # Only 3 characters
            department="Computer Science"
        )
        reg_page.submit()

        assert reg_page.is_error_displayed(), "Error banner was not shown for short password!"
        error_text = reg_page.get_error_message()
        assert "8 characters" in error_text.lower()

        reg_page.take_screenshot("TC_REG_04_ShortPassword_Validation")

    def test_invalid_numeric_age_validation(self, logged_in_dashboard):
        """TC-REG-05: Mandatory Validation 4 - Verify out-of-range age (<16 or >60) shows error."""
        reg_page = logged_in_dashboard

        reg_page.fill_form(
            full_name="Out Range Student",
            email="outofrange@cuilahore.edu.pk",
            roll_number="SP23-BAI-100",
            age="95",  # Invalid age (> 60)
            password="ValidPassword@123",
            department="Artificial Intelligence"
        )
        reg_page.submit()

        assert reg_page.is_error_displayed(), "Error banner was not shown for invalid numeric age!"
        error_text = reg_page.get_error_message()
        assert "between 16 and 60" in error_text.lower()

        reg_page.take_screenshot("TC_REG_05_InvalidAge_Validation")

    def test_required_dropdown_selection(self, logged_in_dashboard):
        """TC-REG-06: Mandatory Validation 5 - Verify unselected department dropdown shows error."""
        reg_page = logged_in_dashboard

        # Populate all fields except department dropdown
        reg_page.fill_form(
            full_name="Dropdown Tester",
            email="dropdown@cuilahore.edu.pk",
            roll_number="SP23-BCY-050",
            age="20",
            password="ValidPassword@123"
        )
        reg_page.submit()

        assert reg_page.is_error_displayed(), "Error banner was not shown for unselected dropdown!"
        error_text = reg_page.get_error_message()
        assert "department" in error_text.lower()

        reg_page.take_screenshot("TC_REG_06_DropdownRequired_Validation")

    def test_clear_form_button(self, logged_in_dashboard):
        """TC-REG-07: Verify Clear Form button resets all input fields."""
        reg_page = logged_in_dashboard

        # Populate form
        reg_page.fill_form(
            full_name="Temporary Name",
            email="temp@cuilahore.edu.pk",
            roll_number="SP23-BSE-999",
            age="24",
            password="TemporaryPassword@123",
            department="Software Engineering"
        )

        # Click Clear Form
        reg_page.clear()

        # Assert fields are now empty
        assert reg_page.get_field_value(reg_page.FULL_NAME_INPUT) == ""
        assert reg_page.get_field_value(reg_page.EMAIL_INPUT) == ""
        assert reg_page.get_field_value(reg_page.ROLL_NUMBER_INPUT) == ""
        assert reg_page.get_field_value(reg_page.AGE_INPUT) == ""
        assert reg_page.get_field_value(reg_page.PASSWORD_INPUT) == ""

    def test_logout_navigation(self, logged_in_dashboard, driver):
        """TC-REG-08: Verify Sign Out button successfully navigates back to /login page."""
        reg_page = logged_in_dashboard
        login_page = LoginPage(driver)

        reg_page.logout()

        # Assert redirected back to /login
        assert "/login" in driver.current_url
        assert login_page.is_element_visible(login_page.USERNAME_INPUT)

        reg_page.take_screenshot("TC_REG_08_LogoutNavigation_Success")


class TestDataDrivenRegistration:

    def test_csv_data_driven_registration(self, logged_in_dashboard):
        """TC-REG-09: Data-Driven test executing cases loaded from test_data/users.csv."""
        reg_page = logged_in_dashboard
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_data", "users.csv"))

        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                case_name = row["test_case"]
                expected_status = row["expected_status"]
                expected_msg = row["expected_message_contains"]

                # Clear previous state
                reg_page.clear()

                # Fill data
                reg_page.fill_form(
                    full_name=row["fullName"] or None,
                    email=row["studentEmail"] or None,
                    roll_number=row["rollNumber"] or None,
                    age=row["age"] or None,
                    password=row["password"] or None,
                    department=row["department"] or None
                )
                reg_page.submit()

                if expected_status == "SUCCESS":
                    assert reg_page.is_success_displayed(), f"[{case_name}] Expected success alert!"
                    assert expected_msg.lower() in reg_page.get_success_message().lower()
                else:
                    assert reg_page.is_error_displayed(), f"[{case_name}] Expected error alert!"
                    assert expected_msg.lower() in reg_page.get_error_message().lower()
