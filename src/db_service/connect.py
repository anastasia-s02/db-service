"""
Connects to database
"""


import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine


def connect_to_db() -> Engine:
    """
    Connects to postgres DB using env vars as credentials
    """
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_LOGIN')}:"
        + f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
        future=True,
    )
    return engine


ENGINE = connect_to_db()
METADATA = MetaData()
