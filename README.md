# Task Management REST API — Python / FastAPI

A runnable, REST API demonstrating:

- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Pydantic v2
- JWT authentication
- Role-based authorization
- Service / Repository architecture
- Dependency Injection
- CRUD
- Search, filtering, pagination and sorting
- Centralized exception handling
- OpenAPI / Swagger UI
- pytest unit and integration tests
- Docker and Docker Compose
- Environment-based configuration
- Health checks

## Architecture

Client
  |
  v
FastAPI Router
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
SQLAlchemy
  |
  v
PostgreSQL

Authentication is handled through JWT access tokens. The project intentionally keeps the business domain simple so the same API can later be implemented in C# and Java.

## Requirements

For the Docker workflow, you only need:

- Docker Desktop
- Docker Compose

Python 3.12+ is recommended for running tests locally.

## Run with Docker Compose

From the project directory:

```bash
docker compose up --build
```

API:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

Health:

http://localhost:8000/health

Stop:

```bash
docker compose down
```

Remove the database volume too:

```bash
docker compose down -v
```

## Default demo users

The application creates these users automatically on startup:

- admin@example.com / Admin123!
- user@example.com / User123!

Change these credentials for any real deployment.

## Authentication flow

1. Open `/docs`.
2. Register a user with `POST /api/v1/auth/register`, or use a seeded demo user.
3. Login with `POST /api/v1/auth/login`.
4. Copy the returned access token.
5. Click **Authorize** in Swagger UI.
6. Enter:

```text
Bearer <your-token>
```

7. Call the protected endpoints.

## Main endpoints

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Tasks

```text
POST   /api/v1/tasks
GET    /api/v1/tasks
GET    /api/v1/tasks/{task_id}
PATCH  /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
```

Task listing supports:

- `page`
- `page_size`
- `status`
- `priority`
- `search`
- `sort_by`
- `sort_order`

Example:

```text
GET /api/v1/tasks?page=1&page_size=10&status=TODO&search=docker&sort_by=created_at&sort_order=desc
```

## Roles

Two roles are provided:

- `USER`: manage own tasks
- `ADMIN`: manage all tasks and delete any task

## Run tests locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
pytest
```
