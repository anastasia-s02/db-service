"""
Insert apartment action interface
"""

from dataclasses import asdict, dataclass

from sqlalchemy import insert
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import APARTMENTS_TABLE, Apartment


@dataclass
class InsertApartmentsRequest(Request):
    """
    Request schema for insert apartments action
    """

    engine: Engine
    apartments: list[Apartment]


@dataclass
class InsertApartmentsResponse(Response):
    """
    Request schema for insert apartments action
    """


def insert_all(request: InsertApartmentsRequest) -> InsertApartmentsResponse:
    """
    Inserts apartments from list into database
    """
    apartments = request.apartments
    engine = request.engine
    for item in apartments:
        dict_repr = asdict(item)
        with engine.connect() as conn:
            conn.execute(insert(APARTMENTS_TABLE).values(dict_repr))
            conn.commit()
    return InsertApartmentsResponse()
