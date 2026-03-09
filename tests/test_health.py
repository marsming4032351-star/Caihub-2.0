import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "test.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_health_check() -> None:
    with create_test_client(Path.cwd() / ".pytest_cache" / "health") as client:
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_system_info() -> None:
    with create_test_client(Path.cwd() / ".pytest_cache" / "system") as client:
        response = client.get("/api/v1/system/info")

        assert response.status_code == 200
        body = response.json()
        assert body["app_name"] == "CaiHub Backend"
        assert body["version"] == "0.1.0"
