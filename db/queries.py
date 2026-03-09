from sqlalchemy import text

from db.engine import engine


def db_healthcheck() -> int:
    with engine.connect() as conn:
        return conn.execute(text('SELECT 1')).scalar_one()


def get_movies_count(session) -> int:
    return session.execute(text('SELECT COUNT(*) FROM movies')).scalar_one()


def get_published_movies(session, limit: int = 10):
    query = text("""
        SELECT id, name, price, location, genre_id, published
        FROM movies
        WHERE published = true
        ORDER BY id DESC
        LIMIT :limit
    """)
    rows = session.execute(query, {'limit': limit}).mappings().all()
    return rows


def get_movies_by_ids(session, movie_ids: list[int]):
    query = text("""
        SELECT id, published
        FROM movies
        WHERE id = ANY(:movie_ids)
    """)
    return session.execute(query, {'movie_ids': movie_ids}).mappings().all()
