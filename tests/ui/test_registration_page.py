import allure
import pytest

from pages.registration_page import RegistrationPage


@allure.title('Registration page loads')
@allure.description('Checks that the registration page renders the main form elements.')
@pytest.mark.ui
@pytest.mark.smoke_stable
def test_registration_page_loads(page, ui_base_url):
    registration_page = RegistrationPage(page)

    with allure.step('Open registration page'):
        registration_page.open(ui_base_url)

    with allure.step('Verify registration page is loaded'):
        registration_page.expect_loaded()
