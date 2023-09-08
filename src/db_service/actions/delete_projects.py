"""
Delete projects action interface
"""


from dataclasses import dataclass

from sqlalchemy import delete
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.project import PROJECTS_TABLE


@dataclass
class DeleteProjectsRequest(Request):
    """
    Request schema for delete projects action
    """

    engine: Engine
    projects: list[int]


@dataclass
class DeleteProjectsResponse(Response):
    """
    Request schema for delete projects action
    """


def delete_all(request: DeleteProjectsRequest) -> DeleteProjectsResponse:
    """
    Deletes projects from list
    """
    projects = request.projects
    engine = request.engine

    with engine.connect() as conn:
        for item in projects:
            conn.execute(delete(PROJECTS_TABLE).where(PROJECTS_TABLE.c.id == item))
        conn.commit()

    return DeleteProjectsResponse()
