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

2. Create and activate a virtual environment:

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create your own `.env` file based on `.env.example` in the project root.

5. Start the application:

    ```bash
    docker-compose up --build
    ```

    By default, the API will be available at `http://localhost:8000/docs`.  
    If you change the port in your `.env`, make sure it matches the port in the URL.

## Project Structure

```bash
src/
├── core/  # Config, DB setup (async + sync), security, seeding
├── users/
│ ├── auth/  # Signup, login, verification
│ ├── user_management/  # Logic for managing users
│ └── models.py  # SQLAlchemy models
├── tasks/  # Celery background tasks
├── api.py  # Router registration
└── main.py  # App entry point
```