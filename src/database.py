import os
import dotenv
from sqlalchemy import create_engine
import sqlalchemy


def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")


engine = create_engine(database_connection_url(), pool_pre_ping=True)


def get_db_connection() -> sqlalchemy.Connection:
    with engine.begin() as connection:
        yield connection
