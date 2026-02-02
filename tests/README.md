## Suíte de Testes Automatizados - layered-architecture-api Project

Este diretório contém a infraestrutura de testes da API, desenvolvida com o objetivo de garantir a **resiliência, segurança e integridade** dos dados do sistema Noach.



### Tecnologias Utilizadas
* **Pytest**: Framework principal para execução e descoberta de testes.
* **FastAPI TestClient**: Simulação de requisições HTTP sem necessidade de subir o servidor manualmente.
* **Unittest.mock**: Utilizado para simular falhas de infraestrutura (Banco de Dados).
* **Pandas**: Validação da lógica de BI e geração de relatórios.

### Arquitetura dos Testes

A suíte foi desenhada seguindo as melhores práticas de **Integração Contínua (CI)**:

1. **Fixtures Globais (``conftest.py``)**: 
   - Gerenciamento automático de tokens JWT para rotas protegidas.
   - **Teardown Automático**: Limpeza do banco de dados após cada execução para evitar poluição de dados (Idempotência).

2. **Módulos de Teste**:
   - ``test_auth.py``: Validação de segurança, decodificação de tokens e proteção de rotas.
   - ``test_api.py`` / ``test_customer.py``: Ciclo de vida completo (CRUD) e tratamento de erros (404/400).
   - ``test_database.py``: Testes de resiliência. Simulamos quedas do MySQL para garantir que a API responda com erro 503 amigável em vez de travar.
   - ``test_order.py``: Integração entre módulos e validação de relatórios de BI.

## 🛠️ Como Executar os Testes

Certifique-se de que o seu ambiente virtual está ativo e as dependências instaladas.

1. **Executar todos os testes utilizando o test.ps1:**

````
./test.ps1
````

2. **Executar todos os testes (padão):**

````
pytest
````

2. **Verificar a cobertura de código (padrão):**

````
pytest --cov=app tests/
````

4. **Executar um módulo específico (padrão), (ex: Segurança):**

````
pytest tests/test_auth.py
````

### Destaques Técnicos

- **Tratamento de Exceções**: Testamos propositalmente falhas de conexão com o banco de dados para validar o comportamento do sistema sob estresse.

- **Isolamento**: Cada teste é independente, garantindo que a falha de um não afete o resultado do próximo.

- **Auditoria JWT**: Testes específicos para garantir que tokens malformados ou expirados sejam devidamente rejeitados.