from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class Order(BaseModel):
    """
    Representa a estrutura básica de um pedido no sistema.
    """
    description: str = Field(
        ..., description="Descrição detalhada dos itens do pedido"
    )
    amount: float = Field(
        ..., gt=0, description="O valor do pedido deve ser maior que zero"
    )
    customer_id: int = Field(
        ..., description="ID de referência do cliente proprietário do pedido"
    )


class OrderResponse(Order):
    """
    Extensão do modelo de pedido para exibição, incluindo dados gerados pelo
    sistema.
    """
    id: int
    created_at: datetime
    customer_name: str

    model_config = ConfigDict(from_attributes=True)


class OrderUpdate(BaseModel):
    """
    Esquema para atualização parcial ou total de dados de um pedido.
    """
    description: str
    amount: float


class DashboardStats(BaseModel):
    """
    Modelo para retorno de métricas financeiras e de volume de vendas.
    """
    total_orders: int
    total_revenue: float
    average_order_value: float
