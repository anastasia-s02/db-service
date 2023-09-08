import enum
from dataclasses import dataclass
from typing import Callable, Type

from db_service.actions import (
    delete_apartments,
    delete_developers,
    delete_projects,
    filter_apartments,
    filter_developers,
    filter_projects,
    insert_apartments,
    insert_developers,
    insert_projects,
    select_apartment_by_ids,
    select_developer_by_ids,
    select_project_by_ids,
    update_apartments,
    update_developers,
    update_projects,
)
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
    FILTER_APARTMENTS = "filter_apartments"
    SELECT_DEVELOPER_BY_IDS = "select_developer_by_ids"
    INSERT_DEVELOPERS = "insert_developers"
    SELECT_PROJECT_BY_IDS = "select_project_by_ids"
    INSERT_PROJECTS = "insert_projects"
    FILTER_PROJECTS = "filter_projects"
    FILTER_DEVELOPERS = "filter_developers"
    UPDATE_PROJECTS = "update_projects"
    UPDATE_APARTMENTS = "update_apartments"
    UPDATE_DEVELOPERS = "update_developers"
    DELETE_DEVELOPERS = "delete_developers"
    DELETE_APARTMENTS = "delete_apartments"
    DELETE_PROJECTS = "delete_projects"


ACTION_REGISTRY = {
    ActionType.SELECT_APARTMENT_BY_IDS: Action(
        name="select_apartment_by_ids",
        function=select_apartment_by_ids.select_all,
        request_schema=select_apartment_by_ids.SelectApartmentByIdsRequest,
        response_schema=select_apartment_by_ids.SelectApartmentByIdsResponse,
    ),
    ActionType.INSERT_APARTMENTS: Action(
        name="insert_apartments",
        function=insert_apartments.insert_all,
        request_schema=insert_apartments.InsertApartmentsRequest,
        response_schema=insert_apartments.InsertApartmentsResponse,
    ),
    ActionType.FILTER_APARTMENTS: Action(
        name="filter_apartments",
        function=filter_apartments.filter_apartments,
        request_schema=filter_apartments.FilterApartmentsRequest,
        response_schema=filter_apartments.FilterApartmentsResponse,
    ),
    ActionType.SELECT_DEVELOPER_BY_IDS: Action(
        name="select_developer_by_ids",
        function=select_developer_by_ids.select_all,
        request_schema=select_developer_by_ids.SelectDeveloperByIdsRequest,
        response_schema=select_developer_by_ids.SelectDeveloperByIdsResponse,
    ),
    ActionType.INSERT_DEVELOPERS: Action(
        name="insert_developers",
        function=insert_developers.insert_all,
        request_schema=insert_developers.InsertDevelopersRequest,
        response_schema=insert_developers.InsertDevelopersResponse,
    ),
    ActionType.SELECT_PROJECT_BY_IDS: Action(
        name="select_project_by_ids",
        function=select_project_by_ids.select_all,
        request_schema=select_project_by_ids.SelectProjectByIdsRequest,
        response_schema=select_project_by_ids.SelectProjectByIdsResponse,
    ),
    ActionType.INSERT_PROJECTS: Action(
        name="insert_projects",
        function=insert_projects.insert_all,
        request_schema=insert_projects.InsertProjectsRequest,
        response_schema=insert_projects.InsertProjectsResponse,
    ),
    ActionType.FILTER_PROJECTS: Action(
        name="filter_projects",
        function=filter_projects.filter_projects,
        request_schema=filter_projects.FilterProjectsRequest,
        response_schema=filter_projects.FilterProjectsResponse,
    ),
    ActionType.FILTER_DEVELOPERS: Action(
        name="filter_developers",
        function=filter_developers.filter_developers,
        request_schema=filter_developers.FilterDevelopersRequest,
        response_schema=filter_developers.FilterDevelopersResponse,
    ),
    ActionType.UPDATE_DEVELOPERS: Action(
        name="update_developers",
        function=update_developers.update_developers,
        request_schema=update_developers.UpdateDevelopersRequest,
        response_schema=update_developers.UpdateDevelopersResponse,
    ),
    ActionType.UPDATE_PROJECTS: Action(
        name="update_projects",
        function=update_projects.update_projects,
        request_schema=update_projects.UpdateProjectsRequest,
        response_schema=update_projects.UpdateProjectsResponse,
    ),
    ActionType.UPDATE_APARTMENTS: Action(
        name="update_apartments",
        function=update_apartments.update_apartments,
        request_schema=update_apartments.UpdateApartmentsRequest,
        response_schema=update_apartments.UpdateApartmentsResponse,
    ),
    ActionType.DELETE_DEVELOPERS: Action(
        name="delete_developers",
        function=delete_developers.delete_all,
        request_schema=delete_developers.DeleteDevelopersRequest,
        response_schema=delete_developers.DeleteDevelopersResponse,
    ),
    ActionType.DELETE_APARTMENTS: Action(
        name="delete_apartments",
        function=delete_apartments.delete_all,
        request_schema=delete_apartments.DeleteApartmentsRequest,
        response_schema=delete_apartments.DeleteApartmentsResponse,
    ),
    ActionType.DELETE_PROJECTS: Action(
        name="delete_projects",
        function=delete_projects.delete_all,
        request_schema=delete_projects.DeleteProjectsRequest,
        response_schema=delete_projects.DeleteProjectsResponse,
    ),
}
