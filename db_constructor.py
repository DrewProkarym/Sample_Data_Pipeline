# CreateDateUTC will be created with default value of current_time UTC for the payment tier type table. Also for user role.
# Some users will be active even though they are deleted. Fix this in normalization.
# Create FullName based on a trimmed and concated first and last name.
import datetime as dt
from pytz import timezone
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Select, Float, NVARCHAR, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import MEDIUMINT, TINYINT
from sqlalchemy.sql import func

# Create connection string
username = ''
password = ''
host = ''
port = ''
database = ''
connection_string = f'postgresql+psycopg2:/{username}:{password}@{host}:{port}/{database}'

# Establish connection to postgres
# engine = create_engine(connection_string, echo = True)

# Create metadata object
meta_data = MetaData()

user = Table(
    "user", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Username", NVARCHAR(255), nullable=False, unique=True),
    Column("Email", NVARCHAR(255), nullable=False, unique=True),
    Column("RoleTypeId", Integer, nullable=False, ForeignKey=True),
    Column("IsActive", TINYINT, nullable=False, default=1),
    Column("TierTypeId", TINYINT, nullable=False, default=1, ForeignKey=True),
    Column("ContactId", Integer, ForeignKey=True, unique=True),
    Column("DeviceId", Integer, ForeignKey=True, unique=True),
    Column("LastLoginDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

roleType = Table(
    "roleType", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False, unique=True),
    Column("Description", NVARCHAR(255), nullable=True),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

contact = Table(
    "contacts", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("FullName", NVARCHAR(255), nullable=False),
    Column("FirstName", NVARCHAR(255), nullable=False),
    Column("LastName", NVARCHAR(255), nullable=False),
    Column("EmailAddress", NVARCHAR(255), nullable=False, unique=True),
    Column("PhoneNumber", NVARCHAR(255), nullable=False, unique=True),
    Column("LocationId", Integer, unique=True),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

location = Table(
    "locations", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Address", NVARCHAR(255)),
    Column("StreetAddress", NVARCHAR(255)),
    Column("City", NVARCHAR(255)),
    Column("PostalCode", NVARCHAR(255)),
    Column("Latitude", Float),
    Column("Longitude", Float),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

state = Table(
    "state", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Abbreviation", NVARCHAR(2), autoincrement=True, nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

device = Table(
    "deviceInfo", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False),
    Column("Type", NVARCHAR(255), nullable=False),
    Column("OS", NVARCHAR(255), nullable=False),
    Column("OSVersion", NVARCHAR(255), nullable=False),
    Column("Model", NVARCHAR(255), nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

payment_tiers = Table(
    "paymentTiers", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.now(timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", TINYINT, nullable=False, default=0),
)

