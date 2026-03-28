from playwright.sync_api import expect

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    PATH = '/register'

    def expect_loaded(self):
        expect(self.page.get_by_role('heading', name='Регистрация', level=2)).to_be_visible()
        expect(self.page.get_by_placeholder('Имя Фамилия Отчество')).to_be_visible()
        expect(self.page.get_by_placeholder('Email')).to_be_visible()
        expect(self.page.get_by_placeholder('Пароль', exact=True)).to_be_visible()
        expect(self.page.get_by_placeholder('Повторите пароль')).to_be_visible()
        expect(
            self.page.locator('form').get_by_role(
                'button',
                name='Зарегистрироваться',
            )
        ).to_be_visible()
        expect(self.page.locator('form').get_by_role('link', name='Войти')).to_be_visible()

    def fill_full_name(self, full_name):
        self.page.get_by_placeholder('Имя Фамилия Отчество').fill(full_name)

    def fill_email(self, email):
        self.page.get_by_placeholder('Email').fill(email)

    def fill_password(self, password):
        self.page.get_by_placeholder('Пароль', exact=True).fill(password)

    def fill_repeat_password(self, password):
        self.page.get_by_placeholder('Повторите пароль').fill(password)

    def click_signup_btn(self):
        self.page.locator('form').get_by_role('button', name='Зарегистрироваться').click()

    def expect_url_changed(self):
        expect(self.page).not_to_have_url('**/register')

    def expect_confirmation_message_visible(self):
        expect(self.page.get_by_text('Подтвердите свою почту', exact=True)).to_be_visible()

    def expect_signup_button_hidden(self):
        expect(
            self.page.locator('form').get_by_role(
                'button',
                name='Зарегистрироваться',
            )
        ).not_to_be_visible()
