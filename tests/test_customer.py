"""
Testes de Cobertura e Casos de Exceção - Customers
--------------------------------------------------
Este módulo foca em atingir 100% de cobertura na camada de serviço de clientes,
testando especificamente os fluxos de erro (404, 400) e a limpeza de dados.
"""


def test_get_customer_not_found(client, auth_headers):
    """
    Valida a resposta quando um cliente pesquisado não existe.

    Garante a cobertura da lógica de 'raise HTTPException' na busca por ID.
    """
    response = client.get("/customers/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_create_duplicate_customer_clean(client, auth_headers):
    """
    Testa a restrição de CPF duplicado e valida o rollback lógico.

    Tenta inserir dois clientes com o mesmo CPF e garante que o segundo
    seja rejeitado com Status 400.
    """
    payload = {
        "name": "[TEST] Cliente Duplicado",
        "age": 30,
        "cpf": "00000000011"
    }

    # 1. Criação do primeiro registro
    res1 = client.post("/customers/", json=payload, headers=auth_headers)

    # 2. Tentativa de duplicata
    res2 = client.post("/customers/", json=payload, headers=auth_headers)

    # 3. Limpeza preventiva
    if res1.status_code == 201:  # Ajustado para 201 Created
        customer_id = res1.json()["id"]
        client.delete(f"/customers/{customer_id}", headers=auth_headers)

    # 4. Validação da falha na duplicata
    assert res2.status_code == 400


def test_delete_customer_not_found_explicit(client, auth_headers):
    """
    Força a cobertura das linhas de exceção no método de exclusão.

    Tenta deletar um ID inexistente para validar se o sistema retorna 404
    em vez de um erro interno de banco (500).
    """
    response = client.delete("/customers/999888", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_force_service_exceptions(client, auth_headers):
    """
    Bateria de testes para forçar exceções em cascata (Update e Delete).

    Garante que tanto a atualização quanto a exclusão tratem IDs fantasmas
    corretamente na camada de serviço.
    """
    # 1. Força erro no Update (ID inexistente)
    payload = {"name": "Ghost", "age": 0, "cpf": "00001000000"}
    res_put = client.put(
        "/customers/999999", json=payload, headers=auth_headers
    )
    assert res_put.status_code == 404

    # 2. Força erro no Delete (ID inexistente)
    res_del = client.delete("/customers/999999", headers=auth_headers)
    assert res_del.status_code == 404


def test_delete_success_for_coverage(client, auth_headers):
    """
    Valida o fluxo completo de exclusão bem-sucedida.

    Cria um registro temporário e o remove imediatamente para garantir
    que as linhas de sucesso da rota DELETE sejam executadas.
    """
    # 1. Setup: Criação temporária
    temp_payload = {"name": "Delete Me", "age": 20, "cpf": "88877766655"}
    res = client.post("/customers/", json=temp_payload, headers=auth_headers)
    cid = res.json()["id"]

    # 2. Execução: Remoção
    res_del = client.delete(f"/customers/{cid}", headers=auth_headers)
    assert res_del.status_code == 200
