import pytest

from pages.login_page import LoginPage


class TestLoginPage:
    @pytest.mark.ui
    @pytest.mark.smoke_stable
    def test_login_page_loads(self, page, ui_base_url):
        login_page = LoginPage(page)

        login_page.open(ui_base_url)
        login_page.expect_loaded()

    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_flow(self, page, ui_base_url, common_user):
        login_page = LoginPage(page)

        login_page.open(ui_base_url)
        login_page.expect_loaded()

        login_page.fill_email(common_user.email)
        login_page.fill_password(common_user.password)
        login_page.click_sign_in_btn()

        login_page.expect_url_changed()
        login_page.expect_sign_in_btn_hidden()
