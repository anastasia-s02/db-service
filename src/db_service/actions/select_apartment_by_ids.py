"""
Select apartment action interface
"""

from dataclasses import dataclass

from dacite import from_dict
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import APARTMENTS_TABLE, Apartment


@dataclass
class SelectApartmentByIdsRequest(Request):
    """
    Request schema for select apartment by ids action
    """

    engine: Engine
    apartment_ids: list[str]


@dataclass
class SelectApartmentByIdsResponse(Response):
    """
    Request schema for select apartment by ids action
    """

    apartments: list[Apartment]


def select(request: SelectApartmentByIdsRequest) -> SelectApartmentByIdsResponse:
    """
    Selects a row from database by ID
    """
    engine = request.engine
    apartment_ids = request.apartment_ids

    result = (
        engine.connect()
        .execute(
            APARTMENTS_TABLE.select().where(
                APARTMENTS_TABLE.c.id_num.in_(apartment_ids)
            )
        )
        .all()
    )
    all_results = [dict(row) for row in result]
    return SelectApartmentByIdsResponse(
        apartments=[from_dict(data_class=Apartment, data=item) for item in all_results]
    )
