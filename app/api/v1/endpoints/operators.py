from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_operator_service
from app.schemas.operator import OperatorCreate, OperatorRead
from app.services.operators import OperatorService

router = APIRouter()


@router.get("", response_model=list[OperatorRead], summary="List operators")
def list_operators(
    service: OperatorService = Depends(get_operator_service),
) -> list[OperatorRead]:
    return service.list_operators()


@router.post(
    "",
    response_model=OperatorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an operator",
)
def create_operator(
    payload: OperatorCreate,
    service: OperatorService = Depends(get_operator_service),
) -> OperatorRead:
    return service.create_operator(payload)
