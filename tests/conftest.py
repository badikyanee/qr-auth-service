import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.models import User, Data

# ТЕСТОВАЯ БАЗА
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/qr_auth_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Создаём таблицы
Base.metadata.create_all(bind=engine)


# Подмена зависимости get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_client():
    return client