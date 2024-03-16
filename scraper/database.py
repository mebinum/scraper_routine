import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine, text

load_dotenv()  # take environment variables from .env.


db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
databaseURI = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def get_engine():
    return create_engine(databaseURI)


def connect():
    """
    Establishes a connection to the PostgreSQL database using SQLAlchemy and returns the connection object.
    """
    engine = get_engine()
    connection = engine.connect()
    return connection


def create_table(table_name, columns):
    """
    Executes a SQL query to create a table with the given name and columns.
    """
    with connect() as connection:
        query = f"CREATE TABLE {table_name} ({columns})"
        connection.execute(text(query))


def load_data(table_name, data):
    """
    Executes a SQL query to load the given data into the table with the given name.
    """
    with connect() as connection:
        query = f"INSERT INTO {table_name} VALUES {data}"
        connection.execute(text(query))


def verify_data(table_name, data):
    """
    Executes a SQL query to verify that the given data is loaded completely and correctly into the table with the given name.
    """
    count = 0
    with connect() as connection:
        query = f"SELECT COUNT(*) FROM {connection.dialect.identifier_preparer.quote_identifier(table_name)}"
        result = connection.execute(text(query))
        count = result.fetchone()[0]
    return count == len(data)


def flush_db():
    with get_engine().connect() as connection:
        metadata = MetaData()
        # Reflect all tables from the database
        metadata.reflect(bind=connection)

        # metadata.drop_all(bind=connection)
        # Drop all tables
        for table in metadata.tables.values():
            table.drop(bind=connection)