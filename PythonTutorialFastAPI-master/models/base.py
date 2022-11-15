from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import Config

Base = declarative_base()
config = Config()

engine = create_engine(config.postgres_host)


def recreate_postgres_tables() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
