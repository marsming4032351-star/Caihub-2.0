# CaiHub Quickstart

CaiHub is an early-stage FastAPI backend for an AI-native restaurant operations
system. It models dish standards, production events, visual quality decisions,
store operations, and data asset materialization for restaurant AI agents.

## Who This Is For

This quickstart is for contributors, reviewers, and developers who want to run
the current backend skeleton locally, inspect the API, or contribute tests and
documentation before deeper product integration.

## Requirements

- Python 3.11 or newer.
- `pip` and `venv`.
- PostgreSQL if you want to run the migration-backed database flow.
- Development dependencies from `pyproject.toml`, including `pytest`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configure Environment

The application reads settings from environment variables and a local `.env`
file through `app/core/config.py`.

Copy the example file:

```bash
cp .env.example .env
```

Keep `.env` local and do not commit it. Use placeholder or local-only values.
The most relevant current settings are:

```bash
CAIHUB_APP_NAME="CaiHub AI Company"
CAIHUB_ENVIRONMENT="development"
CAIHUB_DEBUG=true
CAIHUB_API_V1_PREFIX="/api/v1"
CAIHUB_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/caihub"
CAIHUB_AUTO_CREATE_TABLES=false
```

## Start the Backend

For a database-backed local run, configure `CAIHUB_DATABASE_URL`, then apply
migrations:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

For lightweight local testing with automatic table creation enabled:

```bash
export CAIHUB_AUTO_CREATE_TABLES=true
uvicorn app.main:app --reload
```

The API is served from the `/api/v1` prefix by default. Useful initial checks:

```bash
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8000/api/v1/system/info
```

## Run Tests

`pyproject.toml` configures pytest to discover tests from the `tests/`
directory.

```bash
pytest
```

If your environment uses a different Python runner or dependency manager,
adjust the command according to the current repository script availability.

## Example Data

Synthetic sample payloads live in `examples/`:

- `dish_standard.sample.json`
- `production_event.sample.json`
- `store_daily_report.sample.json`
- `quality_decision.sample.json`

These examples are fictional and safe to share. Do not replace them with real
store data, original dish photos, production screenshots, phone numbers,
webhooks, or credentials.

## Common Questions

### There is no custom test script. What should I run?

Use `pytest`. The current repository does not define a custom test command in
`pyproject.toml`.

### Can I commit my local `.env`?

No. Commit only `.env.example` with safe placeholders.

### Do I need PostgreSQL for every local check?

Not always. For lightweight local API testing, set
`CAIHUB_AUTO_CREATE_TABLES=true`. For migration work, use PostgreSQL and run
`alembic upgrade head`.

### Can examples include real restaurant screenshots or reports?

No. Use synthetic, anonymized, or heavily redacted data only.
