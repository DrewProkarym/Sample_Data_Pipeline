import datetime as dt
import connection_credentials
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Select, Float, NVARCHAR, DateTime, SmallInteger, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

# Create connection string
connection_string = connection_credentials.get_connection_string()

# Establish connection to postgres
engine = create_engine(connection_string, echo = True)

# Create metadata object
meta_data = MetaData()

roleType = Table(
    "roleType", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False, unique=True),
    Column("Description", NVARCHAR(255), nullable=True),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

state = Table(
    "state", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Abbreviation", NVARCHAR(2), autoincrement=True, nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
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
    Column("StateId", Integer, ForeignKey('state.Id')),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

contact = Table(
    "contacts", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("FullName", NVARCHAR(255), nullable=False),
    Column("FirstName", NVARCHAR(255), nullable=False),
    Column("LastName", NVARCHAR(255), nullable=False),
    Column("EmailAddress", NVARCHAR(255), nullable=False, unique=True),
    Column("PhoneNumber", NVARCHAR(255), nullable=False, unique=True),
    Column("LocationId", Integer, ForeignKey('location.Id'), unique=True, ),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

device = Table(
    "deviceInfo", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False),
    Column("Type", NVARCHAR(255), nullable=False),
    Column("OS", NVARCHAR(255), nullable=False),
    Column("OSVersion", NVARCHAR(255), nullable=False),
    Column("Model", NVARCHAR(255), nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

payment_tiers = Table(
    "paymentTierType", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", NVARCHAR(255), nullable=False),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

user = Table(
    "user", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Username", NVARCHAR(255), nullable=False, unique=True),
    Column("Email", NVARCHAR(255), nullable=False, unique=True),
    Column("RoleTypeId", Integer, ForeignKey('roleType.Id'), nullable=False),
    Column("IsActive", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=1),
    Column("PaymentTierTypeId", SmallInteger, ForeignKey('paymentTierType.Id'), nullable=False, default=1,),
    Column("ContactId", Integer, ForeignKey('contact.Id'), unique=True),
    Column("DeviceId", Integer, ForeignKey('deviceInfo.Id'), unique=True),
    Column("LastLoginDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("CreateDateUTC", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, CheckConstraint("Deleted IN (0,1)"), nullable=False, default=0),
)

# Create tables
# meta_data.create_all(engine)
