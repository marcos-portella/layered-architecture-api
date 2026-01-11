from typing import Generator
from fastapi import HTTPException
from app.database import get_db_connection


def get_db() -> Generator:
    """
    Gerencia o ciclo de vida da conexão com o banco de dados para cada
    requisição.
    Abre a conexão no início e garante o fechamento ao final (yield/finally).
    """
    connection = get_db_connection()

    if connection is None:
        raise HTTPException(
            status_code=500, detail="Database connection failed"
        )

    try:
        yield connection
    finally:
        # Garante que a conexão retorne ao pool ou seja encerrada,
        # evitando vazamento de recursos (memory leaks).
        connection.close()
