from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text

from db_service.connect import METADATA
from db_service.environment import ENVIRONMENT


@dataclass
class Project:
    """
    Class for keeping track of project unit.
    """

    id: int
    name: Optional[str]
    photos: Optional[list[str]]
    location: Optional[str]
    description: Optional[str]
    num_floors: Optional[int]
    total_apartments: Optional[int]
    completion_date: Optional[str]
    completion_status: Optional[bool]
    start_of_sales: Optional[str]
    installment_plan: Optional[str]
    payment_methods: Optional[list[str]]
    finishing: Optional[str]
    furnishing: Optional[str]
    dld_charge: Optional[str]
    transaction_costs: Optional[str]
    service_charge_per_sqft_per_year: Optional[float]
    escrow: Optional[bool]
    commision_condition: Optional[str]
    regulation: Optional[list[str]]
    time_to_beach: Optional[float]
    time_to_downtown: Optional[float]
    time_to_school: Optional[float]
    time_to_hospital: Optional[float]
    time_to_airport: Optional[float]
    time_to_marina: Optional[float]
    time_to_mall: Optional[float]
    amenities: Optional[list[str]]
    parking: Optional[bool]
    parking_type: Optional[str]
    parking_spots_per_apartment: Optional[int]
    agent_commission: Optional[float]
    commission_deadline: Optional[int]
    developer_name: Optional[str]
    available_apartments: Optional[int]
    apartment_types: Optional[list[str]]
    total_area: Optional[float]
    total_price: Optional[float]
    price_per_sqft: Optional[float]


PROJECTS_TABLE = Table(
    ENVIRONMENT.projects_table_name,
    METADATA,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("location", Text),
    Column("description", Text),
    Column("num_floors", Integer),
    Column("total_apartments", Integer),
    Column("completion_date", String(30)),
    Column("completion_status", Boolean),
    Column("start_of_sales", String(30)),
    Column("installment_plan", Text),
    Column("finishing", String(30)),
    Column("furnishing", String(30)),
    Column("dld_charge", String(20)),
    Column("transaction_costs", String(30)),
    Column("service_charge_per_sqft_per_year", Float),
    Column("commision_condition", Text),
    Column("escrow", Boolean),
    Column("time_to_beach", Float),
    Column("time_to_downtown", Float),
    Column("time_to_school", Float),
    Column("time_to_hospital", Float),
    Column("time_to_airport", Float),
    Column("time_to_marina", Float),
    Column("time_to_mall", Float),
    Column("parking", Boolean),
    Column("parking_type", String(60)),
    Column("parking_spots_per_apartment", Integer),
    Column("agent_commission", Float),
    Column("commission_deadline", Integer),
)

PROJECTS_PHOTOS_TABLE = Table(
    ENVIRONMENT.projects_photos_table_name,
    METADATA,
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "photo",
        String(20),
        primary_key=True,
    ),
)

PROJECTS_PAYMENT_METHODS_TABLE = Table(
    ENVIRONMENT.projects_payment_methods_table_name,
    METADATA,
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "payment_method",
        String(60),
        primary_key=True,
    ),
)

PROJECTS_REGULATIONS_TABLE = Table(
    ENVIRONMENT.projects_regulations_table_name,
    METADATA,
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "regulation",
        String(20),
        primary_key=True,
    ),
)

PROJECTS_AMENITIES_TABLE = Table(
    ENVIRONMENT.projects_amenities_table_name,
    METADATA,
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "amenity",
        String(60),
        primary_key=True,
    ),
)

PROJECTS_APARTMENTS_TABLE = Table(
    ENVIRONMENT.projects_apartments_table_name,
    METADATA,
    Column(
        "project",
        Integer,
        ForeignKey(f"{ENVIRONMENT.projects_table_name}.id"),
        primary_key=True,
    ),
    Column(
        "apartment",
        Integer,
        ForeignKey(f"{ENVIRONMENT.apartments_table_name}.id"),
        primary_key=True,
    ),
)

PROJECTS_COLUMNS = {
    "id": PROJECTS_TABLE.c.id,
    "name": PROJECTS_TABLE.c.name,
    "num_floors": PROJECTS_TABLE.c.num_floors,
    "location": PROJECTS_TABLE.c.location,
    "description": PROJECTS_TABLE.c.description,
    "total_apartments": PROJECTS_TABLE.c.total_apartments,
    "completion_date": PROJECTS_TABLE.c.completion_date,
    "completion_status": PROJECTS_TABLE.c.completion_status,
    "start_of_sales": PROJECTS_TABLE.c.start_of_sales,
    "installment_plan": PROJECTS_TABLE.c.installment_plan,
    "finishing": PROJECTS_TABLE.c.finishing,
    "furnishing": PROJECTS_TABLE.c.furnishing,
    "dld_charge": PROJECTS_TABLE.c.dld_charge,
    "transaction_costs": PROJECTS_TABLE.c.transaction_costs,
    "service_charge_per_sqft_per_year": PROJECTS_TABLE.c.service_charge_per_sqft_per_year,
    "escrow": PROJECTS_TABLE.c.escrow,
    "commision_condition": PROJECTS_TABLE.c.commision_condition,
    "time_to_beach": PROJECTS_TABLE.c.time_to_beach,
    "time_to_downtown": PROJECTS_TABLE.c.time_to_downtown,
    "time_to_school": PROJECTS_TABLE.c.time_to_school,
    "time_to_hospital": PROJECTS_TABLE.c.time_to_hospital,
    "time_to_airport": PROJECTS_TABLE.c.time_to_airport,
    "time_to_marina": PROJECTS_TABLE.c.time_to_marina,
    "time_to_mall": PROJECTS_TABLE.c.time_to_mall,
    "parking": PROJECTS_TABLE.c.parking,
    "parking_type": PROJECTS_TABLE.c.parking_type,
    "parking_spots_per_apartment": PROJECTS_TABLE.c.parking_spots_per_apartment,
    "agent_commission": PROJECTS_TABLE.c.agent_commission,
    "commission_deadline": PROJECTS_TABLE.c.commission_deadline,
}

PROJECT_COLUMN_TO_TABLE = {
    "photos": PROJECTS_PHOTOS_TABLE,
    "payment_methods": PROJECTS_PAYMENT_METHODS_TABLE,
    "regulation": PROJECTS_REGULATIONS_TABLE,
    "amenities": PROJECTS_AMENITIES_TABLE,
    **{column_name: PROJECTS_TABLE for column_name in PROJECTS_COLUMNS},
}
