"""
Delete apartments action interface
"""


from dataclasses import dataclass

from sqlalchemy import delete
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import APARTMENTS_TABLE


@dataclass
class DeleteApartmentsRequest(Request):
    """
    Request schema for delete apartments action
    """

    engine: Engine
    apartments: list[int]


@dataclass
class DeleteApartmentsResponse(Response):
    """
    Request schema for delete apartments action
    """


def delete_all(request: DeleteApartmentsRequest) -> DeleteApartmentsResponse:
    """
    Deletes apartments from list
    """
    apartments = request.apartments
    engine = request.engine

    with engine.connect() as conn:
        for item in apartments:
            conn.execute(delete(APARTMENTS_TABLE).where(APARTMENTS_TABLE.c.id == item))
        conn.commit()

    return DeleteApartmentsResponse()
