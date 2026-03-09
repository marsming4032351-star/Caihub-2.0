import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.schemas.vision import DishRecognitionResponse, VisionCandidate, VisionFeatures
from app.vision.recognizer import get_dish_recognizer


def create_test_client(tmp_path: Path) -> TestClient:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory
    from app.main import create_application

    tmp_path.mkdir(parents=True, exist_ok=True)
    database_path = tmp_path / "vision.db"
    os.environ["CAIHUB_DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["CAIHUB_AUTO_CREATE_TABLES"] = "true"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    return TestClient(create_application())


class FakeDishRecognizer:
    def recognize(self, image_base64: str) -> DishRecognitionResponse:
        assert image_base64 == "ZmFrZS1pbWFnZS1ieXRlcw=="
        return DishRecognitionResponse(
            label="pizza",
            confidence=0.91,
            candidates=[
                VisionCandidate(label="pizza", confidence=0.91),
                VisionCandidate(label="soup", confidence=0.44),
                VisionCandidate(label="steak", confidence=0.32),
            ],
            features=VisionFeatures(
                brightness=0.62,
                edge_density=0.28,
                circularity=0.81,
                green_ratio=0.07,
                warm_ratio=0.69,
            ),
        )


def test_dish_recognition_endpoint(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        app = client.app
        app.dependency_overrides[get_dish_recognizer] = FakeDishRecognizer

        response = client.post(
            "/api/v1/vision/dish-recognition",
            json={"image_base64": "ZmFrZS1pbWFnZS1ieXRlcw=="},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["label"] == "pizza"
        assert body["candidates"][0]["label"] == "pizza"
        assert body["features"]["warm_ratio"] == 0.69

        app.dependency_overrides.clear()
