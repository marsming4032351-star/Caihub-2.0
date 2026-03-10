from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_data_asset_service
from app.schemas.data_asset import DataAssetBuildSummary, DataAssetCreate, DataAssetRead
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
