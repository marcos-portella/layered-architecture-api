import pytest
import random
from app.services.order_service import OrderService
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.database import get_db_connection

client = TestClient(app)


def test_create_order_success(auth_headers):
    payload = {"name": "Test User ID", "age": 40, "cpf": "00000000010"}

    response = client.post("/customers/", json=payload, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    new_id = data.get("id")

    assert new_id is not None
    assert data["message"] == "Customer created successfully"
    assert data["data"]["name"] == payload["name"]

    try:
        payload = {
            "description": "Pedido de Teste Marcos",
            "amount": 150.50,
            "customer_id": new_id
        }

        response = client.post("/orders/", json=payload, headers=auth_headers)
        assert response.status_code == 200
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
                "Não foi possível conectar ao banco para limpar o rastro "
                "do teste.")


def test_orders_dashboard_stats(auth_headers):
    response = client.get("/orders/stats", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    # Verificamos se as chaves que o SQL retorna existem
    assert "total_revenue" in data
    assert "total_orders" in data
    assert isinstance(data["total_revenue"], float)


def test_create_order_invalid_customer(auth_headers):
    payload = {
        "description": "Pedido Fantasma",
        "amount": 100.0,
        "customer_id": 999999  # ID que não existe
    }
    response = client.post("/orders/", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert "Cliente não encontrado" in response.json()["detail"]


def test_create_order_negative_amount(auth_headers):
    payload = {"name": "Test User ID", "age": 40, "cpf": "00000002323"}

    response = client.post("/customers/", json=payload, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    new_id = data.get("id")

    assert new_id is not None
    assert data["message"] == "Customer created successfully"
    assert data["data"]["name"] == payload["name"]

    try:
        payload = {
            "description": "Pedido Grátis",
            "amount": -50.0,
            "customer_id": new_id
        }
        response = client.post("/orders/", json=payload, headers=auth_headers)
        assert response.status_code == 422  # Erro de validação

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
                "Não foi possível conectar ao banco para limpar o rastro "
                "do teste.")


def test_get_stats_without_auth():
    # Aqui NÃO passamos o auth_headers
    response = client.get("/orders/stats")
    assert response.status_code == 401


# 1. Testar erro ao atualizar pedido inexistente
def test_update_order_not_found(client, auth_headers):
    # ID 999999 não deve existir
    payload = {"description": "Teste", "amount": 100.0}
    response = client.put("/orders/999999", json=payload, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


# 2. Testar erro ao criar pedido para cliente inexistente
def test_create_order_customer_not_found(client, auth_headers):
    payload = {
        "description": "Pedido Fantasma",
        "amount": 50.0,
        "customer_id": 999999  # Cliente que não existe
    }
    response = client.post("/orders/", json=payload, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"


# 3. Testar listagem com filtro de cliente

def test_list_orders_with_filter(client, auth_headers):
    # Testa o 'if customer_id:' do seu list_orders
    response = client.get("/orders/?customer_id=1", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 1. Mata a Linha 34: Listar todos os pedidos (sem customer_id)
def test_list_all_orders_coverage(auth_headers, client):
    # Basta chamar o GET orders sem o parâmetro de query
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. Mata as Linhas 144-149: Estatísticas sem nenhum pedido
def test_get_order_stats_empty_db(auth_headers):
    # Aqui vamos usar o Mock para simular o banco retornando NADA (None)
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor

    # Simulando fetchone() retornando None (tabela vazia)
    mock_cursor.fetchone.return_value = None

    service = OrderService()
    result = service.get_order_stats(mock_db, "marcos@teste.com")

    assert result["total_orders"] == 0
    assert result["total_revenue"] == 0.0
    # Isso garante que o código passou pelo bloco 'if not stats'


def test_order_full_lifecycle_coverage(client, auth_headers):
    # Gerar um CPF aleatório para evitar o erro 400 de duplicata
    random_cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])

    # 1. CRIAR UM CLIENTE DO ZERO
    c_payload = {"name": "Marcos Teste", "age": 30, "cpf": random_cpf}
    c_res = client.post("/customers/", json=c_payload, headers=auth_headers)

    # Verificação de segurança: se não for 201, o teste para aqui com erro claro
    assert c_res.status_code == 200, f"Erro ao criar cliente: {c_res.json()}"
    customer_id = c_res.json()["id"]

    # 2. CRIAR UM PEDIDO PARA ESSE CLIENTE
    o_payload = {
        "description": "Pedido para Testar Update",
        "amount": 50.0,
        "customer_id": customer_id
    }
    o_res = client.post("/orders/", json=o_payload, headers=auth_headers)
    assert o_res.status_code == 200
    order_id = o_res.json()["order_ id"]

    # 3. ATUALIZAR O PEDIDO (Alvo: linhas 61-73)
    u_payload = {"description": "Pedido Atualizado", "amount": 99.99}
    u_res = client.put(
        f"/orders/{order_id}", json=u_payload, headers=auth_headers
    )

    # 4. VALIDAÇÕES
    assert u_res.status_code == 200
    assert u_res.json()["order_id"] == order_id

    # 5. LIMPEZA (Ordem inversa: pedido primeiro, depois cliente)
    client.delete(f"/orders/{order_id}", headers=auth_headers)
    client.delete(f"/customers/{customer_id}", headers=auth_headers)
