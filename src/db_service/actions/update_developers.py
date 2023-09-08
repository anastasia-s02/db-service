from dataclasses import dataclass
from typing import Any

from sqlalchemy import insert
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column, Table

from db_service.actions.io import Request, Response
from db_service.schema.developer import (
    DEVELOPER_COLUMN_TO_TABLE,
    DEVELOPERS_COLUMNS,
    DEVELOPERS_TABLE,
)
from db_service.utils import columns_to_dict


@dataclass
class UpdateDevelopersRequest(Request):
    """
    Request schema for update developers action
    """

    engine: Engine
    param: dict[str, dict[str, Any]]


@dataclass
class UpdateDevelopersResponse(Response):
    """
    Request schema for update developers action
    """


def update_developers(request: UpdateDevelopersRequest) -> UpdateDevelopersResponse:
    """
    Updates developers from list into database
    """
    params = request.param
    engine = request.engine

    with engine.connect() as conn:
        for developer_id_str in params:
            # msgpack does not allow ints as dict ids
            developer_id = int(developer_id_str)

            values_for_base_table: dict[Column, Any] = {}
            values_for_lists_tables: dict[Table, list[dict[str, Any]]] = {}
            for column_name in params[developer_id_str]:
                table_obj = DEVELOPER_COLUMN_TO_TABLE[column_name]
                if table_obj == DEVELOPERS_TABLE:
                    values_for_base_table[DEVELOPERS_COLUMNS[column_name]] = params[developer_id_str][
                        column_name
                    ]
                else:
                    values_for_lists_tables[table_obj] = columns_to_dict(
                        table_obj.primary_key.columns.values()[0].name,
                        developer_id,
                        table_obj.primary_key.columns.values()[1].name,
                        params[developer_id_str][column_name],
                    )

            conn.execute(
                DEVELOPERS_TABLE.update()
                .where(DEVELOPERS_TABLE.c.id == developer_id)
                .values(values_for_base_table)
            )
            for table_obj, values in values_for_lists_tables.items():
                conn.execute(insert(table_obj).values(values))
        conn.commit()
    return UpdateDevelopersResponse()
