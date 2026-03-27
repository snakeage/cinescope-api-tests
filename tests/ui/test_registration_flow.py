from pages.registration_page import RegistrationPage
from utils.data_generator import DataGenerator


def test_registration_flow(page, ui_base_url):
    registration_page = RegistrationPage(page)

    registration_page.open(ui_base_url)
    registration_page.expect_loaded()

    full_name = DataGenerator.generate_random_name()
    registration_page.fill_full_name(full_name)

    email = DataGenerator.generate_random_email()
    registration_page.fill_email(email)

    password = DataGenerator.generate_random_password()
    registration_page.fill_password(password)
    registration_page.fill_repeat_password(password)

    registration_page.click_signup_btn()

    registration_page.expect_url_changed()
    registration_page.expect_confirmation_message_visible()
    registration_page.expect_signup_button_hidden()
