from dataclasses import dataclass

import sqlalchemy
from dacite import from_dict
from sqlalchemy import and_
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.project import PROJECTS_COLUMNS, PROJECTS_TABLE, Project


@dataclass
class FilterProjectsRequest(Request):
    """
    Request schema for filter projects action
    """

    engine: Engine
    clauses: dict[str, list]


@dataclass
class FilterProjectsResponse(Response):
    """
    Request schema for filter projects action
    """

    projects: list[Project]


def filter_projects(request: FilterProjectsRequest) -> FilterProjectsResponse:
    """
    Inserts projects from list into database
    """
    clauses = request.clauses
    engine = request.engine

    sql_clauses: list[sqlalchemy.sql.elements.BinaryExpression] = []
    for column_name, column_values in clauses.items():
        sql_clauses.append(PROJECTS_COLUMNS[column_name].in_(column_values))

    with engine.connect() as conn:
        result = conn.execute(PROJECTS_TABLE.select().where(and_(*sql_clauses))).all()
    all_results = [dict(row) for row in result]
    return FilterProjectsResponse(
        projects=[from_dict(data_class=Project, data=item) for item in all_results]
    )
