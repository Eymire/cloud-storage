FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

RUN useradd -m -u 1001 app

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . .

RUN chown -R app:app /app

USER app
EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "uv", "run", "uvicorn", "--factory", "src.main:create_app", "--host", "0.0.0.0", "--workers", "2", "--no-server-header", "--no-date-header", "--no-use-colors" ]
