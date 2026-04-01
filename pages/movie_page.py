import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class MoviePage(BasePage):
    def open_movie(self, movie_id, base_url):
        self.page.goto(f'{base_url.rstrip("/")}/movies/{movie_id}')

    def expect_loaded(self, movie_name, movie_description=None):
        expect(self.page.get_by_role('heading', name=movie_name, level=2)).to_have_text(movie_name)

        if movie_description:
            expect(self.page.get_by_text(movie_description, exact=True)).to_be_visible()

        expect(self.page.get_by_text('Жанр')).to_be_visible()
        expect(
            self.page.get_by_role('heading', level=3, name=re.compile(r'Ре.*тинг'))
        ).to_be_visible()
        expect(self.page.get_by_role('link', name='Купить билет')).to_be_visible()
        expect(self.page.get_by_role('heading', name='Отзывы:', level=2)).to_be_visible()

    def fill_review(self, text):
        self.page.locator('form').get_by_role('textbox').fill(text)

    def submit_review(self):
        self.page.locator('form').get_by_role('button', name='Отправить').click()

    def expect_review_visible(self, text):
        expect(self.page.get_by_text(text, exact=True)).to_be_visible()
