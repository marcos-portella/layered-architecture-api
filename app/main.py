import time
import logging
from typing import Callable
from fastapi import FastAPI, Request, Response
from app.routers import customers, orders, auth

# 1. Configuração do Log de Auditoria
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API-Auditoria")

"""
API de Gestão de Pedidos - Marcos Portella
---------------------------------
Módulo principal que inicializa o framework FastAPI, configura o sistema de
auditoria via middleware e centraliza as rotas da aplicação.

Padrão de documentação: Google Style Docstrings.
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "🔑 **Acesso e Segurança**. "
        "Registro de novos administradores e geração de tokens JWT para "
        "autenticação.",
    },
    {
        "name": "customers",
        "description": "👥 **Gestão de Clientes**. "
        "Operações de cadastro, listagem, atualização e exclusão de clientes.",
    },
    {
        "name": "orders",
        "description": "📦 **Gestão de Pedidos**. "
        "Criação de vendas vinculadas a clientes e estatísticas de "
        "faturamento.",
    },
    {
        "name": "Monitoramento",
        "description": "🖥️ **Integridade do Sistema**. "
        "Endpoints para verificação de status.",
    },
]

app = FastAPI(
    title="API de Gestão de Pedidos - Marcos",
    openapi_tags=tags_metadata,
    description="""
### Gerenciamento Profissional de Clientes e Pedidos
Esta API implementa uma arquitetura em camadas para controle de vendas com:
* **Segurança**: Autenticação baseada em JWT (JSON Web Tokens).
* **Auditoria**: Registro automático de logs e tempo de resposta.
* **Integridade**: Validação rigorosa de dados com Pydantic.
    """,
    version="1.0.0"
)


# 2. Middleware de Auditoria
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """
    Intercepta requisições HTTP para fins de auditoria e monitoramento de
    performance.

    Registra o início da chamada, o método utilizado, a rota acessada e, ao
    final,o status code retornado junto com o tempo de latência em
    milissegundos.

    Args:
        request (Request): Objeto contendo os dados da requisição recebida.
        call_next (Callable): Próxima função na cadeia de execução (rota ou
        outro middleware).

    Returns:
        Response: O objeto de resposta processado com o cabeçalho
        'X-Process-Time'.
    """
    start_time = time.time()
    logger.info(f"🚀 {request.method} {request.url.path} - Iniciado")

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_time = f"{process_time:.2f}ms"

    logger.info(f"✅ Status: {response.status_code} | Tempo: {formatted_time}")

    response.headers["X-Process-Time"] = formatted_time
    return response

# 3. Inclusão das Rotas (Arquitetura em Camadas)
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/", tags=["Monitoramento"])
def root():
    """
    Realiza o Health Check da aplicação.

    Verifica se a instância da API está ativa e pronta para receber conexões.

    Returns:
        dict: Dicionário contendo a mensagem de status da API.
    """
    return {"message": "API Online - Monitoramento Ativo!"}

# Para rodar a aplicação: uvicorn app.main:app --reload
