import allure
import pytest

from pages.login_page import LoginPage


class TestLoginPage:
    @allure.title('Login page loads')
    @allure.description('Checks that the login page renders the main form elements.')
    @pytest.mark.ui
    @pytest.mark.smoke_stable
    def test_login_page_loads(self, page, ui_base_url):
        login_page = LoginPage(page)

        with allure.step('Open login page'):
            login_page.open(ui_base_url)

        with allure.step('Verify login page is loaded'):
            login_page.expect_loaded()

    @allure.title('Login flow: successful sign in')
    @allure.description('Signs in with an API-created user and verifies the login page is left.')
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_flow(self, page, ui_base_url, common_user):
        login_page = LoginPage(page)

        with allure.step('Open login page'):
            login_page.open(ui_base_url)

        with allure.step('Verify login page is loaded'):
            login_page.expect_loaded()

        with allure.step('Fill valid credentials'):
            login_page.fill_email(common_user.email)
            login_page.fill_password(common_user.password)

        with allure.step('Submit login form'):
            login_page.click_sign_in_btn()

        with allure.step('Verify login was successful'):
            login_page.expect_url_changed()
            login_page.expect_sign_in_btn_hidden()
