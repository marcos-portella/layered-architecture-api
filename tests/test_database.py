from unittest.mock import patch, MagicMock
import mysql.connector
import pytest
from fastapi import HTTPException
from app.database import get_db_connection, get_db
from app.dependencies.database import get_db as get_db_dep

"""
Testes de Infraestrutura e Resiliência de Banco de Dados
------------------------------------------------------
Este módulo utiliza Mocking para simular comportamentos da camada de dados:
- Falhas críticas de conexão (Driver MySQL).
- Indisponibilidade de serviço (HTTP 503).
- Ciclo de vida de dependências (Yield/Close).
Garante que a API trate erros de infraestrutura sem expor stack traces.
"""


def test_get_db_connection_error():
    """
    Testa a resiliência do método de conexão contra erros do driver MySQL.

    Simula um erro 'Conexão recusada' disparado pelo mysql-connector
    e valida se a função lida com a exceção retornando None.
    """
    with patch("mysql.connector.connect") as mock_connect:
        # Simula erro de baixo nível do driver
        mock_connect.side_effect = mysql.connector.Error("Conexão recusada")

        conn = get_db_connection()
        assert conn is None


def test_get_db_dependency_unavailable():
    """
    Valida a resposta HTTP 503 quando o banco está inacessível.

    Simula um cenário onde o banco retorna None na tentativa de conexão,
    forçando o gerador get_db a disparar uma exceção de serviço indisponível.
    """
    with patch("app.database.get_db_connection", return_value=None):
        generator = get_db()
        with pytest.raises(HTTPException) as exc:
            next(generator)  # Tenta obter a conexão do gerador

        assert exc.value.status_code == 503
        assert exc.value.detail == "Banco de dados temporariamente indisponível"


def test_get_db_lifecycle_full_coverage():
    """
    Valida o ciclo de vida completo de uma conexão bem-sucedida.

    Garante que após o uso do banco (yield), o gerador executa o
    bloco finally e fecha a conexão corretamente (close).
    """
    mock_db = MagicMock()
    mock_db.is_connected.return_value = True

    with patch("app.database.get_db_connection", return_value=mock_db):
        generator = get_db()
        db_yielded = next(generator)

        assert db_yielded == mock_db

        try:
            next(generator)
        except StopIteration:
            pass

    # Verifica se a conexão foi encerrada para evitar vazamento de memória
    mock_db.close.assert_called_once()


def test_get_db_dependency_error_coverage():
    """
    Testa o tratamento de falha na injeção de dependência do FastAPI.

    Mata as linhas de cobertura relacionadas ao erro 500 caso a
    conexão falhe no contexto das rotas.
    """
    with patch("app.dependencies.database.get_db_connection") as mock_conn_func:
        mock_conn_func.return_value = None

        generator = get_db_dep()
        with pytest.raises(HTTPException) as exc:
            next(generator)

        assert exc.value.status_code == 500


def test_get_db_dependency_success_lifecycle():
    """
    Garante a integridade da injeção de dependência em fluxos de sucesso.

    Verifica se o objeto injetado nas rotas é exatamente a conexão
    ativa e se ela é devidamente encerrada após a requisição.
    """
    mock_conn = MagicMock()

    with patch(
        "app.dependencies.database.get_db_connection", return_value=mock_conn
    ):
        generator = get_db_dep()
        db = next(generator)

        assert db == mock_conn

        try:
            next(generator)
        except StopIteration:
            pass

    mock_conn.close.assert_called_once()
