from pydantic import BaseModel, Field


class Customer(BaseModel):
    """
    Esquema de representação de um cliente no sistema.
    Inclui regras de validação para integridade de dados básicos e CPF.
    """
    name: str = Field(
        ...,
        min_length=1,
        description="Nome completo do cliente"
    )
    age: int = Field(
        ...,
        ge=0,
        description="Idade do cliente (deve ser maior ou igual a zero)"
    )
    cpf: str = Field(
        ...,
        min_length=11,
        max_length=11,
        description="CPF do cliente contendo apenas os 11 dígitos numéricos"
    )
