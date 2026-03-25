import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.regression
def test_login_negative(page, common_user):
    page.goto('https://dev-cinescope.coconutqa.ru/login')

    expect(page.get_by_role('heading', name='Войти', level=2)).to_be_visible()

    page.get_by_label('Email').fill(common_user.email)
    page.get_by_label('Пароль').fill('invalid_password_123!')
    sign_in_btn_form = page.locator('form').get_by_role('button', name='Войти')
    sign_in_btn_form.click()

    expect(page.get_by_text('Неверная почта или пароль', exact=True)).to_be_visible()
