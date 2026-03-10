import os
from pathlib import Path

from fastapi.testclient import TestClient


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "org-entities.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


def test_create_and_list_stores_and_operators(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        store_response = client.post(
            "/api/v1/stores",
            json={
                "name": "Shanghai Flagship Store",
                "code": "SH-001",
                "city": "Shanghai",
                "status": "active",
                "manager_name": "Ava",
            },
        )
        assert store_response.status_code == 201
        store = store_response.json()
        assert store["code"] == "SH-001"

        operator_response = client.post(
            "/api/v1/operators",
            json={
                "name": "Li Wei",
                "employee_code": "OP-1001",
                "role": "kitchen-lead",
                "store_code": "SH-001",
                "status": "active",
            },
        )
        assert operator_response.status_code == 201
        operator = operator_response.json()
        assert operator["employee_code"] == "OP-1001"
        assert operator["store_code"] == "SH-001"

        stores_response = client.get("/api/v1/stores")
        operators_response = client.get("/api/v1/operators")

        assert stores_response.status_code == 200
        assert operators_response.status_code == 200
        assert len(stores_response.json()) == 1
        assert len(operators_response.json()) == 1
