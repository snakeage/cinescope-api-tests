import pytest

from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_login_negative(page, ui_base_url, common_user):
    login_page = LoginPage(page)

    login_page.open(ui_base_url)
    login_page.expect_loaded()

    login_page.fill_email(common_user.email)
    login_page.fill_password('invalid_password_123!')
    login_page.click_sign_in_btn()

    login_page.expect_error_toaster_is_visible()
