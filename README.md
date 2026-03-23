# Cinescope API Test Framework

Автотесты для API сервиса Cinescope (auth, users, movies + базовые DB-проверки).

## Stack
- Python 3.11
- Pytest
- Requests
- Pydantic v2
- SQLAlchemy + psycopg2
- pre-commit, Ruff, mypy
- Allure (`allure-results`)

## Project Structure
```text
clients/            # HTTP API clients
custom_requester/   # общий sender + status/code checks + логирование
entities/           # доменные обертки (User, Movie)
models/             # Pydantic request/response модели
assertions/         # проверки error-контрактов и бизнес-ожиданий
db/                 # engine, session, SQL queries
tests/api/          # API тесты
tests/db/           # DB тесты
```

## Quick Start
```bash
uv sync
```

## Environment Variables
Обязательные:
- `SUPER_ADMIN_USERNAME`
- `SUPER_ADMIN_PASSWORD`

API endpoints (по умолчанию уже заданы, можно переопределить):
- `AUTH_BASE_URL`
- `API_BASE_URL`

DB (для `tests/db`):
- `DB_MOVIES_HOST`
- `DB_MOVIES_PORT`
- `DB_MOVIES_NAME`
- `DB_MOVIES_USERNAME`
- `DB_MOVIES_PASSWORD`

## Test Run
```bash
uv run pytest
```

Удобные команды через Makefile:
```bash
make lint
make test
make test-smoke
make test-smoke-stable
make test-smoke-integration
make test-regression
make test-negative
make test-workflow
```

## Markers
Настроены в `pytest.ini`:
- `smoke_stable` — стабильный smoke для PR CI
- `smoke_integration` — smoke, зависящий от внешнего окружения
- `regression`
- `negative`
- `workflow`
- `api`
- `db`
- `slow`

Посмотреть, какие тесты входят в маркер:
```bash
uv run pytest -m smoke_stable --collect-only -q
uv run pytest -m smoke_integration --collect-only -q
```

## Response Validation Approach
- Позитивные ответы валидируются через Pydantic `response_model`.
- Негативные ответы валидируются через `ErrorResponse` и assertions.
- HTTP status code проверяется централизованно в `CustomRequester`.

## CI
GitHub Actions workflow (`.github/workflows/ci.yml`) делает:
1. Установка зависимостей
2. `pre-commit run --all-files`
3. `pytest --collect-only -q`
4. `pytest -m smoke_stable -q`
5. Upload `allure-results` artifact (`if: always()`)

Это значит, что PR не блокируется из-за нестабильных интеграционных smoke.

## Dependencies Policy
Используются:
- `pyproject.toml` — прямые зависимости проекта и настройки инструментов
- `uv.lock` — полный lock для воспроизводимых прогонов

Обновить lock и окружение:
```bash
uv lock
uv sync
```
