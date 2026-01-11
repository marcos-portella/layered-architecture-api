from typing import Any, Dict, cast
from mysql.connector.abstracts import MySQLConnectionAbstract
from fastapi import HTTPException
from app.models.users import UserCreate
from app.dependencies.auth import HashHelper, create_access_token


class AuthService:
    """
    Gerencia a segurança e autenticação da aplicação.
    Responsável pelo ciclo de vida de usuários e geração de tokens JWT.
    """

    @staticmethod
    def create_user(
        user_data: UserCreate, db: MySQLConnectionAbstract, user_email: str
    ) -> Dict[str, Any]:
        """
        Registra um novo usuário com senha criptografada após validar o e-mail.
        """
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM users WHERE email = %s", (user_data.email,)
        )
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        # Segurança: Senhas nunca devem ser salvas em texto puro
        hashed_pwd = HashHelper.get_password_hash(user_data.password)

        sql = """
            INSERT INTO users (email, hashed_password, full_name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (user_data.email, hashed_pwd, user_data.full_name))

        db.commit()
        new_id = cursor.lastrowid
        cursor.close()

        return {
            "id": new_id,
            "email": user_data.email,
            "message": "Usuário criado com sucesso",
            "created_by": user_email
        }

    @staticmethod
    def authenticate_user(
        db: MySQLConnectionAbstract, email: str, password: str
    ) -> Dict[str, str]:
        """
        Valida as credenciais do usuário e emite um token de acesso JWT.
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cast(Dict[str, Any], cursor.fetchone())
        cursor.close()

        if not user:
            raise HTTPException(
                status_code=401, detail="E-mail ou senha incorretos"
            )

        hashed_password = cast(str, user["hashed_password"])

        if not HashHelper.verify_password(password, hashed_password):
            raise HTTPException(
                status_code=401, detail="E-mail ou senha incorretos"
            )

        token = create_access_token(data={"sub": str(user["email"])})

        return {
            "access_token": token,
            "token_type": "bearer"
        }
