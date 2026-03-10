from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operation_snapshot import StoreOperationSnapshot
from app.schemas.operations import StoreOperationSnapshotCreate


class StoreOperationSnapshotRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[StoreOperationSnapshot]:
        result = self.session.execute(
            select(StoreOperationSnapshot).order_by(
                StoreOperationSnapshot.created_at.desc()
            )
        )
        return result.scalars().all()

    def create(
        self,
        payload: StoreOperationSnapshotCreate,
    ) -> StoreOperationSnapshot:
        snapshot = StoreOperationSnapshot(**payload.model_dump())
        self.session.add(snapshot)
        self.session.commit()
        self.session.refresh(snapshot)
        return snapshot
