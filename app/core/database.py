from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import dbSettings

DATABASE_URL = f"{dbSettings.db_driver}://{dbSettings.db_username}:{dbSettings.db_password}@{dbSettings.db_host}:{dbSettings.db_port}/{dbSettings.db_name}"
engine = create_engine( DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()