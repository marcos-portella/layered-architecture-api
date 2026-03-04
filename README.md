# Layered Architecture API (Customers & Orders)
![Monitor Status](https://github.com/marcos-portella/layered-architecture-api/actions/workflows/databricks_monitor.yml/badge.svg)

A professional REST API built with **FastAPI** and **MySQL**, focusing on clean code principles, security, and high-performance testing. This project manages customers and their orders using a decoupled **Service Layer** architecture.

## Live Demo & Automation

### API Access (Development Tunnel)
The API is currently live and available for testing through a secure **ngrok** tunnel.
* **Interactive Documentation:** [Explore Swagger UI](https://nonvagrantly-unreverting-rutha.ngrok-free.dev/docs)
* **System Health Check:** [API Status](https://nonvagrantly-unreverting-rutha.ngrok-free.dev/)
> **Note:** Running in a Docker environment; links may be offline during maintenance.

### Smart Monitoring System (New!)
I implemented an automated **Serverless Watcher** that monitors the Databricks AI Summit agenda every hour.
* **Infrastructure**: GitHub Actions (Cron Jobs).
* **Communication**: Real-time alerts via **Telegram Bot API**.
* **Data Persistence**: State tracking via Git-based storage to minimize database overhead.

---

### Key Features

- **Security**: Professional OAuth2 (JWT) Bearer Token authentication.
- **Architecture**: Implements the **Service Layer Pattern** to decouple business logic from API routes.
- **Validation**: Strict data validation using Pydantic V2 with custom field constraints.
- **Auditing**: Automatic tracking of user actions (`created_by`) via JWT payloads.
- **Automation**: Headless web scraping and cloud-based task scheduling.

### Tech Stack

* **Backend**: FastAPI (Python)
* **Database**: MySQL
* **DevOps**: GitHub Actions, Docker
* **Notifications**: Telegram API
* **Testing**: Pytest (Integration Tests)

### Testing & Quality

The project features a comprehensive suite of **12 automated integration tests** covering authentication, CRUD operations, and error handling.
* **Performance**: Optimized session-scoped fixtures, reducing execution time from 3.04s to **1.04s** (~70% faster).

````
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

├── selenium/         # Web Scraper & Automation Logic

├── tests/            # Pytest Integration Suite

└── last_count.txt    # Persistent monitor state


I maintain a detailed development log tracking my daily progress, technical challenges, and architectural decisions. 

You can follow the step-by-step evolution of this project here:
**[View Development Journal (JOURNAL.md)](./JOURNAL.md)**

### Evolution Roadmap
Currently, **layered-architecture-api** is 100% powered by Python and FastAPI. I have initiated **Java** studies (located in the ``/java_study`` directory) with the goal of eventually migrating performance-critical modules to microservices using **Java** and **Spring Boot**.
