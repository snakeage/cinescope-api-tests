from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = '/login'

    def expect_loaded(self):
        expect(self.page.get_by_role('heading', name='Войти', level=2)).to_be_visible()
        expect(self.page.get_by_label('Email')).to_be_visible()
        expect(self.page.get_by_label('Пароль')).to_be_visible()
        expect(self.page.locator('form').get_by_role('button', name='Войти')).to_be_visible()
        expect(self.page.get_by_role('link', name='Зарегистрироваться')).to_be_visible()

    def fill_email(self, email):
        self.page.get_by_label('Email').fill(email)

    def fill_password(self, password):
        self.page.get_by_label('Пароль').fill(password)

    def click_sign_in_btn(self):
        self.page.locator('form').get_by_role('button', name='Войти').click()

    def expect_url_changed(self):
        expect(self.page).not_to_have_url('**/login')

    def expect_sign_in_btn_hidden(self):
        expect(self.page.locator('form').get_by_role('button', name='Войти')).not_to_be_visible()

    def expect_error_toaster_is_visible(self):
        expect(self.page.get_by_text('Неверная почта или пароль', exact=True)).to_be_visible()
