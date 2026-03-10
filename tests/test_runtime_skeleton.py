import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "runtime-tests.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_agent_runtime_overview(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.get("/api/v1/system/agent-runtime")

        assert response.status_code == 200
        body = response.json()
        assert body["orchestration_status"] == "skeleton-ready"
        assert body["runtime_ready_agents"] >= 1
        assert any(agent["agent_id"] == "ceo-agent" for agent in body["agents"])


def test_system_info_exposes_ai_company_metadata(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.get("/api/v1/system/info")

        assert response.status_code == 200
        body = response.json()
        assert body["app_name"] == "CaiHub AI Company"
        assert body["system_type"] == "restaurant-ai-operating-system"
        assert body["architecture_stage"] == "foundation-with-runtime-skeleton"
