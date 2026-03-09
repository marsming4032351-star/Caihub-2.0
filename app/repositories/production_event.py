from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.production_event import ProductionEvent


class ProductionEventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[ProductionEvent]:
        result = self.session.execute(
            select(ProductionEvent).order_by(ProductionEvent.created_at.desc())
        )
        return result.scalars().all()

    def create(self, event: ProductionEvent) -> ProductionEvent:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event
