import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "operations.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_create_and_list_operation_snapshots(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        create_response = client.post(
            "/api/v1/operations/snapshots",
            json={
                "store_code": "SH-001",
                "shift": "lunch",
                "operator_count": 5,
                "quality_alert_count": 1,
                "sop_risk_items": ["plating-delay"],
                "temperature_status": "stable",
                "throughput_score": 0.86,
                "notes": "Lunch rush stable.",
            },
        )

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["store_code"] == "SH-001"
        assert created["throughput_score"] == 0.86

        list_response = client.get("/api/v1/operations/snapshots")
        assert list_response.status_code == 200
        listed = list_response.json()
        assert len(listed) == 1
        assert listed[0]["shift"] == "lunch"
