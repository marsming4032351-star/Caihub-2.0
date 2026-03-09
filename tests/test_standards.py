import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "standards.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_create_and_list_standards(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        create_response = client.post(
            "/api/v1/standards",
            json={
                "dish_key": "dish-kungpao-001",
                "name": "宫保鸡丁标准",
                "description": "午市标准出品。",
                "target_weight_grams": 320,
                "weight_tolerance_grams": 20,
                "target_temperature_celsius": 70,
                "temperature_tolerance_celsius": 8,
                "minimum_confidence": 0.8,
                "maximum_deviation_score": 0.25,
                "is_active": True,
            },
        )

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["dish_key"] == "dish-kungpao-001"

        list_response = client.get("/api/v1/standards")
        assert list_response.status_code == 200
        listed = list_response.json()
        assert len(listed) == 1
        assert listed[0]["dish_key"] == "dish-kungpao-001"
