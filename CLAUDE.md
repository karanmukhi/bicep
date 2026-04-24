# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI Python service that ingests workout and sensor data (accelerometer, gyroscope) into a PostgreSQL database. The app is named `bq-api-python` (originally built for BigQuery, now using Postgres).

## Setup

Dependencies are managed with Poetry:

```bash
poetry install          # install all deps including dev
poetry install --no-dev # production deps only
```

Run the server:

```bash
API_PORT=8000 TR_AI_NER_POSTGRES_PASSWORD=<password> python -m src.main
```

The `TR_AI_NER_POSTGRES_PASSWORD` env var is required at startup — the app will raise on launch without it. DB connection config (host, database, port, user) lives in `src/main/config/database_config.ini` under the `[trainer_one]` section.

## Running Tests

```bash
pytest src/test/
```

Run a single test:

```bash
pytest src/test/test_endpoints.py::testPing
```

## Architecture

**Request flow:** `endpoints.py` (FastAPI routes) → `endpointsLogic.py` (DB logic) → PostgreSQL via `psycopg2`

**Three model layers:**

- `model/model.py` — Pydantic request/response schemas (`User`, `Workout`, `ExerciseSet`, `SensorData`)
- `model/table.py` — Table name constants as classes inheriting `BqTable`
- `model/responseModel.py` — Response-only schemas (`SensorSuccessResponse`)

**API endpoints** (all under `/api/v1`):

- `POST /users`, `POST /workouts`, `POST /exercise_sets` — accept JSON matching the Pydantic models
- `POST /acceleration_data`, `POST /gyroscope_data` — accept CSV file uploads; processed in 10k-row chunks via pandas, deriving a `ms` timestamp column as `index * 20`

**SQL construction** in `endpointsLogic.py:addRowsToTableLogic` uses f-string interpolation of dict values directly into INSERT statements — this is a SQL injection risk to be aware of when modifying that function.

## Docker

```bash
docker build -t bicep .
docker run -e API_PORT=8000 -e TR_AI_NER_POSTGRES_PASSWORD=<password> bicep
```
