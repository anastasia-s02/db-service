"""
Select apartments by IDs action interface
"""


from dataclasses import dataclass

from dacite import from_dict
from sqlalchemy import select
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import (
    APARTMENTS_APPLIANCES_TABLE,
    APARTMENTS_EXTRA_FEATURES_TABLE,
    APARTMENTS_TABLE,
    Apartment,
)
from db_service.schema.developer import DEVELOPERS_PROJECTS_TABLE, DEVELOPERS_TABLE
from db_service.schema.project import (
    PROJECTS_AMENITIES_TABLE,
    PROJECTS_APARTMENTS_TABLE,
    PROJECTS_REGULATIONS_TABLE,
    PROJECTS_TABLE,
)
from db_service.utils import to_list


@dataclass
class SelectApartmentByIdsRequest(Request):
    """
    Request schema for select apartment by ids action
    """

    engine: Engine
    apartment_ids: list[int]


@dataclass
class SelectApartmentByIdsResponse(Response):
    """
    Request schema for select apartment by ids action
    """

    apartments: list[Apartment]


def select_all(request: SelectApartmentByIdsRequest) -> SelectApartmentByIdsResponse:
    """
    Selects a row from database by ID
    """
    engine = request.engine
    apartment_ids = request.apartment_ids

    with engine.connect() as conn:
        result = conn.execute(
            select(
                [
                    APARTMENTS_TABLE,
                    to_list(APARTMENTS_APPLIANCES_TABLE.c.appliance).label("appliances"),
                    to_list(APARTMENTS_EXTRA_FEATURES_TABLE.c.extra_feature).label("extra_features"),
                    to_list(PROJECTS_REGULATIONS_TABLE.c.regulation).label("regulation"),
                    to_list(PROJECTS_AMENITIES_TABLE.c.amenity).label("amenities"),
                    PROJECTS_TABLE.c.location,
                    PROJECTS_TABLE.c.name.label("project_name"),
                    DEVELOPERS_TABLE.c.name.label("developer_name"),
                    PROJECTS_TABLE.c.completion_date,
                    PROJECTS_TABLE.c.dld_charge,
                    PROJECTS_TABLE.c.transaction_costs,
                    PROJECTS_TABLE.c.service_charge_per_sqft_per_year,
                    PROJECTS_TABLE.c.time_to_beach,
                    PROJECTS_TABLE.c.time_to_downtown,
                    PROJECTS_TABLE.c.time_to_school,
                    PROJECTS_TABLE.c.time_to_hospital,
                    PROJECTS_TABLE.c.time_to_airport,
                    PROJECTS_TABLE.c.time_to_marina,
                    PROJECTS_TABLE.c.time_to_mall,
                    (APARTMENTS_TABLE.c.total_price / APARTMENTS_TABLE.c.total_area).label("price_per_ft"),
                ]
            )
            .outerjoin(
                PROJECTS_APARTMENTS_TABLE,
                PROJECTS_APARTMENTS_TABLE.c.apartment == APARTMENTS_TABLE.c.id,
            )
            .outerjoin(PROJECTS_TABLE, PROJECTS_TABLE.c.id == PROJECTS_APARTMENTS_TABLE.c.project)
            .outerjoin(
                DEVELOPERS_PROJECTS_TABLE,
                DEVELOPERS_PROJECTS_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(DEVELOPERS_TABLE, DEVELOPERS_TABLE.c.id == DEVELOPERS_PROJECTS_TABLE.c.developer)
            .outerjoin(
                APARTMENTS_APPLIANCES_TABLE,
                APARTMENTS_APPLIANCES_TABLE.c.apartment == APARTMENTS_TABLE.c.id,
            )
            .outerjoin(
                APARTMENTS_EXTRA_FEATURES_TABLE,
                APARTMENTS_EXTRA_FEATURES_TABLE.c.apartment == APARTMENTS_TABLE.c.id,
            )
            .outerjoin(
                PROJECTS_REGULATIONS_TABLE,
                PROJECTS_REGULATIONS_TABLE.c.project == PROJECTS_TABLE.c.id,
            )
            .outerjoin(PROJECTS_AMENITIES_TABLE, PROJECTS_AMENITIES_TABLE.c.project == PROJECTS_TABLE.c.id)
            .where(APARTMENTS_TABLE.c.id.in_(apartment_ids))
            .group_by(
                APARTMENTS_TABLE.c.id,
                PROJECTS_TABLE.c.name,
                DEVELOPERS_TABLE.c.name,
                PROJECTS_TABLE.c.completion_date,
                PROJECTS_TABLE.c.dld_charge,
                PROJECTS_TABLE.c.transaction_costs,
                PROJECTS_TABLE.c.service_charge_per_sqft_per_year,
                PROJECTS_TABLE.c.time_to_beach,
                PROJECTS_TABLE.c.time_to_downtown,
                PROJECTS_TABLE.c.time_to_school,
                PROJECTS_TABLE.c.time_to_hospital,
                PROJECTS_TABLE.c.time_to_airport,
                PROJECTS_TABLE.c.time_to_marina,
                PROJECTS_TABLE.c.time_to_mall,
                PROJECTS_TABLE.c.location,
                APARTMENTS_TABLE.c.total_price,
                APARTMENTS_TABLE.c.total_area,
            )
        ).all()

    all_results = [dict(row) for row in result]
    return SelectApartmentByIdsResponse(
        apartments=[from_dict(data_class=Apartment, data=item) for item in all_results]
    )
