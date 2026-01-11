from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from mysql.connector.abstracts import MySQLConnectionAbstract
from app.models.users import UserCreate
from app.services.auth_service import AuthService
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def create_user(
    user_data: UserCreate,
    db: MySQLConnectionAbstract = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    """
    Cadastra um novo administrador no sistema.
    Requer que o solicitante já possua um token de acesso válido.
    """
    return AuthService.create_user(user_data, db, user_email)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: MySQLConnectionAbstract = Depends(get_db)
):
    """
    Autentica o usuário e retorna um token JWT (Bearer).
    O campo 'username' deve ser preenchido com o e-mail do usuário.
    """
    return AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )
