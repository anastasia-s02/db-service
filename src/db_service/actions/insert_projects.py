"""
Insert projects action interface
"""


from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.developer import DEVELOPERS_PROJECTS_TABLE, DEVELOPERS_TABLE
from db_service.schema.project import (
    PROJECTS_AMENITIES_TABLE,
    PROJECTS_COLUMNS,
    PROJECTS_PAYMENT_METHODS_TABLE,
    PROJECTS_PHOTOS_TABLE,
    PROJECTS_REGULATIONS_TABLE,
    PROJECTS_TABLE,
)
from db_service.utils import columns_to_dict


@dataclass
class InsertProjectsRequest(Request):
    """
    Request schema for insert projects action
    """

    engine: Engine
    projects: list[dict]


@dataclass
class InsertProjectsResponse(Response):
    """
    Request schema for insert projects action
    """


def insert_all(request: InsertProjectsRequest) -> InsertProjectsResponse:
    """
    Inserts projects from list into database
    """
    projects = request.projects
    engine = request.engine
    with engine.connect() as conn:
        for project in projects:
            project_columns = list(PROJECTS_COLUMNS.keys())

            bare_project = {k: project[k] for k in project_columns}
            conn.execute(insert(PROJECTS_TABLE).values(bare_project))
            project_id = project["id"]
            if project["photos"]:
                project_photos = columns_to_dict("project", project_id, "photo", project["photos"])
                conn.execute(insert(PROJECTS_PHOTOS_TABLE).values(project_photos))
            if project["payment_methods"]:
                project_payment_methods = columns_to_dict(
                    "project", project_id, "payment_method", project["payment_methods"]
                )
                conn.execute(insert(PROJECTS_PAYMENT_METHODS_TABLE).values(project_payment_methods))
            if project["regulation"]:
                project_regulations = columns_to_dict(
                    "project", project_id, "regulation", project["regulation"]
                )
                conn.execute(insert(PROJECTS_REGULATIONS_TABLE).values(project_regulations))
            if project["amenities"]:
                project_amenities = columns_to_dict("project", project_id, "amenity", project["amenities"])
                conn.execute(insert(PROJECTS_AMENITIES_TABLE).values(project_amenities))
            if project["developer_name"]:
                developer_id = (
                    conn.execute(
                        select(DEVELOPERS_TABLE.c.id).where(
                            DEVELOPERS_TABLE.c.name == project["developer_name"]
                        )
                    ).all()
                )[0][0]
                project_developer = columns_to_dict("project", project_id, "developer", [developer_id])
                conn.execute(insert(DEVELOPERS_PROJECTS_TABLE).values(project_developer))
        conn.commit()
    return InsertProjectsResponse()
