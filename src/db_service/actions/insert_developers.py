from dataclasses import dataclass

from sqlalchemy import insert
from sqlalchemy.engine.base import Engine

from db_service.actions.io import Request, Response
from db_service.schema.developer import (
    DEVELOPERS_COLUMNS,
    DEVELOPERS_CONSTRUCTION_TYPES_TABLE,
    DEVELOPERS_DOCUMENTS_TABLE,
    DEVELOPERS_LOCATIONS_TABLE,
    DEVELOPERS_MARKET_SEGMENTS_TABLE,
    DEVELOPERS_TABLE,
)
from db_service.utils import columns_to_dict


@dataclass
class InsertDevelopersRequest(Request):
    """
    Request schema for insert developers action
    """

    engine: Engine
    developers: list[dict]


@dataclass
class InsertDevelopersResponse(Response):
    """
    Request schema for insert developers action
    """


def insert_all(request: InsertDevelopersRequest) -> InsertDevelopersResponse:
    """
    Inserts developers from list into database
    """
    developers = request.developers
    engine = request.engine
    with engine.connect() as conn:
        for developer in developers:
            developer_columns = list(DEVELOPERS_COLUMNS.keys())

            bare_developer = {k: developer[k] for k in developer_columns}
            conn.execute(insert(DEVELOPERS_TABLE).values(bare_developer))
            developer_id = developer["id"]
            if developer["construction_types"]:
                developer_constructions = columns_to_dict(
                    "developer", developer_id, "construction_type", developer["construction_types"]
                )
                conn.execute(insert(DEVELOPERS_CONSTRUCTION_TYPES_TABLE).values(developer_constructions))
            if developer["documents"]:
                developer_documents = columns_to_dict(
                    "developer", developer_id, "document", developer["documents"]
                )
                conn.execute(insert(DEVELOPERS_DOCUMENTS_TABLE).values(developer_documents))
            if developer["locations"]:
                developer_locations = columns_to_dict(
                    "developer", developer_id, "location", developer["locations"]
                )
                conn.execute(insert(DEVELOPERS_LOCATIONS_TABLE).values(developer_locations))
            if developer["market_segments"]:
                developer_market_segments = columns_to_dict(
                    "developer", developer_id, "market_segment", developer["market_segments"]
                )
                conn.execute(insert(DEVELOPERS_MARKET_SEGMENTS_TABLE).values(developer_market_segments))
        conn.commit()

    return InsertDevelopersResponse()
