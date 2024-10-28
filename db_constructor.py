import datetime as dt
import pandas as pd
import connection_credentials
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Select, Float, String, DateTime, SmallInteger
from sqlalchemy.orm import sessionmaker

# Create connection string
connection_string = connection_credentials.get_connection_string()

# Establish connection to postgres
engine = create_engine(connection_string, echo = True)

# Create metadata object
meta_data = MetaData()

roleType = Table(
    "roleType", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", String(255), nullable=False, unique=True),
    Column("Description", String(255), nullable=True),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, nullable=False, server_default="0"),
)

state = Table(
    "state", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", String(255), nullable=False),
    Column("Abbreviation", String(2), autoincrement=True, nullable=False),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, server_server_default="0"),
)

location = Table(
    "locations", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Address", String(255)),
    Column("StreetAddress", String(255)),
    Column("City", String(255)),
    Column("PostalCode", String(255)),
    Column("Latitude", Float),
    Column("Longitude", Float),
    Column("StateId", Integer, ForeignKey('state.Id')),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, server_default="0"),
)

contact = Table(
    "contacts", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("FullName", String(255), nullable=False),
    Column("FirstName", String(255), nullable=False),
    Column("LastName", String(255), nullable=False),
    Column("EmailAddress", String(255), nullable=False, unique=True),
    Column("PhoneNumber", String(255), nullable=False, unique=True),
    Column("LocationId", Integer, ForeignKey('locations.Id'), unique=True, ),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, server_default="0"),
)

device = Table(
    "deviceInfo", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", String(255), nullable=False),
    Column("Type", String(255), nullable=False),
    Column("OS", String(255), nullable=False),
    Column("OSVersion", String(255), nullable=False),
    Column("Model", String(255), nullable=False),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, server_default="0"),
)

payment_tiers = Table(
    "paymentTierType", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Name", String(255), nullable=False),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, nullable=False, server_default="0"),
)

user = Table(
    "user", meta_data,
    Column("Id", Integer, autoincrement=True, nullable=False, primary_key=True),
    Column("Username", String(255), nullable=False, unique=True),
    Column("Email", String(255), nullable=False, unique=True),
    Column("RoleTypeId", Integer, ForeignKey('roleType.Id'), nullable=False),
    Column("IsActive", SmallInteger, nullable=False, server_default="1"),
    Column("PaymentTierTypeId", SmallInteger, ForeignKey('paymentTierType.Id'), server_default="1",),
    Column("ContactId", Integer, ForeignKey('contacts.Id'), unique=True),
    Column("DeviceId", Integer, ForeignKey('deviceInfo.Id'), unique=True),
    Column("LastLoginDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("CreateDateUTC", DateTime, server_default=dt.datetime.now(dt.timezone.utc).strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]),
    Column("UpdateDateUTC", DateTime, nullable=True),
    Column("DeleteDateUTC", DateTime, nullable=True),
    Column("Deleted", SmallInteger, nullable=False, server_default="0"),
)

# Create tables
meta_data.create_all(engine)

# Update state, paymentTier, and Role tables to include server_default values using dataframes
# Create sessionmaker object
session = sessionmaker(bind=engine)()

states = pd.DataFrame({
    "Name": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
    "Abbreviation": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
})

roleType = pd.DataFrame({
    "Name": ["User", "Employee", "Admin"],
    "Description": ["Regular user account", "Employee account with some elevated privileges and benefits", "Admin account with all privilege"]
})

paymentTierType = pd.DataFrame({
    "Name": ["Basic", "Advanced", "Premium"]
})

states.to_sql('state', con=engine, if_exists='append', index=False)
roleType.to_sql('roleType', con=engine, if_exists='append', index=False)
paymentTierType.to_sql('paymentTierType', con=engine, if_exists='append', index=False)

session.commit()
session.close()