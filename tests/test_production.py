import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "production.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_create_and_list_production_events(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        standard_response = client.post(
            "/api/v1/standards",
            json={
                "dish_key": "dish-kungpao-001",
                "name": "宫保鸡丁标准",
                "description": "严格版标准。",
                "target_weight_grams": 345,
                "weight_tolerance_grams": 10,
                "target_temperature_celsius": 66,
                "temperature_tolerance_celsius": 3,
                "minimum_confidence": 0.9,
                "maximum_deviation_score": 0.12,
                "is_active": True,
            },
        )
        assert standard_response.status_code == 201

        create_response = client.post(
            "/api/v1/production/events",
            json={
                "store_code": "store-sh-001",
                "dish_id": "dish-kungpao-001",
                "operator_code": "chef-ming",
                "capture": {
                    "image_url": "https://example.com/kungpao.jpg",
                    "lighting_profile": "5600K-standard",
                    "camera_profile": "caibox-v1",
                    "temperature_celsius": 66.0,
                    "weight_grams": 345.0,
                },
                "recognition": {
                    "model_version": "vlm-vision-v1",
                    "top_label": "kung-pao-chicken",
                    "confidence": 0.92,
                },
                "feedback": {
                    "corrected": False,
                    "corrected_label": None,
                    "reason": None,
                },
            },
        )

        assert create_response.status_code == 201
        assert (
            create_response.headers["X-CaiHub-Quality-Event"]
            == "production.quality.decided"
        )
        created = create_response.json()
        assert created["dish_id"] == "dish-kungpao-001"
        assert created["store_code"] == "store-sh-001"
        assert created["operator_code"] == "chef-ming"
        assert created["quality_result"]["standard_dish_key"] == "dish-kungpao-001"
        assert created["quality_result"]["pass_decision"] is True
        assert created["quality_result"]["plating_score"] >= 0.8

        list_response = client.get("/api/v1/production/events")
        assert list_response.status_code == 200
        listed = list_response.json()
        assert len(listed) == 1
        assert listed[0]["id"] == created["id"]
