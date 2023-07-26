from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#  variable holds the URL for the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"         

# create the engine that will manage the database connection/session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# generate individual sessions that will be used for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class to be inherited for all the declarative class definitions (models) that represent database tables
Base = declarative_base()
