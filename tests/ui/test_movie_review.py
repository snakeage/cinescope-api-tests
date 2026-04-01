import allure
import pytest

from pages.movie_page import MoviePage


@allure.title('Leave a review under a movie')
@allure.description('User opens a movie page, submits a review, and verifies it is visible.')
@pytest.mark.ui
@pytest.mark.regression
def test_movie_review(ui_authorized_page, ui_base_url, created_movie, movie_data):
    movie_page = MoviePage(ui_authorized_page)

    with allure.step('Open the movie page'):
        movie_page.open_movie(created_movie.id, ui_base_url)

    with allure.step('Verify the movie page is loaded'):
        movie_page.expect_loaded(created_movie.name, movie_data['description'])

    review_text = 'Good movie'
    with allure.step('Fill the review form'):
        movie_page.fill_review(review_text)

    with allure.step('Submit the review'):
        movie_page.submit_review()

    with allure.step('Verify the review is visible'):
        movie_page.expect_review_visible(review_text)
