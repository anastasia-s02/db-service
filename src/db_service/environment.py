from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Variable:
    """
    A way to express an attribute that we'll load from an environment variable,
    with a given default.

    Environment variables are all strings, so the values will be run through the
    `data_type` constructor to make sure they're the correct type.
    """

    attr_name: str
    env_name: str
    default: Any
    data_type: type = str


DEFAULTS = [
    Variable("rmq_connect", "RMQ_CONNECT", "", str),
    Variable("rmq_queue", "RMQ_QUEUE", "", str),
    Variable("db_password", "DB_PASSWORD", "", str),
    Variable("db_login", "DB_LOGIN", "", str),
    Variable("db_host", "DB_HOST", "", str),
    Variable("db_name", "DB_NAME", "", str),
    Variable("apartments_table_name", "APARTMENTS_TABLE_NAME", "dev.apartments", str),
    Variable("developers_table_name", "DEVELOPERS_TABLE_NAME", "dev.developers", str),
    Variable(
        "developers_projects_table_name",
        "DEVELOPERS_PROJECTS_TABLE_NAME",
        "dev.developers-projects",
        str,
    ),
    Variable(
        "developers_construction_types_table_name",
        "DEVELOPERS_CONSTRUCTION_TYPES_TABLE_NAME",
        "dev.developers-construction_types",
        str,
    ),
    Variable(
        "developers_documents_table_name",
        "DEVELOPERS_DOCUMENTS_TABLE_NAME",
        "dev.developers-documents",
        str,
    ),
    Variable(
        "developers_locations_table_name",
        "DEVELOPERS_LOCATIONS_TYPES_TABLE_NAME",
        "dev.developers-locations",
        str,
    ),
    Variable(
        "developers_market_segments_table_name",
        "DEVELOPERS_MARKET_SEGMENTS_TABLE_NAME",
        "dev.developers-market_segments",
        str,
    ),
    Variable("projects_table_name", "PROJECTS_TABLE_NAME", "dev.projects", str),
    Variable(
        "projects_photos_table_name",
        "PROJECTS_PHOTOS_TABLE_NAME",
        "dev.projects-photos",
        str,
    ),
    Variable(
        "projects_regulations_table_name",
        "PROJECTS_REGULATIONS_TABLE_NAME",
        "dev.projects-regulations",
        str,
    ),
    Variable(
        "projects_amenities_table_name",
        "PROJECTS_AMENITIES_TABLE_NAME",
        "dev.projects-amenities",
        str,
    ),
    Variable(
        "projects_payment_methods_table_name",
        "PROJECTS_PAYMENT_METHODS_TABLE_NAME",
        "dev.projects-payment_methods",
        str,
    ),
    Variable(
        "projects_apartments_table_name",
        "PROJECTS_APARTMENTS_TABLE_NAME",
        "dev.projects-apartments",
        str,
    ),
    Variable(
        "apartments_appliances_table_name",
        "APARTMENTS_APPLIANCES_TABLE_NAME",
        "dev.apartments-appliances",
        str,
    ),
    Variable(
        "apartments_extra_features_table_name",
        "APARTMENTS_EXTRA_FEATURES_TABLE_NAME",
        "dev.apartments-extra_features",
        str,
    ),
]


@dataclass
class Environment:
    """
    This class loads in the required environment variables
    """

    rmq_connect: str
    rmq_queue: str
    db_password: str
    db_login: str
    db_host: str
    db_name: str
    apartments_table_name: str
    developers_table_name: str
    developers_projects_table_name: str
    developers_construction_types_table_name: str
    developers_documents_table_name: str
    developers_locations_table_name: str
    developers_market_segments_table_name: str
    projects_table_name: str
    projects_amenities_table_name: str
    projects_payment_methods_table_name: str
    projects_regulations_table_name: str
    projects_photos_table_name: str
    projects_apartments_table_name: str
    apartments_appliances_table_name: str
    apartments_extra_features_table_name: str

    @classmethod
    def from_environment_variables(cls) -> Environment:
        """
        Load environment variables into an Environment instance.

        Get defaults from the DEFAULTS list, and log when the defaults are used.
        """
        params = {}
        for var in DEFAULTS:
            if var.env_name in os.environ:
                constructor = var.data_type
                params[var.attr_name] = constructor(os.environ[var.env_name])
            else:
                logger.info(f"Environment variable {var.env_name} not set. Using default {var.default!r}")
                params[var.attr_name] = var.default
        return cls(**params)


ENVIRONMENT = Environment.from_environment_variables()
