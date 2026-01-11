import os
from typing import cast
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# Configurações de Segurança
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-KEY"
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_padrao_para_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Valida a presença e integridade da API Key nos headers da requisição.
    """
    if api_key_header == API_KEY and API_KEY is not None:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acesso negado: API Key inválida ou ambiente não configurado"
    )


class HashHelper:
    """
    Utilitário para processamento de hashes de senhas utilizando BCrypt.
    """
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Compara uma senha em texto puro com um hash armazenado.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Gera um hash seguro a partir de uma senha em texto puro.
        """
        return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    Gera um token JWT assinado com tempo de expiração configurado.
    """
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decodifica o token JWT e extrai a identidade do usuário (e-mail).
    Utilizado como dependência para proteger rotas privadas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = cast(str, payload.get("sub"))

        if email is None:
            raise credentials_exception

        return email
    except JWTError:
        raise credentials_exception
