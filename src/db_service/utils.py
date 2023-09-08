from typing import Union

import sqlalchemy
from sqlalchemy import Column, func


def to_list(column: Column) -> sqlalchemy.sql.functions.Function:
    """
    Builds aggregation for a list
    """
    return func.array_remove(func.array_agg(column.distinct()), None)


def columns_to_dict(
    id_name: str, id_value: int, column_name: str, column_values: list[Union[str, int, float, bool]]
) -> list[dict]:
    """
    Builds dictionary for columns
    """
    return [{id_name: id_value, column_name: v} for v in column_values]
