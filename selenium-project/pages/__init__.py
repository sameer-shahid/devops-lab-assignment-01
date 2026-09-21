"""Pages package for Selenium Page Object Model."""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage

__all__ = ["BasePage", "LoginPage", "RegistrationPage"]
