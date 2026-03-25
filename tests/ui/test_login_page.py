import pytest
from playwright.sync_api import expect


class TestLoginPage:
    @pytest.mark.ui
    @pytest.mark.smoke_stable
    def test_login_page_loads(self, page):
        page.goto('https://dev-cinescope.coconutqa.ru/login')

        expect(page.get_by_role('heading', name='Войти', level=2)).to_be_visible()
        expect(page.get_by_label('Email')).to_be_visible()
        expect(page.get_by_label('Пароль')).to_be_visible()
        expect(page.locator('form').get_by_role('button', name='Войти')).to_be_visible()
        expect(page.get_by_role('link', name='Зарегистрироваться')).to_be_visible()

    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_flow(self, page, common_user):
        page.goto('https://dev-cinescope.coconutqa.ru/login')

        expect(page.get_by_role('heading', name='Войти', level=2)).to_be_visible()

        page.get_by_label('Email').fill(common_user.email)
        page.get_by_label('Пароль').fill(common_user.password)
        sign_in_btn_form = page.locator('form').get_by_role('button', name='Войти')
        sign_in_btn_form.click()

        expect(page).not_to_have_url('**/login')
        expect(sign_in_btn_form).not_to_be_visible()
