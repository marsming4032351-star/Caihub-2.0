from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_store_service
from app.schemas.store import StoreCreate, StoreRead
from app.services.stores import StoreService

router = APIRouter()


@router.get("", response_model=list[StoreRead], summary="List stores")
def list_stores(
    service: StoreService = Depends(get_store_service),
) -> list[StoreRead]:
    return service.list_stores()


@router.post(
    "",
    response_model=StoreRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a store",
)
def create_store(
    payload: StoreCreate,
    service: StoreService = Depends(get_store_service),
) -> StoreRead:
    return service.create_store(payload)
