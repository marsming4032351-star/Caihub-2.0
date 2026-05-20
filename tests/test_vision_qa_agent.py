import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "vision-qa-agent.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_vision_qa_agent_demo_runtime_returns_core_agent_artifacts(
    tmp_path: Path,
) -> None:
    with create_test_client(tmp_path) as client:
        response = client.post(
            "/api/v1/agents/vision-qa/inspect-demo",
            json={
                "image_url": "https://example.com/caihub/dish-001.jpg",
                "order_id": "order-001",
                "dish_id": "kung-pao-chicken",
                "temperature_celsius": 62.5,
                "store_id": "store-shanghai-001",
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["task_input"]["dish_id"] == "kung-pao-chicken"
        assert body["react_steps"]
        assert body["tool_calls"]
        assert body["observations"]
        assert body["memory_records"]
        assert body["final_decision"]["status"] in [
            "qualified",
            "unqualified",
            "manual_review",
        ]
        assert body["data_asset_record"]["asset_type"] == "vision-qa-quality-event"
