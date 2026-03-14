# ===== Build stage =====
FROM python:3.13-slim-trixie AS build-stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv .venv --prompt .venv
RUN uv sync --locked --no-dev --compile-bytecode


# ===== Runtime stage =====
FROM python:3.13-slim-trixie AS runtime-stage

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=build-stage /app/.venv /app/.venv

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

EXPOSE 8000

CMD [ "uvicorn", "--factory", "src.main:create_app", "--host", "0.0.0.0", "--workers", "2", "--no-server-header", "--no-use-colors" ]
