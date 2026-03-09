from app.events.base import DomainEvent


def dish_created_event(dish_id: str, name: str) -> DomainEvent:
    return DomainEvent(
        event_type="catalog.dish.created",
        domain="catalog",
        producer="catalog-service",
        payload={"dish_id": dish_id, "name": name},
    )
