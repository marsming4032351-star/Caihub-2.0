from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_dish_standard_service
from app.schemas.standard import DishStandardCreate, DishStandardRead
from app.services.standards import DishStandardService

router = APIRouter()


@router.get("", response_model=list[DishStandardRead], summary="查询菜品标准")
def list_standards(
    service: DishStandardService = Depends(get_dish_standard_service),
) -> list[DishStandardRead]:
    return service.list_standards()


@router.post(
    "",
    response_model=DishStandardRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建菜品标准",
)
def create_standard(
    payload: DishStandardCreate,
    service: DishStandardService = Depends(get_dish_standard_service),
) -> DishStandardRead:
    return service.create_standard(payload)
