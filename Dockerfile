FROM python:3.8

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root --no-interaction --no-ansi

COPY src ./src

ENTRYPOINT ["python", "-m", "src.main"]
