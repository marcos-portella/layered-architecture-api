def test_get_customer_not_found(client, auth_headers):
    # Cobre a linha de 'cliente não encontrado' no service
    response = client.get("/customers/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_create_duplicate_customer_clean(client, auth_headers):
    payload = {
        "name": "[TEST] Cliente Duplicado",
        "age": 30,
        "cpf": "00000000011"
    }

    # 1. Cria o primeiro
    res1 = client.post("/customers/", json=payload, headers=auth_headers)

    # 2. Tenta criar o segundo
    res2 = client.post("/customers/", json=payload, headers=auth_headers)

# 3. LIMPEZA: Deleta o primeiro que foi criado com sucesso (se o res1 deu 200)
    if res1.status_code == 200:
        customer_id = res1.json()["id"]
        client.delete(f"/customers/{customer_id}", headers=auth_headers)

    # 4. Valida se o segundo realmente falhou
    assert res2.status_code == 400


def test_delete_customer_not_found(client, auth_headers):
    response = client.delete("/customers/999999", headers=auth_headers)
    assert response.status_code == 404


def test_delete_customer_not_found_explicit(client, auth_headers):
    # Força as linhas 102 e 103: Deletar um ID que não existe
    # Usamos um ID bem alto para garantir que não tem no banco
    response = client.delete("/customers/999888", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_force_service_exceptions(client, auth_headers):
    # 1. Força o erro no Update (Linha 74)
    payload = {"name": "Ghost", "age": 0, "cpf": "00001000000"}
    # Usamos um ID absurdamente alto
    res_put = client.put(
        "/customers/999999", json=payload, headers=auth_headers
    )
    assert res_put.status_code == 404

    # 2. Força o erro no Delete (Linhas 103-104)
    res_del = client.delete("/customers/999999", headers=auth_headers)
    assert res_del.status_code == 404


def test_delete_success_for_coverage(client, auth_headers):
    # 1. Cria um temporário só para deletar
    temp_payload = {"name": "Delete Me", "age": 20, "cpf": "88877766655"}
    res = client.post("/customers/", json=temp_payload, headers=auth_headers)
    cid = res.json()["id"]

    # 2. Deleta (Isso vai passar pelas linhas 103 e 104)
    res_del = client.delete(f"/customers/{cid}", headers=auth_headers)
    assert res_del.status_code == 200
