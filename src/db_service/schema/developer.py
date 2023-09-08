"""
Developer schema
"""


from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text

from db_service.connect import METADATA
from db_service.environment import ENVIRONMENT


@dataclass
class Developer:
    """
    Class for keeping track of developer
    """

    id: int
    name: str
    logo: Optional[str]
    web_page: Optional[str]
    foundation_year: Optional[int]
    locations: Optional[list[str]]
    construction_types: Optional[list[str]]
    market_segments: Optional[list[str]]
    total_constructed_area: Optional[float]
    total_completed_projects: Optional[int]
    total_active_projects: Optional[int]
    active_projects: Optional[list[str]]
    agent_commission: Optional[float]
    documents: Optional[list[str]]


DEVELOPERS_TABLE = Table(
    ENVIRONMENT.developers_table_name,
    METADATA,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("logo", String(20)),
    Column("web_page", Text),
    Column("foundation_year", Integer),
    Column("total_constructed_area", Float),
    Column("total_completed_projects", Integer),
    Column("agent_commission", Float),
)

DEVELOPERS_PROJECTS_TABLE = Table(
    ENVIRONMENT.developers_projects_table_name,
    METADATA,
    Column(
        "developer",
        Integer,
        ForeignKey(f"{ENVIRONMENT.developers_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
)

DEVELOPERS_CONSTRUCTION_TYPES_TABLE = Table(
    ENVIRONMENT.developers_construction_types_table_name,
    METADATA,
    Column(
        "developer",
        Integer,
        ForeignKey(f"{ENVIRONMENT.developers_table_name}.id"),
        primary_key=True,
    ),
    Column("construction_type", String(60), primary_key=True),
)

DEVELOPERS_DOCUMENTS_TABLE = Table(
    ENVIRONMENT.developers_documents_table_name,
    METADATA,
    Column(
        "developer",
        Integer,
        ForeignKey(f"{ENVIRONMENT.developers_table_name}.id"),
        primary_key=True,
    ),
    Column("document", String(20), primary_key=True),
)

DEVELOPERS_LOCATIONS_TABLE = Table(
    ENVIRONMENT.developers_locations_table_name,
    METADATA,
    Column(
        "developer",
        Integer,
        ForeignKey(f"{ENVIRONMENT.developers_table_name}.id"),
        primary_key=True,
    ),
    Column("location", String(60), primary_key=True),
)

DEVELOPERS_MARKET_SEGMENTS_TABLE = Table(
    ENVIRONMENT.developers_market_segments_table_name,
    METADATA,
    Column(
        "developer",
        Integer,
        ForeignKey(f"{ENVIRONMENT.developers_table_name}.id"),
        primary_key=True,
    ),
    Column("market_segment", String(60), primary_key=True),
)

DEVELOPERS_COLUMNS = {
    "id": DEVELOPERS_TABLE.c.id,
    "name": DEVELOPERS_TABLE.c.name,
    "logo": DEVELOPERS_TABLE.c.logo,
    "web_page": DEVELOPERS_TABLE.c.web_page,
    "foundation_year": DEVELOPERS_TABLE.c.foundation_year,
    "total_constructed_area": DEVELOPERS_TABLE.c.total_constructed_area,
    "total_completed_projects": DEVELOPERS_TABLE.c.total_completed_projects,
    "agent_commission": DEVELOPERS_TABLE.c.agent_commission,
}

DEVELOPER_COLUMN_TO_TABLE = {
    "construction_type": DEVELOPERS_CONSTRUCTION_TYPES_TABLE,
    "document": DEVELOPERS_DOCUMENTS_TABLE,
    "locations": DEVELOPERS_LOCATIONS_TABLE,
    "market_segments": DEVELOPERS_MARKET_SEGMENTS_TABLE,
    **{column_name: DEVELOPERS_TABLE for column_name in DEVELOPERS_COLUMNS},
}
