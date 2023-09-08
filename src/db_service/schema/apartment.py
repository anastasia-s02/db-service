from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text

from db_service.connect import METADATA
from db_service.environment import ENVIRONMENT


@dataclass
class Apartment:
    """
    Class for keeping track of apartment unit.
    """

    id: int
    floor_plan: Optional[str]
    apartment_plan: Optional[int]
    property_type: Optional[str]
    building_number: Optional[str]
    entrance_number: Optional[str]
    floor: Optional[str]
    apartment_number: Optional[str]
    apartment_status: Optional[str]
    apartment_type: Optional[str]
    total_area: Optional[float]
    total_internal_area: Optional[float]
    total_external_area: Optional[float]
    balcony_type: Optional[str]
    total_price: Optional[float]
    appliances: Optional[list[str]]
    extra_features: Optional[list[str]]
    developer_name: str
    project_name: str
    location: Optional[str]
    completion_date: Optional[str]
    price_per_ft: Optional[float]
    dld_charge: Optional[str]
    transaction_costs: Optional[str]
    service_charge_per_sqft_per_year: Optional[float]
    time_to_beach: Optional[float]
    time_to_downtown: Optional[float]
    time_to_school: Optional[float]
    time_to_hospital: Optional[float]
    time_to_airport: Optional[float]
    time_to_marina: Optional[float]
    time_to_mall: Optional[float]
    amenities: Optional[list[str]]
    regulation: Optional[list[str]]


APARTMENTS_TABLE = Table(
    ENVIRONMENT.apartments_table_name,
    METADATA,
    Column("id", Integer, primary_key=True),
    Column("floor_plan", String(20)),
    Column("property_type", String(20)),
    Column("building_number", String(20)),
    Column("entrance_number", String(20)),
    Column("floor", String(20)),
    Column("apartment_number", String(20)),
    Column("apartment_status", String(60)),
    Column("apartment_type", String(60)),
    Column("total_area", Float),
    Column("total_internal_area", Float),
    Column("total_external_area", Float),
    Column("balcony_type", String(60)),
    Column("total_price", Float),
)

APARTMENTS_APPLIANCES_TABLE = Table(
    ENVIRONMENT.apartments_appliances_table_name,
    METADATA,
    Column(
        "apartment",
        Integer,
        ForeignKey(f"{ENVIRONMENT.apartments_table_name}.id"),
        primary_key=True,
    ),
    Column("appliance", Text, primary_key=True),
)

APARTMENTS_EXTRA_FEATURES_TABLE = Table(
    ENVIRONMENT.apartments_extra_features_table_name,
    METADATA,
    Column(
        "apartment",
        Integer,
        ForeignKey(f"{ENVIRONMENT.apartments_table_name}.id"),
        primary_key=True,
    ),
    Column("extra_feature", Text, primary_key=True),
)

APARTMENTS_COLUMNS = {
    "id": APARTMENTS_TABLE.c.id,
    "floor_plan": APARTMENTS_TABLE.c.floor_plan,
    "property_type": APARTMENTS_TABLE.c.property_type,
    "building_number": APARTMENTS_TABLE.c.building_number,
    "entrance_number": APARTMENTS_TABLE.c.entrance_number,
    "floor": APARTMENTS_TABLE.c.floor,
    "apartment_number": APARTMENTS_TABLE.c.apartment_number,
    "apartment_status": APARTMENTS_TABLE.c.apartment_status,
    "total_area": APARTMENTS_TABLE.c.total_area,
    "total_internal_area": APARTMENTS_TABLE.c.total_internal_area,
    "total_external_area": APARTMENTS_TABLE.c.total_external_area,
    "balcony_type": APARTMENTS_TABLE.c.balcony_type,
    "total_price": APARTMENTS_TABLE.c.total_price,
}

APARTMENT_COLUMN_TO_TABLE = {
    "appliances": APARTMENTS_APPLIANCES_TABLE,
    "extra_features": APARTMENTS_EXTRA_FEATURES_TABLE,
    **{column_name: APARTMENTS_TABLE for column_name in APARTMENTS_COLUMNS},
}
