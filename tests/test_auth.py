import os
import anyio
import random
import pytest
from jose import jwt
from fastapi import HTTPException
from typing import cast
from app.dependencies.auth import get_api_key, get_current_user
from mysql.connector.abstracts import MySQLConnectionAbstract
from app.services.auth_service import AuthService
from app.models.users import UserCreate
from app.database import get_db_connection


def test_login_invalid_email(client):
    # Testa e-mail que não existe no banco
    data = {"username": "nao_existo_mesmo@gmail.com", "password": "123"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_login_wrong_password(client):
    # Testa senha errada para usuário existente
    email = os.getenv("TEST_USER_EMAIL")
    data = {"username": email, "password": "senha_totalmente_errada"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_create_duplicate_user(client, auth_headers):
    # Tenta criar um usuário com e-mail já cadastrado
    # Usando o e-mail que está no seu .env
    email = os.getenv("TEST_USER_EMAIL")
    payload = {
        "email": email,
        "password": "123456",
        "full_name": "[TEST] Marcos Duplicado"
    }
    response = client.post("/auth/register", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail já cadastrado"


def test_auth_service_creation_manual_root():
    # 1. SETUP MANUAL DA CONEXÃO
    raw_db = get_db_connection()

    # Garantimos que o db existe antes de prosseguir
    if raw_db is None:
        raise Exception("Não foi possível conectar ao banco de dados")

    db = cast(MySQLConnectionAbstract, raw_db)

    random_id = random.randint(1000, 9999)
    test_email = f"root_test_{random_id}@gmail.com"

    user_in = UserCreate(
        email=test_email,
        password="senha_raiz_123",
        full_name="Marcos Root Explorer"
    )

    try:
        # 2. EXECUÇÃO DIRETA NO SERVICE (Agora o Pylance fica feliz)
        result = AuthService.create_user(
            user_data=user_in,
            db=db,
            user_email="admin@sistema.com"
        )

        # 3. VALIDAÇÃO
        assert result["email"] == test_email
        assert "sucesso" in result["message"].lower()

    finally:
        # 4. LIMPEZA (Sempre feche o raw_db original)
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (test_email,))
        db.commit()
        cursor.close()
        db.close()


# 1. MATANDO AS LINHAS 20-26 (API KEY)
def test_get_api_key_manual_coverage():
    """
    Testa a API Key usando anyio para rodar a função async.
    Mata as linhas 20-23.
    """
    # 1. Testando a Falha (Linhas 23-26)
    with pytest.raises(HTTPException) as exc:
        anyio.run(get_api_key, "CHAVE_ERRADA")
    assert exc.value.status_code == 403

    # 2. Testando o Sucesso (Linhas 20-23)
    # Importamos o valor real do seu código para bater com o IF
    from app.dependencies.auth import API_KEY
    if API_KEY:
        result = anyio.run(get_api_key, API_KEY)
        assert result == API_KEY


# 2. MATANDO AS LINHAS 80, 83-84 (JWT EXPLODINDO)
def test_get_current_user_invalid_token_coverage():
    # Testa JWTError (Linhas 83-84) - Mandando um token que é apenas um texto
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token_totalmente_invalido_e_nao_jwt")
    assert exc.value.status_code == 401

    # Testa email is None (Linha 80) - Token válido mas sem 'sub'
    from app.dependencies.auth import SECRET_KEY, ALGORITHM
    token_sem_sub = jwt.encode(
        {"payload_aleatorio": "oi"}, SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(HTTPException) as exc:
        get_current_user(token=token_sem_sub)
    assert exc.value.status_code == 401
