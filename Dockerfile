FROM python:3.8 AS build

# Only rebuilds if dockerfile is changed
RUN pip install poetry

FROM build AS build-reqs

# Install requirements - only rebuilds if pyproject.toml changes
COPY poetry.lock /app/
COPY pyproject.toml /app
RUN cd /app && \
    poetry install --no-dev --no-interaction

FROM python:3.8-slim

# Copy installed required packages
COPY --from=build-reqs /root/.cache/pypoetry/virtualenvs/*/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
# Install app
COPY src/main /app/bq-api

WORKDIR /app
ENTRYPOINT python -m bq-api