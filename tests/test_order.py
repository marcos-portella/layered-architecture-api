import pytest
import random
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db_connection
from app.services.order_service import OrderService

"""
Testes de Integração e Cobertura - Módulo de Pedidos (Orders)
------------------------------------------------------------
Este módulo valida o ciclo de vida completo de pedidos, desde a criação
vinculada a clientes até a geração de métricas para o dashboard, garantindo
100% de cobertura nas camadas de Router e Service.
"""

client = TestClient(app)


def test_create_order_success(auth_headers):
    """
    Testa a criação bem-sucedida de um pedido vinculado a um cliente válido.
    Verifica se o retorno apresenta o Status 201 e a mensagem de sucesso.
    """
    payload = {"name": "Test User ID", "age": 40, "cpf": "00000000010"}

    response = client.post("/customers/", json=payload, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    new_id = data.get("id")

    assert new_id is not None
    assert data["message"] == "Customer created successfully"
    assert data["data"]["name"] == payload["name"]

    try:
        payload_order = {
            "description": "Pedido de Teste Marcos",
            "amount": 150.50,
            "customer_id": new_id
        }

        response = client.post(
            "/orders/", json=payload_order, headers=auth_headers
        )
        assert response.status_code == 201
        assert "Pedido criado com sucesso" in response.json()["message"]

    finally:
        conn = get_db_connection()
        if conn is not None:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM customers WHERE id = %s", (new_id,)
                    )
                conn.commit()
            finally:
                conn.close()
        else:
            pytest.fail(
                "Não foi possível conectar ao banco para limpeza do teste."
            )


def test_orders_dashboard_stats(auth_headers):
    """
    Valida o endpoint de estatísticas do dashboard.
    Verifica a existência das chaves de receita e total de pedidos.
    """
    response = client.get("/orders/stats", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "total_revenue" in data
    assert "total_orders" in data
    assert isinstance(data["total_revenue"], float)


def test_create_order_invalid_customer(auth_headers):
    """
    Valida o erro 404 ao tentar criar pedido para um cliente inexistente.
    """
    payload = {
        "description": "Pedido Fantasma",
        "amount": 100.0,
        "customer_id": 999999
    }
    response = client.post("/orders/", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert "Cliente não encontrado" in response.json()["detail"]


def test_create_order_negative_amount(auth_headers):
    """
    Testa a validação de esquema (Pydantic) para valores negativos.
    """
    payload = {"name": "Test User ID", "age": 40, "cpf": "00000002323"}
    response = client.post("/customers/", json=payload, headers=auth_headers)
    new_id = response.json().get("id")

    try:
        payload_order = {
            "description": "Pedido Grátis",
            "amount": -50.0,
            "customer_id": new_id
        }
        response = client.post(
            "/orders/", json=payload_order, headers=auth_headers
        )
        assert response.status_code == 422
    finally:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM customers WHERE id = %s", (new_id,))
            conn.commit()
            conn.close()


def test_get_stats_without_auth():
    """Valida que o acesso às estatísticas exige autenticação Bearer."""
    response = client.get("/orders/stats")
    assert response.status_code == 401


def test_update_order_not_found(client, auth_headers):
    """Cobre a exceção de pedido não encontrado durante o update."""
    payload = {"description": "Teste", "amount": 100.0}
    response = client.put("/orders/999999", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


def test_create_order_customer_not_found(client, auth_headers):
    """
    Reforça a cobertura para criação de pedidos com IDs de clientes órfãos.
    """
    payload = {"description": "Fantasma", "amount": 50.0, "customer_id": 999999}
    response = client.post("/orders/", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"


def test_list_orders_with_filter(client, auth_headers):
    """Cobre o fluxo de listagem com filtro por customer_id."""
    response = client.get("/orders/?customer_id=1", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_all_orders_coverage(auth_headers, client):
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order_stats_empty_db():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    service = OrderService()
    result = service.get_order_stats(mock_db, "marcos@teste.com")

    assert result["total_orders"] == 0
    assert result["total_revenue"] == 0.0


def test_order_full_lifecycle_coverage(client, auth_headers):
    """
    Cobre o ciclo de vida completo e atinge as linhas de Update/Delete no
    Service.
    Utiliza CPFs aleatórios para evitar conflitos de integridade.
    """
    random_cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
    c_res = client.post(
        "/customers/",
        json={"name": "Marcos Teste", "age": 30, "cpf": random_cpf},
        headers=auth_headers
    )
    customer_id = c_res.json()["id"]

    o_payload = {
        "description": "Teste Update",
        "amount": 50.0,
        "customer_id": customer_id
    }
    o_res = client.post("/orders/", json=o_payload, headers=auth_headers)
    order_id = o_res.json()["order_id"]

    # Teste de Update (Alvo: linhas de sucesso do Service)
    u_payload = {"description": "Atualizado", "amount": 99.99}
    u_res = client.put(
        f"/orders/{order_id}", json=u_payload, headers=auth_headers
    )
    assert u_res.status_code == 200
    assert u_res.json()["order_id"] == order_id

    # Cleanup
    client.delete(f"/orders/{order_id}", headers=auth_headers)
    client.delete(f"/customers/{customer_id}", headers=auth_headers)


def test_get_order_stats_with_data(auth_headers, client):
    """
    Garante que as estatísticas sejam calculadas e o banco limpo após o teste.
    """
    random_cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
    cust_id = None

    try:
        # 1. Cria um cliente e um pedido
        c_res = client.post(
            "/customers/",
            json={"name": "Stat User", "age": 25, "cpf": random_cpf},
            headers=auth_headers
        )
        cust_id = c_res.json()["id"]

        client.post(
            "/orders/",
            json={
                "description": "Venda Real",
                "amount": 100.0,
                "customer_id": cust_id},
            headers=auth_headers
        )

        # 2. Valida estatísticas
        response = client.get("/orders/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total_orders"] > 0
        assert data["total_revenue"] >= 100.0

    finally:
        # 3. LIMPEZA: Remove o cliente (o CASCADE removerá o pedido
        # automaticamente)
        if cust_id:
            client.delete(f"/customers/{cust_id}", headers=auth_headers)
