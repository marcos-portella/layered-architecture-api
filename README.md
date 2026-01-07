## Layered Architecture API (Customers & Orders)

A professional REST API built with **FastAPI** and **MySQL**, focusing on clean code principles, security, and high-performance testing. This project manages customers and their orders using a decoupled **Service Layer** architecture.



### 🚀 Key Features

- **Security**: Professional OAuth2 (JWT) Bearer Token authentication.
- **Architecture**: Implements the **Service Layer Pattern** to decouple business logic from API routes.
- **Database**: Robust relational structure with MySQL, including advanced SQL aggregations for business metrics.
- **Validation**: Strict data validation using Pydantic V2 with custom field constraints.
- **Admin Control**: Secured registration endpoints restricted to authenticated administrators.
- **Auditing**: Automatic tracking of user actions (created_by) via JWT payloads.

### 🛠️ Tech Stack

* **Framework**: FastAPI
* **Database**: MySQL
* **Authentication**: JWT (JSON Web Tokens)
* **Testing**: Pytest (Integration Tests)
* **Validation**: Pydantic V2

### 🧪 Testing & Quality

The project features a comprehensive suite of **12 automated integration tests** covering:
- Authentication flows (Login/Register).
- CRUD operations for Customers and Orders.
- Error handling (401 Unauthorized, 404 Not Found, 422 Unprocessable Entity).
- **Performance Optimization**: Utilizes session-scoped fixtures, reducing test execution time by ~70% (from 3.04s to **1.04s**).

````bash
# How to run tests
python -m pytest
````


Project Structure
Plaintext

├── app/
│   ├── core/         # Config & Security settings
│   ├── models/       # Pydantic Schemas
│   ├── routers/      # API Endpoints (Skinny Controllers)
│   ├── services/     # Business Logic (Service Layer)
│   └── main.py       # Application Entry Point
├── tests/            # Pytest Integration Suite
└── .env.example      # Environment Template


I maintain a detailed development log tracking my daily progress, technical challenges, and architectural decisions. 

You can follow the step-by-step evolution of this project here:
👉 **[View Development Journal (JOURNAL.md)](./JOURNAL.md)**
