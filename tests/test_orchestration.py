import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "orchestration.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_system_orchestration_plan(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.get("/api/v1/system/orchestration-plan")

        assert response.status_code == 200
        body = response.json()
        assert body["owner_agent_id"] == "ceo-agent"
        assert body["status"] == "draft"
        assert len(body["tasks"]) >= 3
        assert any(task["assigned_agent_id"] == "vision-qa-agent" for task in body["tasks"])
