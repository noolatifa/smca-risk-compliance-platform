from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.core.config import settings

url = make_url(settings.database_url)
est_sqlite = url.get_backend_name() == "sqlite"

if est_sqlite and url.database:
    Path(url.database).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(url)

if est_sqlite:

    @event.listens_for(engine, "connect")
    def configurer_sqlite(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
