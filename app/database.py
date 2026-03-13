# app/database.py
from sqlmodel import SQLModel, Session, create_engine
from app.models import PricePoint

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    """Creates the database and tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for providing database sessions."""
    with Session(engine) as session:
        yield session