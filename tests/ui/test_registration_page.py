import pytest

from pages.registration_page import RegistrationPage


@pytest.mark.ui
@pytest.mark.smoke_stable
def test_registration_page_loads(page, ui_base_url):
    registration_page = RegistrationPage(page)

    registration_page.open(ui_base_url)
    registration_page.expect_loaded()
