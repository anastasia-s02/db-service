"""
Delete developers action interface
"""


from dataclasses import dataclass

from sqlalchemy import delete
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.developer import DEVELOPERS_TABLE


@dataclass
class DeleteDevelopersRequest(Request):
    """
    Request schema for delete developers action
    """

    engine: Engine
    developers: list[int]


@dataclass
class DeleteDevelopersResponse(Response):
    """
    Request schema for delete developers action
    """


def delete_all(request: DeleteDevelopersRequest) -> DeleteDevelopersResponse:
    """
    Deletes developers from list
    """
    developers = request.developers
    engine = request.engine

    with engine.connect() as conn:
        for item in developers:
            conn.execute(delete(DEVELOPERS_TABLE).where(DEVELOPERS_TABLE.c.id == item))
        conn.commit()

    return DeleteDevelopersResponse()
