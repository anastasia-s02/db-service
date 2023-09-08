"""
FIlter developers action interface
"""


from dataclasses import dataclass

import sqlalchemy
from dacite import from_dict
from sqlalchemy import and_
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.developer import DEVELOPERS_COLUMNS, DEVELOPERS_TABLE, Developer


@dataclass
class FilterDevelopersRequest(Request):
    """
    Request schema for filter developers action
    """

    engine: Engine
    clauses: dict[str, list]


@dataclass
class FilterDevelopersResponse(Response):
    """
    Request schema for filter developers action
    """

    developers: list[Developer]


def filter_developers(request: FilterDevelopersRequest) -> FilterDevelopersResponse:
    """
    Inserts developers from list into database
    """
    clauses = request.clauses
    engine = request.engine

    sql_clauses: list[sqlalchemy.sql.elements.BinaryExpression] = []
    for column_name, column_values in clauses.items():
        sql_clauses.append(DEVELOPERS_COLUMNS[column_name].in_(column_values))

    with engine.connect() as conn:
        result = conn.execute(DEVELOPERS_TABLE.select().where(and_(*sql_clauses))).all()
    all_results = [dict(row) for row in result]
    return FilterDevelopersResponse(
        developers=[from_dict(data_class=Developer, data=item) for item in all_results]
    )
