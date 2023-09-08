from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine

from db_service.environment import ENVIRONMENT


def connect_to_db() -> Engine:
    """
    Connects to postgres DB using env vars as credentials
    """
    engine = create_engine(
        f"postgresql+psycopg2://{ENVIRONMENT.db_login}:"
        + f"{ENVIRONMENT.db_password}@{ENVIRONMENT.db_host}/{ENVIRONMENT.db_name}",
        future=True,
    )
    return engine


ENGINE = connect_to_db()
METADATA = MetaData()
