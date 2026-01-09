from mysql.connector.abstracts import MySQLConnectionAbstract
from fastapi import HTTPException
from app.models.customers import Customer


class CustomerServices:
    @staticmethod
    def get_customer(
        customer_id: int, db: MySQLConnectionAbstract,
        user_email: str
    ):
        cursor = db.cursor(dictionary=True)

        print(
                f"Ação: Usuário {user_email} buscou pelo cliente {customer_id}"
            )

        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @staticmethod
    def create_customer(
        customer: Customer, db: MySQLConnectionAbstract, user_email: str
    ):
        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM customers WHERE cpf = %s", (customer.cpf,)
        )
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        print(
                f"Ação: Usuário {user_email} adicionou mais um cliente"
            )

        sql = "INSERT INTO customers (nome, idade, cpf) VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer.name, customer.age, customer.cpf))
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {
            "id": new_id, "message": "Customer created successfully",
            "data": customer,
            "created_by": user_email
        }

    @staticmethod
    def update_customer(
        customer_id: int, updated_data: Customer,
        db: MySQLConnectionAbstract, user_email: str
    ):
        with db.cursor() as cursor:

            print(
                f"Ação: Usuário {user_email} atualizou o cliente {customer_id}"
            )

            sql = """
            UPDATE customers SET nome = %s, idade = %s, cpf = %s WHERE id = %s
            """
            cursor.execute(
                sql, (
                    updated_data.name, updated_data.age,
                    updated_data.cpf, customer_id
                )
            )
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Customer not found"
                )
            db.commit()
            return {
                "message": "Customer updated successfully",
                "id": customer_id,
                "updated_by": user_email
            }

    @staticmethod
    def delete_customer(
        customer_id: int, db: MySQLConnectionAbstract, user_email: str
    ):
        with db.cursor() as cursor:
            print(f"Ação: Usuário {user_email} deletou o cliente {customer_id}")

            sql = "DELETE FROM customers WHERE id = %s"
            cursor.execute(sql, (customer_id,))

            # Se não deletou nada, lança erro e sai da função aqui
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Customer not found"
                )

            # Se chegou aqui, é sucesso total. O commit e return PRECISAM rodar.
            db.commit()
            return {
                "message": "Customer deleted successfully",
                "id": customer_id,
                "deleted_by": user_email
            }
