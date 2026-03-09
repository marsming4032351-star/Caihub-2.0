import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "architecture.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_system_architecture_blueprint(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.get("/api/v1/system/architecture")

        assert response.status_code == 200
        body = response.json()
        assert any("事件优先" in principle for principle in body["core_principles"])
        assert "catalog" in body["mesh_domains"]
        assert "production" in body["mesh_domains"]
        assert any(
            contract["product"] == "dish_catalog"
            for contract in body["data_contracts"]
        )
        assert any(
            contract["product"] == "dish_production_event"
            for contract in body["data_contracts"]
        )
        assert any(
            agent["agent_id"] == "backend-architect"
            for agent in body["agents"]
        )
        assert any(
            agent["agent_id"] == "quality-judge"
            for agent in body["agents"]
        )
        assert any(
            skill["skill_id"] == "contract-governance"
            for skill in body["skills"]
        )
        assert any(
            skill["skill_id"] == "quality-rule-engine"
            for skill in body["skills"]
        )
