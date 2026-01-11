from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    """
    Esquema para criação de um novo administrador.
    Inclui a senha em texto puro para processamento inicial de hash.
    """
    email: EmailStr = Field(
        ..., description="Endereço de e-mail único do usuário"
    )
    password: str = Field(
        ..., min_length=6, description="Senha de acesso (mínimo 6 caracteres)"
    )
    full_name: str = Field(
        ..., description="Nome completo do administrador"
    )


class UserResponse(BaseModel):
    """
    Esquema de resposta para dados do usuário.
    Não inclui campos sensíveis como senhas.
    """
    id: int
    email: EmailStr = Field(
        ..., description="Endereço de e-mail único do usuário"
    )
    full_name: str = Field(
        ..., description="Nome completo do administrador"
    )

    model_config = ConfigDict(from_attributes=True)
