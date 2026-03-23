from playwright.sync_api import expect


def test_login_page_loads(page):
    page.goto('https://dev-cinescope.coconutqa.ru/login')
    assert page.url.startswith('https://dev-cinescope.coconutqa.ru/login')

    expect(page.get_by_role('heading', name='Войти', level=2)).to_be_visible()
    expect(page.get_by_label('Email')).to_be_visible()
    expect(page.get_by_label('Пароль')).to_be_visible()
    expect(page.locator('form').get_by_role('button', name='Войти')).to_be_visible()
    expect(page.get_by_role('link', name='Зарегистрироваться')).to_be_visible()
