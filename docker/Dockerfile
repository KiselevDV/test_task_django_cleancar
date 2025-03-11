FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

COPY README.md ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --with dev --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]