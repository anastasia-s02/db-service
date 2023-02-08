"""
Apartment schema
"""

import os
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Table

from db_service.connect import METADATA


@dataclass
class Apartment:
    """
    Class for keeping track of apartment unit.
    """

    id_num: int
    name: str
    cost: int


APARTMENTS_TABLE = Table(
    os.getenv("APARTMENTS_TABLE_NAME"),
    METADATA,
    Column("id_num", Integer, primary_key=True),
    Column("name", String(20)),
    Column("cost", Integer),
)
