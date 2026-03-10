from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_operations_service
from app.schemas.operations import (
    StoreOperationSnapshotCreate,
    StoreOperationSnapshotRead,
)
from app.services.operations import OperationsService

router = APIRouter()


@router.get(
    "/snapshots",
    response_model=list[StoreOperationSnapshotRead],
    summary="List store operation snapshots",
)
def list_operation_snapshots(
    service: OperationsService = Depends(get_operations_service),
) -> list[StoreOperationSnapshotRead]:
    return service.list_snapshots()


@router.post(
    "/snapshots",
    response_model=StoreOperationSnapshotRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a store operation snapshot",
)
def create_operation_snapshot(
    payload: StoreOperationSnapshotCreate,
    service: OperationsService = Depends(get_operations_service),
) -> StoreOperationSnapshotRead:
    return service.create_snapshot(payload)
