## Cloud Storage API

FastAPI-based cloud storage service with JWT auth, OTP email verification, and async
PostgreSQL persistence.

## Features

- Async FastAPI + SQLAlchemy with PostgreSQL
- Email OTP signup flow and JWT access/refresh tokens (RS256)
- File upload, download, visibility controls, and storage quotas
- Alembic migrations
- Docker + Compose ready

## Requirements

- Python 3.13+
- PostgreSQL 17+ (or use Docker Compose)
- SMTP server for OTP emails

## Quick Start (Docker)

1) Create a `.env` file (see the sample below).
2) Run the stack:

```bash
docker compose up --build
```

The API will be available at `http://localhost:${COMPOSE_APP_PORT}`.

## Local Development

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn --factory src.main:create_app --port 8000 --reload
```

If you run locally, generate JWT keys once:

```bash
openssl genrsa -out ./certificates/jwt-private.pem 2048
openssl rsa -in ./certificates/jwt-private.pem -outform PEM -pubout -out ./certificates/jwt-public.pem
```

## Environment Variables

All settings are read from `.env` using the prefixes below.

```dotenv
# Database
DB_HOST=postgres
DB_NAME=app
DB_USER=app_user
DB_PASSWORD=postgres_password

# Auth
AUTH_JWT_ACCESS_LIFETIME_MINUTES=60
AUTH_JWT_REFRESH_LIFETIME_DAYS=30
AUTH_OTP_EXPIRE_MINUTES=10

# SMTP
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=mailer@example.com
SMTP_PASSWORD=change-me
SMTP_FROM_NAME=Cloud Storage

# Docker Compose
COMPOSE_APP_PORT=8000
COMPOSE_APP_WORKERS_COUNT=2
```

## API Overview

### Auth

- `POST /auth/sign_up` - Start signup (OTP email)
- `POST /auth/verify_otp` - Verify OTP, returns tokens
- `POST /auth/resend_otp` - Resend OTP
- `POST /auth/sign_in` - Sign in, returns tokens
- `POST /auth/refresh` - Rotate refresh token, returns new tokens
- `GET /auth` - Current user (access token required)

### Files

- `GET /files` - List current user files
- `GET /files/{id}` - Get file metadata (auth optional if public)
- `POST /files` - Upload a file
- `GET /files/{id}/download` - Download file (auth optional if public)
- `PATCH /files/{id}` - Update name or visibility
- `DELETE /files/{id}` - Delete file

Auth uses the `Authorization: Bearer <token>` header for access/refresh tokens.

## Storage Limits

- basic: 100 MB
- plus: 200 MB
- pro: 500 MB

## Notes

- Docs (`/docs`, `/redoc`) are enabled only when `APP_ENVIRONMENT=development`.
- When using Docker, migrations and JWT key generation are handled in `entrypoint.sh`.
