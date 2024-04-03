import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.core.config import dbSettings
from fastapi.testclient import TestClient
from ..app.main import app
from ..app.core.database import get_db
from ..app.models.user import User
from ..app.models.base import Base
from ..app.core.database import DATABASE_URL

engine = create_engine( DATABASE_URL )
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def override_get_db():

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture
def client(session):
    yield TestClient(app)



