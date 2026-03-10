from app.schemas.production import ProductionEventCreate


def test_production_event_create_normalizes_org_refs() -> None:
    payload = ProductionEventCreate(
        store_code="store-sh-001",
        dish_id="dish-kungpao-001",
        operator_code="chef-ming",
        capture={
            "image_url": "https://example.com/kungpao.jpg",
            "lighting_profile": "5600K-standard",
            "camera_profile": "caibox-v1",
            "temperature_celsius": 66.0,
            "weight_grams": 345.0,
        },
        recognition={
            "model_version": "vlm-vision-v1",
            "top_label": "kung-pao-chicken",
            "confidence": 0.92,
        },
    )

    assert payload.store_id == "store-sh-001"
    assert payload.store_code == "store-sh-001"
    assert payload.operator_id == "chef-ming"
    assert payload.operator_code == "chef-ming"
