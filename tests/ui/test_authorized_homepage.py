import allure
import pytest
from playwright.sync_api import expect


@allure.title('Authorized homepage smoke')
@allure.description('Checks that an authenticated user sees the profile link on the homepage.')
@pytest.mark.ui
@pytest.mark.smoke_stable
def test_authorized_homepage_smoke(ui_authorized_page, ui_base_url):
    with allure.step('Open the homepage'):
        ui_authorized_page.goto(ui_base_url)

    profile_link = ui_authorized_page.locator('a[href="/profile"]')
    with allure.step('Verify the profile link is visible'):
        expect(profile_link).to_be_visible()
        expect(profile_link).to_have_text('Профиль')
