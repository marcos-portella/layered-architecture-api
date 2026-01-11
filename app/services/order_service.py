from typing import Optional, List, Dict, Any, cast
from datetime import datetime
from mysql.connector.abstracts import MySQLConnectionAbstract
from fastapi import HTTPException
from app.models.orders import OrderUpdate, Order


class OrderService:
    """
    Serviços de gerenciamento de pedidos (Orders).
    Centraliza a lógica de vendas, estatísticas e vínculo com clientes.
    """

    @staticmethod
    def list_orders(
        user_email: str,
        db: MySQLConnectionAbstract,
        customer_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista todos os pedidos realizados, permitindo filtragem por cliente.
        """
        cursor = db.cursor(dictionary=True)

        if customer_id:
            print(
                f"Ação: Usuário {user_email} buscou os pedidos do cliente "
                f"{customer_id}"
            )

        sql = """
            SELECT o.*, c.name as customer_name
            FROM orders o
            INNER JOIN customers c ON o.customer_id = c.id
        """

        if customer_id:
            sql += " WHERE o.customer_id = %s"
            cursor.execute(sql, (customer_id,))
        else:
            cursor.execute(sql)

        results = cursor.fetchall()
        cursor.close()

        return cast(List[Dict[str, Any]], results)

    @staticmethod
    def create_order(
        order: Order, db: MySQLConnectionAbstract, user_email: str
    ) -> Dict[str, Any]:
        """
        Registra um novo pedido vinculado a um cliente existente.
        """
        cursor = db.cursor()

        print(f"Ação: Usuário {user_email} criou um pedido")

        # Regra de Integridade: O cliente deve existir para receber um pedido
        cursor.execute(
            "SELECT id FROM customers WHERE id = %s", (order.customer_id,)
        )
        if not cursor.fetchone():
            cursor.close()
            raise HTTPException(
                status_code=404, detail="Cliente não encontrado"
            )

        now = datetime.now()

        sql = """
            INSERT INTO orders (description, amount, customer_id, created_at)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            sql, (order.description, order.amount, order.customer_id, now)
        )

        db.commit()
        new_id = cursor.lastrowid
        cursor.close()

        return {
            "order_id": new_id,
            "message": "Pedido criado com sucesso!",
            "timestamp": now,
            "created_by": user_email
        }

    @staticmethod
    def update_order(
        order_id: int, order_data: OrderUpdate,
        db: MySQLConnectionAbstract, user_email: str
    ) -> Dict[str, Any]:
        """
        Atualiza as informações de um pedido específico.
        """
        cursor = db.cursor()

        print(f"Ação: Usuário {user_email} atualizou o pedido {order_id}")

        cursor.execute("SELECT id FROM orders WHERE id = %s", (order_id,))
        if not cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        sql = "UPDATE orders SET description = %s, amount = %s WHERE id = %s"
        cursor.execute(
            sql, (order_data.description, order_data.amount, order_id)
        )

        db.commit()
        cursor.close()

        return {
            "message": f"Pedido {order_id} atualizado com sucesso!",
            "order_id": order_id,
            "updated_by": user_email
        }

    @staticmethod
    def get_order_stats(
        db: MySQLConnectionAbstract, user_email: str
    ) -> Dict[str, Any]:
        """
        Calcula métricas globais de vendas: total de pedidos, receita e ticket
        médio.
        """
        cursor = db.cursor(dictionary=True)

        print(f"Ação: Usuário {user_email} buscou os status de vendas")

        sql = """
            SELECT
                COUNT(*) as total_orders,
                SUM(amount) as total_revenue,
                AVG(amount) as average_order_value
            FROM orders
        """

        cursor.execute(sql)
        raw_data = cursor.fetchone()
        stats = cast(Optional[Dict[str, Any]], raw_data)
        cursor.close()

        if not stats or stats['total_orders'] == 0:
            return {
                "total_orders": 0,
                "total_revenue": 0.0,
                "average_order_value": 0.0,
                "created_by": user_email
            }

        return {
            "total_orders": stats['total_orders'],
            "total_revenue": float(stats['total_revenue'] or 0),
            "average_order_value": float(stats['average_order_value'] or 0),
            "generated_by": user_email
        }
