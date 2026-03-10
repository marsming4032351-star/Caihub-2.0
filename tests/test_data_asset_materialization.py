import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "data-asset-materialization.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_preview_and_materialize_data_asset(tmp_path: Path) -> None:
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

        preview_response = client.post(
            "/api/v1/data-assets/materialize-preview",
            json={
                "knowledge_refs": ["ops/snapshot/SH-001"],
                "api_export_ready": True
            },
        )
        assert preview_response.status_code == 200
        preview = preview_response.json()
        assert preview["asset_payload"]["asset_type"] == "restaurant-knowledge-pack"
        assert preview["asset_payload"]["api_export_ready"] is True
        assert len(preview["rationale"]) >= 2

        materialize_response = client.post(
            "/api/v1/data-assets/materialize",
            json={
                "knowledge_refs": ["ops/snapshot/SH-001"],
                "api_export_ready": True
            },
        )
        assert materialize_response.status_code == 201
        materialized = materialize_response.json()
        assert materialized["asset_type"] == "restaurant-knowledge-pack"
        assert materialized["api_export_ready"] is True

        list_response = client.get("/api/v1/data-assets")
        assert list_response.status_code == 200
        listed = list_response.json()
        assert len(listed) == 1
