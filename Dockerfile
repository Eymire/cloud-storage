FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -m -u 1001 app

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . .

RUN chown -R app:app /app

USER app
EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "--factory", "src.main:create_app", "--host", "0.0.0.0", "--workers", "4", "--no-server-header", "--no-date-header" ]
