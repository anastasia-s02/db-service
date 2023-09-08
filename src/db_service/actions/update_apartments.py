"""
Update apartments action interface
"""


from dataclasses import dataclass
from typing import Any

from sqlalchemy import insert
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column, Table

from db_service.actions.io import Request, Response
from db_service.schema.apartment import (
    APARTMENT_COLUMN_TO_TABLE,
    APARTMENTS_COLUMNS,
    APARTMENTS_TABLE,
)
from db_service.utils import columns_to_dict


@dataclass
class UpdateApartmentsRequest(Request):
    """
    Request schema for update apartments action
    """

    engine: Engine
    params: dict[str, dict[str, Any]]


@dataclass
class UpdateApartmentsResponse(Response):
    """
    Request schema for update apartments action
    """


def update_apartments(request: UpdateApartmentsRequest) -> UpdateApartmentsResponse:
    """
    Updates apartments from list into database
    """
    params = request.params
    engine = request.engine
    with engine.connect() as conn:
        for apartment_id_str in params:

            apartment_id = int(apartment_id_str)

            values_for_base_table: dict[Column, Any] = {}
            values_for_lists_tables: dict[Table, list[dict[str, Any]]] = {}
            for column_name in params[apartment_id_str]:
                table_obj = APARTMENT_COLUMN_TO_TABLE[column_name]
                if table_obj == APARTMENTS_TABLE:
                    values_for_base_table[APARTMENTS_COLUMNS[column_name]] = params[apartment_id_str][
                        column_name
                    ]
                else:
                    values_for_lists_tables[table_obj] = columns_to_dict(
                        table_obj.primary_key.columns.values()[0].name,
                        apartment_id,
                        table_obj.primary_key.columns.values()[1].name,
                        params[apartment_id_str][column_name],
                    )

            conn.execute(
                APARTMENTS_TABLE.update()
                .where(APARTMENTS_TABLE.c.id == apartment_id)
                .values(values_for_base_table)
            )
            for table_obj, values in values_for_lists_tables.items():
                conn.execute(insert(table_obj).values(values))
        conn.commit()
    return UpdateApartmentsResponse()
