# Contributing to CaiHub

Thanks for your interest in CaiHub. This repository is an early-stage FastAPI
backend for an AI-native restaurant operations system. Contributions that
improve reliability, documentation, tests, data contracts, agent architecture,
and safe demo workflows are welcome.

## Before You Start

- Do not commit real restaurant data, production reports, screenshots, phone
  numbers, API keys, tokens, webhook URLs, Feishu/Lark credentials, or `.env`
  files.
- Use only synthetic or anonymized examples in tests, docs, screenshots, and
  sample payloads.
- Keep changes focused. Avoid large rewrites of core business logic unless the
  issue or pull request discussion calls for it.

## Fork and Clone

1. Fork the repository on GitHub.
2. Clone your fork:

```bash
git clone https://github.com/<your-user>/Caihub-2.0.git
cd Caihub-2.0
```

3. Add the upstream repository if needed:

```bash
git remote add upstream https://github.com/marsming4032351-star/Caihub-2.0.git
```

## Install Dependencies

The project uses Python 3.11+ and `pyproject.toml`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configure Local Environment

Copy the example environment file and edit local values as needed:

```bash
cp .env.example .env
```

Keep `.env` local only. Do not commit it.

For lightweight local API testing without a running database migration flow,
the current code supports:

```bash
export CAIHUB_AUTO_CREATE_TABLES=true
```

For database-backed development, configure `CAIHUB_DATABASE_URL` locally and
run migrations:

```bash
alembic upgrade head
```

## Run the App

```bash
uvicorn app.main:app --reload
```

The default API prefix is `/api/v1`.

## Run Tests

The repository uses `pytest` with test discovery configured in `pyproject.toml`.

```bash
pytest
```

If your local environment does not have development dependencies installed, run
`pip install -e ".[dev]"` first.

## Issues

When opening an issue, include:

- What you expected to happen.
- What actually happened.
- Steps to reproduce the behavior.
- Relevant operating system, Python version, and dependency context.

Never include secrets, real restaurant data, raw screenshots from production
systems, private webhook URLs, or customer-identifying details in an issue.

## Pull Requests

Before opening a pull request:

- Keep the change scoped to one concern.
- Add or update tests when behavior changes.
- Update documentation when APIs, commands, data contracts, or examples change.
- Run `pytest` locally when possible.
- Use clear synthetic data in examples and tests.

## Code Style and Documentation

- Follow the style already present in the repository.
- Prefer typed Pydantic schemas and explicit domain language for data contracts.
- Keep docs concise and practical.
- Document new environment variables in `.env.example` and related docs.
- Do not add generated artifacts, local caches, real screenshots, or exported
  production reports.
