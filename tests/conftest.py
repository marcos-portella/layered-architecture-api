import os
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app

load_dotenv()

"""
Configurações de Teste e Fixtures - Pytest
-----------------------------------------
Este módulo centraliza as fixtures do Pytest para garantir um ambiente
de teste isolado, autenticado e com limpeza automática de dados.
"""


@pytest.fixture(scope="session")
def client():
    """
    Cria uma instância do TestClient do FastAPI para toda a sessão de testes.

    Yields:
        TestClient: Cliente de teste para realizar chamadas HTTP.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client):
    """
    Realiza o login global e gera os headers de autenticação JWT.

    Utiliza as credenciais de teste definidas no arquivo .env para obter
    um token de acesso válido para as rotas protegidas.

    Args:
        client (TestClient): O cliente de teste instanciado.

    Returns:
        dict: Dicionário contendo o header de Authorization com o Bearer Token.
    """
    email = os.getenv("TEST_USER_EMAIL", "")
    password = os.getenv("TEST_USER_PASSWORD", "")

    login_data = {"username": email, "password": password}
    response = client.post("/auth/login", data=login_data)

    if response.status_code != 200:
        pytest.fail(f"❌ Falha no login global de teste: {response.text}")

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def clean_customer(db):
    """
    Fixture de limpeza (Teardown) para registros de clientes.

    Executa o teste e, após a finalização, remove qualquer cliente
    cujo nome comece com '[TEST]' para manter o banco de dados limpo.

    Args:
        db: Conexão com o banco de dados injetada.
    """
    yield  # Execução do teste

    # Código de limpeza pós-teste
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE name LIKE '[TEST]%'")
        db.commit()
    except Exception as e:
        print(f"⚠️ Erro ao limpar dados de teste: {e}")
        db.rollback()
    finally:
        cursor.close()
