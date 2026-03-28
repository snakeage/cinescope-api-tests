import allure
import pytest

from pages.login_page import LoginPage


@allure.title('Login flow: invalid password')
@allure.description(
    'Attempts to sign in with a valid email and invalid password and expects an error.'
)
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_login_negative(page, ui_base_url, common_user):
    login_page = LoginPage(page)

    with allure.step('Open login page'):
        login_page.open(ui_base_url)

    with allure.step('Verify login page is loaded'):
        login_page.expect_loaded()

    with allure.step('Fill valid email and invalid password'):
        login_page.fill_email(common_user.email)
        login_page.fill_password('invalid_password_123!')

    with allure.step('Submit login form'):
        login_page.click_sign_in_btn()

    with allure.step('Verify error message is shown'):
        login_page.expect_error_toaster_is_visible()
