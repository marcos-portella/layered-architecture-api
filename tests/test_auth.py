import os
import anyio
import random
import pytest
from jose import jwt
from fastapi import HTTPException
from typing import cast
from mysql.connector.abstracts import MySQLConnectionAbstract

from app.dependencies.auth import get_api_key, get_current_user
from app.services.auth_service import AuthService
from app.models.users import UserCreate
from app.database import get_db_connection

"""
Testes de Autenticação e Segurança - Módulo de Auditoria
-------------------------------------------------------
Este módulo valida os mecanismos de proteção da API, incluindo:
- Validação de credenciais de Login (E-mail/Senha).
- Restrição de duplicidade de usuários.
- Integridade de Tokens JWT e chaves de API (API Key).
- Testes unitários diretos na camada de Service.
"""


def test_login_invalid_email(client):
    """
    Valida a rejeição de login para e-mails não cadastrados.

    Espera-se Status 401 e mensagem de erro genérica por segurança.
    """
    data = {"username": "nao_existo_mesmo@gmail.com", "password": "123"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_login_wrong_password(client):
    """
    Valida a rejeição de login para senhas incorretas em usuários válidos.
    """
    email = os.getenv("TEST_USER_EMAIL")
    data = {"username": email, "password": "senha_totalmente_errada"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"


def test_create_duplicate_user(client, auth_headers):
    """
    Verifica a restrição de unicidade do campo e-mail.

    Tenta registrar um usuário que já existe no banco de dados.
    """
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
    """
    Teste unitário de baixo nível da camada AuthService.

    Realiza o setup manual da conexão com o MySQL para validar a
    lógica de criação de usuários sem passar pela rota HTTP.
    """
    # 1. SETUP MANUAL DA CONEXÃO
    raw_db = get_db_connection()

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
        # 2. EXECUÇÃO DIRETA NO SERVICE
        result = AuthService.create_user(
            user_data=user_in,
            db=db,
            user_email="admin@sistema.com"
        )

        # 3. VALIDAÇÃO
        assert result["email"] == test_email
        assert "sucesso" in result["message"].lower()

    finally:
        # 4. LIMPEZA DE DADOS
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (test_email,))
        db.commit()
        cursor.close()
        db.close()


def test_get_api_key_manual_coverage():
    """
    Testa a dependência get_api_key usando anyio para execução assíncrona.

    Cobre as ramificações de sucesso (chave correta) e falha (chave incorreta).
    """
    # 1. Testando a Falha (Erro 403 Forbidden)
    with pytest.raises(HTTPException) as exc:
        anyio.run(get_api_key, "CHAVE_ERRADA")
    assert exc.value.status_code == 403

    # 2. Testando o Sucesso
    from app.dependencies.auth import API_KEY
    if API_KEY:
        result = anyio.run(get_api_key, API_KEY)
        assert result == API_KEY


def test_get_current_user_invalid_token_coverage():
    """
    Valida a robustez do decodificador JWT contra tokens malformados.

    Cobre os casos de tokens que não são JWT e tokens válidos mas
    sem a identificação do usuário (Subject/Sub).
    """
    # 1. Testa JWTError (Mala-formação)
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token_totalmente_invalido_e_nao_jwt")
    assert exc.value.status_code == 401

    # 2. Testa payload sem 'sub' (E-mail ausente)
    from app.dependencies.auth import SECRET_KEY, ALGORITHM
    token_sem_sub = jwt.encode(
        {"payload_aleatorio": "oi"}, SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(HTTPException) as exc:
        get_current_user(token=token_sem_sub)
    assert exc.value.status_code == 401
