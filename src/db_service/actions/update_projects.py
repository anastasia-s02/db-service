from dataclasses import dataclass
from typing import Any

from sqlalchemy import insert
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column, Table

from db_service.actions.io import Request, Response
from db_service.schema.project import PROJECT_COLUMN_TO_TABLE, PROJECTS_COLUMNS, PROJECTS_TABLE
from db_service.utils import columns_to_dict


@dataclass
class UpdateProjectsRequest(Request):
    """
    Request schema for update projects action
    """

    engine: Engine
    params: dict[str, dict[str, Any]]


@dataclass
class UpdateProjectsResponse(Response):
    """
    Request schema for update projects action
    """


def update_projects(request: UpdateProjectsRequest) -> UpdateProjectsResponse:
    """
    Updates projects from list into database
    """
    params = request.params
    engine = request.engine

    with engine.connect() as conn:

        for project_id_str in params:

            project_id = int(project_id_str)

            values_for_base_table: dict[Column, Any] = {}
            values_for_lists_tables: dict[Table, list[dict[str, Any]]] = {}
            for column_name in params[project_id_str]:
                table_obj = PROJECT_COLUMN_TO_TABLE[column_name]
                if table_obj == PROJECTS_TABLE:
                    values_for_base_table[PROJECTS_COLUMNS[column_name]] = params[project_id_str][column_name]
                else:
                    values_for_lists_tables[table_obj] = columns_to_dict(
                        table_obj.primary_key.columns.values()[0].name,
                        project_id,
                        table_obj.primary_key.columns.values()[1].name,
                        params[project_id_str][column_name],
                    )

            conn.execute(
                PROJECTS_TABLE.update().where(PROJECTS_TABLE.c.id == project_id).values(values_for_base_table)
            )
            for table_obj, values in values_for_lists_tables.items():
                conn.execute(insert(table_obj).values(values))
        conn.commit()
    return UpdateProjectsResponse()
