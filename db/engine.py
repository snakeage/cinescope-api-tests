from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.db_creds import MoviesDbCreds


connection_string = (
    f"postgresql+psycopg2://{MoviesDbCreds.USERNAME}:"
    f"{MoviesDbCreds.PASSWORD}@{MoviesDbCreds.HOST}:"
    f"{MoviesDbCreds.PORT}/{MoviesDbCreds.DATABASE_NAME}"
)

engine = create_engine(connection_string, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()