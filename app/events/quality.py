from app.events.base import DomainEvent


def quality_decision_event(
    event_id: str,
    dish_id: str,
    passed: bool,
) -> DomainEvent:
    return DomainEvent(
        event_type="production.quality.decided",
        domain="production",
        producer="quality-service",
        payload={
            "event_id": event_id,
            "dish_id": dish_id,
            "passed": passed,
        },
    )
