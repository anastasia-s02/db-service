from dataclasses import dataclass

from dacite import from_dict
from sqlalchemy import select
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.developer import (
    DEVELOPERS_CONSTRUCTION_TYPES_TABLE,
    DEVELOPERS_DOCUMENTS_TABLE,
    DEVELOPERS_LOCATIONS_TABLE,
    DEVELOPERS_MARKET_SEGMENTS_TABLE,
    DEVELOPERS_PROJECTS_TABLE,
    DEVELOPERS_TABLE,
    Developer,
)
from db_service.schema.project import PROJECTS_TABLE
from db_service.utils import to_list


@dataclass
class SelectDeveloperByIdsRequest(Request):
    """
    Request schema for select developer by ids action
    """

    engine: Engine
    developer_ids: list[int]


@dataclass
class SelectDeveloperByIdsResponse(Response):
    """
    Request schema for select developer by ids action
    """

    developers: list[Developer]


def select_all(request: SelectDeveloperByIdsRequest) -> SelectDeveloperByIdsResponse:
    """
    Selects a row from database by ID
    """
    engine = request.engine
    developer_ids = request.developer_ids

    with engine.connect() as conn:
        result = conn.execute(
            select(
                [
                    DEVELOPERS_TABLE,
                    to_list(DEVELOPERS_CONSTRUCTION_TYPES_TABLE.c.construction_type).label(
                        "construction_types"
                    ),
                    to_list(DEVELOPERS_DOCUMENTS_TABLE.c.document).label("documents"),
                    to_list(DEVELOPERS_MARKET_SEGMENTS_TABLE.c.market_segment).label("market_segments"),
                    to_list(DEVELOPERS_LOCATIONS_TABLE.c.location).label("locations"),
                    to_list(PROJECTS_TABLE.c.name).label("active_projects"),
                ]
            )
            .outerjoin(
                DEVELOPERS_CONSTRUCTION_TYPES_TABLE,
                DEVELOPERS_CONSTRUCTION_TYPES_TABLE.c.developer == DEVELOPERS_TABLE.c.id,
            )
            .outerjoin(
                DEVELOPERS_DOCUMENTS_TABLE,
                DEVELOPERS_DOCUMENTS_TABLE.c.developer == DEVELOPERS_TABLE.c.id,
            )
            .outerjoin(
                DEVELOPERS_MARKET_SEGMENTS_TABLE,
                DEVELOPERS_MARKET_SEGMENTS_TABLE.c.developer == DEVELOPERS_TABLE.c.id,
            )
            .outerjoin(
                DEVELOPERS_PROJECTS_TABLE,
                DEVELOPERS_PROJECTS_TABLE.c.developer == DEVELOPERS_TABLE.c.id,
            )
            .outerjoin(
                DEVELOPERS_LOCATIONS_TABLE,
                DEVELOPERS_LOCATIONS_TABLE.c.developer == DEVELOPERS_TABLE.c.id,
            )
            .join(PROJECTS_TABLE, PROJECTS_TABLE.c.id == DEVELOPERS_PROJECTS_TABLE.c.project)
            .where(DEVELOPERS_TABLE.c.id.in_(developer_ids))
            .group_by(
                DEVELOPERS_TABLE.c.id,
            )
        ).all()

    return SelectDeveloperByIdsResponse(
        developers=[from_dict(data_class=Developer, data=dict(row)) for row in result]
    )
