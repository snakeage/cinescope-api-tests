import allure
import pytest

from pages.registration_page import RegistrationPage
from utils.data_generator import DataGenerator


@allure.title('Registration flow: successful sign up')
@allure.description('Registers a new user with generated data and verifies the success state.')
@pytest.mark.ui
@pytest.mark.regression
def test_registration_flow(page, ui_base_url):
    registration_page = RegistrationPage(page)

    with allure.step('Open registration page'):
        registration_page.open(ui_base_url)

    with allure.step('Verify registration page is loaded'):
        registration_page.expect_loaded()

    with allure.step('Fill registration form'):
        full_name = DataGenerator.generate_random_name()
        email = DataGenerator.generate_random_email()
        password = DataGenerator.generate_random_password()

        registration_page.fill_full_name(full_name)
        registration_page.fill_email(email)
        registration_page.fill_password(password)
        registration_page.fill_repeat_password(password)

    with allure.step('Submit registration form'):
        registration_page.click_signup_btn()

    with allure.step('Verify registration was successful'):
        registration_page.expect_url_changed()
        registration_page.expect_confirmation_message_visible()
        registration_page.expect_signup_button_hidden()
