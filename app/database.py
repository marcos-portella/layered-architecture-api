import mysql.connector
from mysql.connector import Error
import os
from app.dependencies.auth import HashHelper


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            # Dica: adicione um timeout para a API não ficar travada esperando
            connect_timeout=5
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
# Aqui podes decidir: ou para o sistema, ou levanta uma exceção para o FastAPI
        return None


# No FastAPI, usamos o gerador (yield) para garantir que fecha a conexão
def get_db():
    db = get_db_connection()
    if db is None:
        # Se o banco estiver fora, avisamos o usuário da API de forma elegante
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail="Banco de dados temporariamente indisponível"
        )
    try:
        yield db
    finally:
        if db.is_connected():
            db.close()


def create_tables():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                cpf VARCHAR(11) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                customer_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        """)

        # 2. SEED: Criando o usuário com a Hash que a API aceita
        test_email = os.getenv(
            "TEST_USER_EMAIL", "testemailapiuserorderetc@gmail.com"
        )
        test_password_plana = os.getenv("TEST_USER_PASSWORD", "testpassword")

        # Usamos o seu método para criar a hash padrão
        test_password_hashed = HashHelper.get_password_hash(test_password_plana)

        cursor.execute("""
            INSERT IGNORE INTO users (email, hashed_password, full_name)
            VALUES (%s, %s, %s)
        """, (test_email, test_password_hashed, "Admin Teste"))

        conn.commit()
        cursor.close()
        conn.close()
