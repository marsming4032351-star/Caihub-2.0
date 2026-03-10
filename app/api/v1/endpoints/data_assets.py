from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_data_asset_service
from app.schemas.data_asset import (
    DataAssetBuildSummary,
    DataAssetCreate,
    DataAssetMaterializationPreview,
    DataAssetMaterializationRequest,
    DataAssetRead,
)
from app.services.data_assets import DataAssetService

router = APIRouter()


@router.get("", response_model=list[DataAssetRead], summary="List data assets")
def list_data_assets(
    service: DataAssetService = Depends(get_data_asset_service),
) -> list[DataAssetRead]:
    return service.list_assets()


@router.post(
    "",
    response_model=DataAssetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a data asset",
)
def create_data_asset(
    payload: DataAssetCreate,
    service: DataAssetService = Depends(get_data_asset_service),
) -> DataAssetRead:
    return service.create_asset(payload)


@router.get(
    "/build-summary",
    response_model=DataAssetBuildSummary,
    summary="Build data asset summary from current production and operations data",
)
def build_data_asset_summary(
    service: DataAssetService = Depends(get_data_asset_service),
) -> DataAssetBuildSummary:
    return service.build_summary()


@router.post(
    "/materialize-preview",
    response_model=DataAssetMaterializationPreview,
    summary="Preview a materialized data asset payload",
)
def preview_data_asset_materialization(
    payload: DataAssetMaterializationRequest,
    service: DataAssetService = Depends(get_data_asset_service),
) -> DataAssetMaterializationPreview:
    return service.build_materialization_preview(payload)


@router.post(
    "/materialize",
    response_model=DataAssetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Materialize a data asset from current production and operations signals",
)
def materialize_data_asset(
    payload: DataAssetMaterializationRequest,
    response: Response,
    service: DataAssetService = Depends(get_data_asset_service),
) -> DataAssetRead:
    created, event = service.materialize_asset(payload)
    response.headers["X-CaiHub-Asset-Event"] = event.event_type
    return created
