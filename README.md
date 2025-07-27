# Coffee Shop API — User Management Module

This module implements user authentication, verification, and role-based access control for the Coffee Shop API.

## Features

- Registration with email, password, optional name/surname
- Email verification (simulated via console output)
- JWT-based authentication (access + refresh tokens)
- Automatic removal of unverified users after 2 days
- Role-based access: User / Admin

## Tech Stack

- FastAPI (async)
- SQLAlchemy 2.0 (async + sync engines)
- PostgreSQL
- Alembic
- Celery
- Docker, Docker Compose

## Getting Started

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd <project-dir>
    ```

2. Create and activate a virtual environment.

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create your own `.env` file based on `.env.example` in the project root.

5. Start the application:

    ```bash
    docker compose up --build
    ```

    By default, the API will be available at `http://localhost:8000/docs`.  
    If you change the port in your `.env`, make sure it matches the port in the URL.

## Project Structure

```bash
├── alembic/ # Database migrations
├── src/
│   ├── core/
│   │   ├── config.py  # Environment configuration
│   │   ├── database.py  # Async and sync database engines/sessions
│   │   ├── schemas.py  # Security-related Pydantic models
│   │   ├── scripts.py  # Startup scripts (e.g., admin user creation)
│   │   └── security.py  # Password hashing and JWT handling
│   │
│   ├── tasks/
│   │   └── celery_tasks.py  # Background tasks (e.g., auto-delete unverified users)
│   │
│   ├── users/
│   │   ├── auth/
│   │   │   ├── schemas.py  # Pydantic models for auth endpoints
│   │   │   ├── service.py  # Business logic for registration, login, verification
│   │   │   ├── utils.py  # Helper functions (e.g., code generation)
│   │   │   └── views.py  # Routes for auth
│   │   ├── user_management/
│   │   │   ├── dependencies.py  # Dependency for role-based access
│   │   │   ├── schemas.py  # Pydantic models for user data
│   │   │   ├── service.py  # User management logic (e.g., update, delete)
│   │   │   └── views.py  # Routes for user management
│   │   ├── dependencies.py  # Shared dependencies (e.g., get_session)
│   │   └── models.py  # SQLAlchemy models
│   │
│   ├── api.py  # FastAPI router registration
│   └── main.py  # Application entry point
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env  # Environment variables file
├── worker.py  # Celery worker entry point
└── alembic.ini  # Alembic configuration
```