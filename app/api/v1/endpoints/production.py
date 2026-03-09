from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_production_event_service
from app.schemas.production import ProductionEventCreate, ProductionEventRead
from app.services.production import ProductionEventService

router = APIRouter()


@router.get("/events", response_model=list[ProductionEventRead], summary="查询出品事件")
def list_production_events(
    service: ProductionEventService = Depends(get_production_event_service),
) -> list[ProductionEventRead]:
    return service.list_events()


@router.post(
    "/events",
    response_model=ProductionEventRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建出品事件并完成质检裁决",
)
def create_production_event(
    payload: ProductionEventCreate,
    response: Response,
    service: ProductionEventService = Depends(get_production_event_service),
) -> ProductionEventRead:
    created, decision_event = service.create_event(payload)
    response.headers["X-CaiHub-Quality-Event"] = decision_event.event_type
    return created
