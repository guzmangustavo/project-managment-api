import os

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Creates the database and all tables defined in the SQLModel metadata.

    This function uses the SQLModel engine to connect to the database and 
    create all the tables that are mapped to SQLModel models.

    Returns:
        None
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provides a session for database operations.

    This function creates a new database session using the SQLModel engine. 
    The session is used to interact with the database and is automatically 
    closed when the operations are complete.

    Yields:
        Session: A SQLModel session for interacting with the database.
    """
    with Session(engine) as session:
        yield session