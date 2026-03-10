from app.repositories.operations import StoreOperationSnapshotRepository
from app.schemas.operations import (
    StoreOperationSnapshotCreate,
    StoreOperationSnapshotRead,
)


class OperationsService:
    def __init__(self, repository: StoreOperationSnapshotRepository) -> None:
        self.repository = repository

    def list_snapshots(self) -> list[StoreOperationSnapshotRead]:
        return [
            StoreOperationSnapshotRead.model_validate(snapshot)
            for snapshot in self.repository.list_all()
        ]

    def create_snapshot(
        self,
        payload: StoreOperationSnapshotCreate,
    ) -> StoreOperationSnapshotRead:
        snapshot = self.repository.create(payload)
        return StoreOperationSnapshotRead.model_validate(snapshot)
