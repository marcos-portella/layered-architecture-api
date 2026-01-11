from typing import Optional
from fastapi import APIRouter, Depends
from mysql.connector.abstracts import MySQLConnectionAbstract
from app.dependencies.database import get_db
from app.models.orders import Order, OrderUpdate, DashboardStats
from app.services.order_service import OrderService
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", status_code=201)
def create_order(
    order: Order,
    db: MySQLConnectionAbstract = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    """
    Registra um novo pedido no sistema vinculado a um cliente.
    """
    return OrderService.create_order(order, db, user_email)


@router.get("/")
def get_orders(
    customer_id: Optional[int] = None,
    db: MySQLConnectionAbstract = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    """
    Lista pedidos realizados, com opção de filtro por ID de cliente.
    """
    return OrderService.list_orders(user_email, db, customer_id)


@router.put("/{order_id}")
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: MySQLConnectionAbstract = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    """
    Atualiza as informações de um pedido existente (descrição e valor).
    """
    return OrderService.update_order(order_id, order_data, db, user_email)


@router.get("/stats", response_model=DashboardStats)
def get_order_stats(
    db: MySQLConnectionAbstract = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    """
    Retorna métricas consolidadas: total de vendas, receita e ticket médio.
    """
    return OrderService.get_order_stats(db, user_email)
