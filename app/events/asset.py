from app.events.base import DomainEvent


def data_asset_materialized_event(
    asset_id: str,
    asset_type: str,
    training_value_score: float,
) -> DomainEvent:
    return DomainEvent(
        event_type="asset.data_asset.materialized",
        domain="asset",
        producer="data-asset-service",
        payload={
            "asset_id": asset_id,
            "asset_type": asset_type,
            "training_value_score": training_value_score,
        },
    )
