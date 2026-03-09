from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_dish_service
from app.schemas.dish import DishCreate, DishRead
from app.services.dishes import DishService

router = APIRouter()


@router.get("", response_model=list[DishRead], summary="List dishes")
def list_dishes(
    service: DishService = Depends(get_dish_service),
) -> list[DishRead]:
    return service.list_dishes()


@router.post(
    "",
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a dish",
)
def create_dish(
    payload: DishCreate,
    service: DishService = Depends(get_dish_service),
) -> DishRead:
    return service.create_dish(payload)
