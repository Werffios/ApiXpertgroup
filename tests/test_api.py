# test/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.database import Base, get_db
from unittest.mock import patch # Required for mocking the OpenAI service

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db # Importante, sobrescribe a get_db para usar la base de datos de prueba

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_init_user(db_session):
    response = client.post("/init_user", json={"username": "testuser", "role": "expert"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "expert"
    assert "id" in data


@patch("app.services.openai_service.get_chatbot_response")
def test_ask(mock_get_gepeto_response, db_session):
    mock_get_gepeto_response.return_value = "La capital de Francia es París."

    client.post("/init_user", json={"username": "testuser", "role": "expert"})

    # Test the /ask endpoint
    response = client.post("/ask?username=testuser", json={"message": "¿Cuál es la capital de Francia?"})
    assert response.status_code == 200
    assert response.json() == {"response": "La capital de Francia es París."} # Verifica que la respuesta sea la esperada
