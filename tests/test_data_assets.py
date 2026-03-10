import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "data-assets.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_create_list_and_build_data_assets(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        client.post(
            "/api/v1/operations/snapshots",
            json={
                "store_code": "SH-001",
                "shift": "dinner",
                "operator_count": 4,
                "quality_alert_count": 0,
                "sop_risk_items": [],
                "temperature_status": "stable",
                "throughput_score": 0.92,
            },
        )

        summary_response = client.get("/api/v1/data-assets/build-summary")
        assert summary_response.status_code == 200
        summary = summary_response.json()
        assert summary["operation_snapshot_count"] == 1
        assert summary["recommended_asset_type"] == "restaurant-knowledge-pack"

        create_response = client.post(
            "/api/v1/data-assets",
            json={
                "asset_type": "restaurant-knowledge-pack",
                "source_domains": ["production", "operations"],
                "quality_summary": "No production events available yet.",
                "ops_summary": "1 operation snapshots available for SOP analysis.",
                "knowledge_refs": ["ops/snapshot/SH-001"],
                "training_value_score": 0.15,
                "api_export_ready": False
            },
        )
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["asset_type"] == "restaurant-knowledge-pack"

        list_response = client.get("/api/v1/data-assets")
        assert list_response.status_code == 200
        listed = list_response.json()
        assert len(listed) == 1
