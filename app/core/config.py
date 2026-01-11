import os
from typing import cast
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centraliza as configurações globais da aplicação com tipagem forte.
    """
    PROJECT_NAME: str = "Meu Projeto Final"

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = cast(str, os.getenv("DB_USER"))
    DB_PASSWORD: str = cast(str, os.getenv("DB_PASSWORD"))
    DB_DATABASE: str = cast(str, os.getenv("DB_DATABASE"))

    API_KEY: str = cast(str, os.getenv("API_KEY"))


settings = Settings()

if not settings.API_KEY:
    raise RuntimeError(
        "ERRO CRÍTICO: A variável API_KEY não foi encontrada no ficheiro .env. "
        "A segurança da API depende desta chave."
    )

settings = Settings()
