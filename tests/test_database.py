from unittest.mock import patch, MagicMock
import mysql.connector
from app.database import get_db_connection, get_db
import pytest
from fastapi import HTTPException
from app.dependencies.database import get_db as get_db_dep


def test_get_db_connection_error():
    with patch("mysql.connector.connect") as mock_connect:
        # Simulamos que o driver do MySQL disparou um erro
        mock_connect.side_effect = mysql.connector.Error("Conexão recusada")

        conn = get_db_connection()
        assert conn is None


def test_get_db_dependency_unavailable():
    # Simulamos que a função de conexão retornou None
    with patch("app.database.get_db_connection", return_value=None):
        generator = get_db()
        with pytest.raises(HTTPException) as exc:
            next(generator)  # Tenta pegar o banco

        assert exc.value.status_code == 503
        assert exc.value.detail == "Banco de dados temporariamente indisponível"


def test_get_db_lifecycle_full_coverage():
    # Criamos um mock para a conexão
    mock_db = MagicMock()
    mock_db.is_connected.return_value = True

    # Fazemos o get_db_connection retornar esse mock
    with patch("app.database.get_db_connection", return_value=mock_db):
        generator = get_db()

        db_yielded = next(generator)
        assert db_yielded == mock_db

        try:
            next(generator)
        except StopIteration:
            pass

    # Verifica se o close() foi realmente chamado no banco
    mock_db.close.assert_called_once()


def test_get_db_dependency_error_coverage():
    """
    Testa o tratamento de falha na conexão dentro da dependência do FastAPI.
    Utiliza patch no namespace de consumo para garantir que a exceção seja
    disparada.
    """
    with patch("app.dependencies.database.get_db_connection") as mock_conn_func:
        mock_conn_func.return_value = None

        generator = get_db_dep()
        with pytest.raises(HTTPException) as exc:
            next(generator)

        assert exc.value.status_code == 500


def test_get_db_dependency_success_lifecycle():
    mock_conn = MagicMock()
    # Forçamos o retorno da conexão fake
    with patch(
        "app.dependencies.database.get_db_connection", return_value=mock_conn
    ):
        generator = get_db_dep()
        db = next(generator)
        # Agora o assert deve passar, pois o db SERÁ o mock_conn
        assert db == mock_conn
        try:
            next(generator)
        except StopIteration:
            pass
    mock_conn.close.assert_called_once()
