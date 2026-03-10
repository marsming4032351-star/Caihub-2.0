from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store import Store
from app.schemas.store import StoreCreate


class StoreRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Store]:
        result = self.session.execute(select(Store).order_by(Store.created_at.desc()))
        return result.scalars().all()

    def create(self, payload: StoreCreate) -> Store:
        store = Store(**payload.model_dump())
        self.session.add(store)
        self.session.commit()
        self.session.refresh(store)
        return store
