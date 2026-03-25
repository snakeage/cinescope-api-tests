from playwright.sync_api import expect

from utils.data_generator import DataGenerator


def test_registration_flow(page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    expect(page.get_by_role('heading', name='Регистрация', level=2)).to_be_visible()

    full_name = DataGenerator.generate_random_name()
    page.get_by_placeholder('Имя Фамилия Отчество').fill(full_name)

    email = DataGenerator.generate_random_email()
    page.get_by_placeholder('Email').fill(email)

    password = DataGenerator.generate_random_password()
    page.get_by_placeholder('Пароль', exact=True).fill(password)
    page.get_by_placeholder('Повторите пароль').fill(password)

    page.locator('form').get_by_role('button', name='Зарегистрироваться').click()

    expect(page).not_to_have_url('**/register')
    expect(page.get_by_text('Подтвердите свою почту', exact=True)).to_be_visible()
    expect(
        page.locator('form').get_by_role('button', name='Зарегистрироваться')
    ).not_to_be_visible()
