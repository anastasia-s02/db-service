"""
Action registry
"""

import enum
from dataclasses import dataclass
from typing import Callable, Type

from db_service.actions import insert_apartments, select_apartment_by_ids
from db_service.actions.io import Request, Response


@dataclass
class Action:
    """
    Action for the db-serivce
    """

    name: str
    function: Callable
    request_schema: Type[Request]
    response_schema: Type[Response]


class ActionType(enum.Enum):
    """
    Types of actions
    """

    SELECT_APARTMENT_BY_IDS = "select_apartment_by_ids"
    INSERT_APARTMENTS = "insert_apartments"


ACTION_REGISTRY = {
    ActionType.SELECT_APARTMENT_BY_IDS: Action(
        name="select_apartment_by_ids",
        function=select_apartment_by_ids.select,
        request_schema=select_apartment_by_ids.SelectApartmentByIdsRequest,
        response_schema=select_apartment_by_ids.SelectApartmentByIdsResponse,
    ),
    ActionType.INSERT_APARTMENTS: Action(
        name="insert_apartments",
        function=insert_apartments.insert_all,
        request_schema=insert_apartments.InsertApartmentsRequest,
        response_schema=insert_apartments.InsertApartmentsResponse,
    ),
}
