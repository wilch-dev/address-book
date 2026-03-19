from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float
import os

# SQLite database URL
DATABASE_URL = "sqlite:///./address_book.db"

# Create engine with proper settings for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Ensure database file has proper permissions
db_path = "./address_book.db"
if os.path.exists(db_path):
    os.chmod(db_path, 0o666)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class Address(Base):
    """Address model for SQLite database"""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
