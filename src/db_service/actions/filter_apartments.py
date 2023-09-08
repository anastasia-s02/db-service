"""
Filter apartments action interface
"""


from dataclasses import dataclass

import sqlalchemy
from dacite import from_dict
from sqlalchemy import and_
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.apartment import APARTMENTS_COLUMNS, APARTMENTS_TABLE, Apartment


@dataclass
class FilterApartmentsRequest(Request):
    """
    Request schema for filter apartments action
    """

    engine: Engine
    clauses: dict[str, list]


@dataclass
class FilterApartmentsResponse(Response):
    """
    Request schema for filter apartments action
    """

    apartments: list[Apartment]


def filter_apartments(request: FilterApartmentsRequest) -> FilterApartmentsResponse:
    """
    Inserts apartments from list into database
    """
    clauses = request.clauses
    engine = request.engine

    sql_clauses: list[sqlalchemy.sql.elements.BinaryExpression] = []
    for column_name, column_values in clauses.items():
        sql_clauses.append(APARTMENTS_COLUMNS[column_name].in_(column_values))

    with engine.connect() as conn:
        result = conn.execute(APARTMENTS_TABLE.select().where(and_(*sql_clauses))).all()
    all_results = [dict(row) for row in result]
    return FilterApartmentsResponse(
        apartments=[from_dict(data_class=Apartment, data=item) for item in all_results]
    )
