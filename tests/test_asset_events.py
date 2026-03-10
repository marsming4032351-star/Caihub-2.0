from app.events.asset import data_asset_materialized_event


def test_data_asset_materialized_event() -> None:
    event = data_asset_materialized_event(
        asset_id="asset-1",
        asset_type="restaurant-knowledge-pack",
        training_value_score=0.45,
    )

    assert event.event_type == "asset.data_asset.materialized"
    assert event.domain == "asset"
    assert event.payload["asset_id"] == "asset-1"
    assert event.payload["asset_type"] == "restaurant-knowledge-pack"
