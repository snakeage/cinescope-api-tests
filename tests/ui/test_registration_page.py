import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@pytest.mark.smoke_stable
def test_registration_page_loads(page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')
    assert page.url.startswith('https://dev-cinescope.coconutqa.ru/register')

    expect(page.get_by_role('heading', name='Регистрация', level=2)).to_be_visible()
    expect(page.get_by_placeholder('Имя Фамилия Отчество')).to_be_visible()
    expect(page.get_by_placeholder('Email')).to_be_visible()
    expect(page.get_by_placeholder('Пароль', exact=True)).to_be_visible()
    expect(page.get_by_placeholder('Повторите пароль')).to_be_visible()
    expect(page.locator('form').get_by_role('button', name='Зарегистрироваться')).to_be_visible()
    expect(page.locator('form').get_by_role('link', name='Войти')).to_be_visible()
