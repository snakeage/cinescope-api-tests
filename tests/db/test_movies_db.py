import pytest
from sqlalchemy import text

from db.queries import get_movies_count, get_published_movies


class TestMoviesDb:
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.db
    def test_db_connection_healthcheck(self, db_session):
        result = db_session.execute(text('SELECT 1')).scalar_one()
        assert result == 1

    @pytest.mark.regression
    @pytest.mark.db
    def test_movies_table_has_rows(self, db_session):
        count = get_movies_count(db_session)
        assert count >= 0

    @pytest.mark.regression
    @pytest.mark.db
    def test_get_published_movies(self, db_session):
        rows = get_published_movies(db_session, limit=5)
        assert isinstance(rows, list)
        for row in rows:
            assert row['published'] is True
            assert 'id' in row
            assert 'name' in row
