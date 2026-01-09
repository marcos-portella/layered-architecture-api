import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_headers(client):  # O NOME TEM QUE SER ESTE
    email = os.getenv("TEST_USER_EMAIL", "")
    password = os.getenv("TEST_USER_PASSWORD", "")

    login_data = {"username": email, "password": password}
    response = client.post("/auth/login", data=login_data)

    if response.status_code != 200:
        pytest.fail(f"Falha no login global: {response.text}")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def clean_customer(db):
    yield  # Aqui o teste acontece
    # O código abaixo roda DEPOIS que o teste termina
    cursor = db.cursor()
    cursor.execute("DELETE FROM customers WHERE name LIKE '[TEST]%'")
    db.commit()
    cursor.close()
