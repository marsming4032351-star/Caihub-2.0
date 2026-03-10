from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import (
    get_agent_runtime_service,
    get_architecture_service,
    get_orchestration_service,
    get_system_service,
)
from app.schemas.agent_runtime import AgentRuntimeOverview
from app.schemas.agent_task import OrchestrationPlan
from app.schemas.architecture import ArchitectureBlueprintResponse
from app.schemas.system import SystemInfoResponse
from app.agents.runtime import AgentRuntimeService
from app.services.architecture import ArchitectureService
from app.services.orchestration import OrchestrationService
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


@router.get(
    "/agent-runtime",
    response_model=AgentRuntimeOverview,
    summary="Agent runtime 概览",
)
async def system_agent_runtime(
    service: AgentRuntimeService = Depends(get_agent_runtime_service),
) -> AgentRuntimeOverview:
    return service.get_overview()


@router.get(
    "/orchestration-plan",
    response_model=OrchestrationPlan,
    summary="CEO Agent orchestration skeleton",
)
async def system_orchestration_plan(
    service: OrchestrationService = Depends(get_orchestration_service),
) -> OrchestrationPlan:
    return service.build_foundation_plan()
