from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import get_architecture_service, get_system_service
from app.schemas.architecture import ArchitectureBlueprintResponse
from app.schemas.system import SystemInfoResponse
from app.services.architecture import ArchitectureService
from app.services.system import SystemService

router = APIRouter()


@router.get("/info", response_model=SystemInfoResponse, summary="System metadata")
async def system_info(
    service: SystemService = Depends(get_system_service),
) -> SystemInfoResponse:
    return service.get_info()


@router.get(
    "/architecture",
    response_model=ArchitectureBlueprintResponse,
    summary="平台架构蓝图",
)
async def system_architecture(
    service: ArchitectureService = Depends(get_architecture_service),
) -> ArchitectureBlueprintResponse:
    return service.get_blueprint()
