from dataclasses import dataclass

from dacite import from_dict
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql import func

from db_service.actions.io import Request, Response
from db_service.schema.apartment import APARTMENTS_TABLE
from db_service.schema.developer import DEVELOPERS_PROJECTS_TABLE, DEVELOPERS_TABLE
from db_service.schema.project import (
    PROJECTS_AMENITIES_TABLE,
    PROJECTS_APARTMENTS_TABLE,
    PROJECTS_PAYMENT_METHODS_TABLE,
    PROJECTS_PHOTOS_TABLE,
    PROJECTS_REGULATIONS_TABLE,
    PROJECTS_TABLE,
    Project,
)
from db_service.utils import to_list


@dataclass
class SelectProjectByIdsRequest(Request):
    """
    Request schema for select project by ids action
    """

    engine: Engine
    project_ids: list[int]


@dataclass
class SelectProjectByIdsResponse(Response):
    """
    Request schema for select project by ids action
    """

    projects: list[Project]


def select_all(request: SelectProjectByIdsRequest) -> SelectProjectByIdsResponse:
    """
    Selects a row from database by ID
    """
    engine = request.engine
    project_ids = request.project_ids

    available_apts = (
        select(
            PROJECTS_APARTMENTS_TABLE.c.project,
            func.count(PROJECTS_APARTMENTS_TABLE.c.apartment).label("available_apartments"),
        )
        .group_by(PROJECTS_APARTMENTS_TABLE.c.project)
        .subquery()
    )

    apartments_agg_stats = (
        select(
            PROJECTS_APARTMENTS_TABLE.c.project,
            func.sum(APARTMENTS_TABLE.c.total_area).label("project_total_area"),
            func.sum(APARTMENTS_TABLE.c.total_price).label("project_total_price"),
            (func.sum(APARTMENTS_TABLE.c.total_price) / func.sum(APARTMENTS_TABLE.c.total_area)).label(
                "price_per_sqft"
            ),
        )
        .outerjoin(APARTMENTS_TABLE, APARTMENTS_TABLE.c.id == PROJECTS_APARTMENTS_TABLE.c.apartment)
        .group_by(PROJECTS_APARTMENTS_TABLE.c.project)
        .subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            select(
                [
                    PROJECTS_TABLE,
                    to_list(PROJECTS_PHOTOS_TABLE.c.photo).label("photos"),
                    to_list(PROJECTS_AMENITIES_TABLE.c.amenity).label("amenities"),
                    to_list(PROJECTS_REGULATIONS_TABLE.c.regulation).label("regulations"),
                    to_list(PROJECTS_PAYMENT_METHODS_TABLE.c.payment_method).label("payment_methods"),
                    to_list(APARTMENTS_TABLE.c.apartment_type).label("apartment_types"),
                    DEVELOPERS_TABLE.c.name.label("developer_name"),
                    available_apts.c.available_apartments,
                    apartments_agg_stats.c.project_total_price.label("total_price"),
                    apartments_agg_stats.c.project_total_area.label("total_area"),
                    apartments_agg_stats.c.price_per_sqft,
                ]
            )
            .outerjoin(
                available_apts,
                available_apts.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(apartments_agg_stats, apartments_agg_stats.c.project == PROJECTS_TABLE.c.id)
            .outerjoin(PROJECTS_APARTMENTS_TABLE, PROJECTS_APARTMENTS_TABLE.c.project == PROJECTS_TABLE.c.id)
            .outerjoin(APARTMENTS_TABLE, APARTMENTS_TABLE.c.id == PROJECTS_APARTMENTS_TABLE.c.apartment)
            .outerjoin(
                PROJECTS_PHOTOS_TABLE,
                PROJECTS_PHOTOS_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(
                PROJECTS_AMENITIES_TABLE,
                PROJECTS_AMENITIES_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(
                PROJECTS_PAYMENT_METHODS_TABLE,
                PROJECTS_PAYMENT_METHODS_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(
                PROJECTS_REGULATIONS_TABLE,
                PROJECTS_REGULATIONS_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(
                DEVELOPERS_PROJECTS_TABLE,
                PROJECTS_TABLE.c.id == DEVELOPERS_PROJECTS_TABLE.c.project,
            )
            .outerjoin(
                DEVELOPERS_TABLE,
                DEVELOPERS_TABLE.c.id == DEVELOPERS_PROJECTS_TABLE.c.developer,
            )
            .where(PROJECTS_TABLE.c.id.in_(project_ids))
            .group_by(
                apartments_agg_stats.c.project_total_area,
                apartments_agg_stats.c.price_per_sqft,
                available_apts.c.available_apartments,
                apartments_agg_stats.c.project_total_price,
                PROJECTS_TABLE.c.id,
                PROJECTS_AMENITIES_TABLE.c.project,
                PROJECTS_PAYMENT_METHODS_TABLE.c.project,
                DEVELOPERS_TABLE.c.id,
            )
        ).all()

    return SelectProjectByIdsResponse(
        projects=[from_dict(data_class=Project, data=dict(row)) for row in result]
    )
