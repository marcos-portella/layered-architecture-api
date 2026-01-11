import pytest
from app.database import get_db_connection

"""
Testes de Integração - Endpoints de Clientes
-------------------------------------------
Validação das operações de CRUD e integridade da API de Clientes.
Garante que as regras de negócio e status codes estejam corretos.
"""


def test_root_status(auth_headers, client):
    """
    Testa a rota raiz da API (Health Check).

    Verifica se o endpoint principal está online e retornando a
    mensagem de monitoramento correto com Status 200.
    """
    response = client.get("/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "API Online - Monitoramento Ativo!"}


def test_get_non_existent_customer(auth_headers, client):
    """
    Valida o comportamento ao buscar um cliente inexistente.

    Espera-se que a API retorne Status 404 e a mensagem de erro apropriada.
    """
    customer_id = 999999
    response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_create_and_delete_customer_by_id(auth_headers, client):
    """
    Testa a criação de um cliente e a limpeza manual via banco.

    Verifica se os dados enviados no payload são refletidos na resposta
    da API e se o ID gerado é válido.
    """
    payload = {"name": "Test User ID", "age": 40, "cpf": "00000000001"}

    response = client.post("/customers/", json=payload, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    new_id = data.get("id")

    assert new_id is not None
    assert data["message"] == "Customer created successfully"
    assert data["data"]["name"] == payload["name"]

    # Limpeza de rastro manual
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM customers WHERE id = %s", (new_id,))
            conn.commit()
        finally:
            conn.close()
    else:
        pytest.fail("Falha na conexão com o banco para limpeza do teste.")


def test_create_customer_invalid_age(auth_headers, client):
    """
    Valida a restrição de idade no cadastro de clientes.

    Envia uma idade negativa para garantir que o Pydantic/FastAPI
    bloqueie a requisição com Status 422 (Unprocessable Entity).
    """
    payload = {"name": "Invalido", "age": -1}
    response = client.post("/customers/", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_full_cycle(auth_headers, client):
    """
    Executa o ciclo completo: Criação seguido de Consulta (GET).

    Garante que um dado persistido via POST pode ser recuperado
    corretamente via ID.
    """
    payload = {"name": "Ciclo Completo", "age": 22, "cpf": "00000000002"}

    # Passo 1: Criação
    res_post = client.post("/customers/", json=payload, headers=auth_headers)
    assert res_post.status_code == 201
    new_id = res_post.json()["id"]

    # Passo 2: Verificação de persistência
    res_get = client.get(f"/customers/{new_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.json()["name"] == "Ciclo Completo"

    # Limpeza
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM customers WHERE id = %s", (new_id,))
        conn.commit()
        conn.close()


def test_update_customer(auth_headers, client):
    """
    Valida a atualização de dados de um cliente existente (PUT).

    Cria um registro, altera seus valores e confirma se as mudanças
    foram persistidas no banco de dados através de um novo GET.
    """
    # 1. Criação inicial
    payload_original = {"name": "Marcos Velho", "age": 30, "cpf": "00000000003"}
    res_post = client.post(
        "/customers/", json=payload_original, headers=auth_headers
    )
    customer_id = res_post.json()["id"]

    # 2. Atualização
    payload_novo = {"name": "Marcos Novo", "age": 25, "cpf": "00000000004"}
    res_put = client.put(
        f"/customers/{customer_id}", json=payload_novo, headers=auth_headers
    )

    assert res_put.status_code == 200
    assert res_put.json()["message"] == "Customer updated successfully"

    # 3. Validação pós-update
    res_get = client.get(f"/customers/{customer_id}", headers=auth_headers)
    data_final = res_get.json()
    assert data_final["name"] == "Marcos Novo"
    assert data_final["age"] == 25
    assert data_final["cpf"] == "00000000004"

    # Limpeza
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM customers WHERE id = %s", (customer_id,)
            )
        conn.commit()
        conn.close()
