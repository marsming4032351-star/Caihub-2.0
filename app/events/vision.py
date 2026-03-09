from app.events.base import DomainEvent


def recognition_completed_event(label: str, confidence: float) -> DomainEvent:
    return DomainEvent(
        event_type="vision.recognition.completed",
        domain="vision",
        producer="vision-service",
        payload={"label": label, "confidence": confidence},
    )
