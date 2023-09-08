"""
Insert apartments action interface
"""


from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import (
    APARTMENTS_APPLIANCES_TABLE,
    APARTMENTS_COLUMNS,
    APARTMENTS_EXTRA_FEATURES_TABLE,
    APARTMENTS_TABLE,
)
from db_service.schema.project import PROJECTS_APARTMENTS_TABLE, PROJECTS_TABLE
from db_service.utils import columns_to_dict


@dataclass
class InsertApartmentsRequest(Request):
    """
    Request schema for insert apartments action
    """

    engine: Engine
    apartments: list[dict]


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
    with engine.connect() as conn:
        for apartment in apartments:
            apartment_columns = list(APARTMENTS_COLUMNS.keys())
            bare_apartment = {k: apartment[k] for k in apartment_columns}
            conn.execute(insert(APARTMENTS_TABLE).values(bare_apartment))
            apartment_id = apartment["id"]

            if apartment["appliances"]:
                apartment_appliances = columns_to_dict(
                    "apartment", apartment_id, "appliance", apartment["appliances"]
                )
                conn.execute(insert(APARTMENTS_APPLIANCES_TABLE).values(apartment_appliances))

            if apartment["extra_features"]:
                apartment_extra_features = columns_to_dict(
                    "apartment", apartment_id, "extra_feature", apartment["extra_features"]
                )
                conn.execute(insert(APARTMENTS_EXTRA_FEATURES_TABLE).values(apartment_extra_features))
            project_id = (
                conn.execute(
                    select(PROJECTS_TABLE.c.id).where(PROJECTS_TABLE.c.name == apartment["project_name"])
                ).all()
            )[0][0]
            apartment_project = columns_to_dict("apartment", apartment_id, "project", [project_id])
            conn.execute(insert(PROJECTS_APARTMENTS_TABLE).values(apartment_project))
        conn.commit()
    return InsertApartmentsResponse()
