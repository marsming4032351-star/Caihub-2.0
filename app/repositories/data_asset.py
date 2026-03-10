from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_asset import DataAsset
from app.schemas.data_asset import DataAssetCreate


class DataAssetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[DataAsset]:
        result = self.session.execute(
            select(DataAsset).order_by(DataAsset.created_at.desc())
        )
        return result.scalars().all()

    def create(self, payload: DataAssetCreate) -> DataAsset:
        asset = DataAsset(**payload.model_dump())
        self.session.add(asset)
        self.session.commit()
        self.session.refresh(asset)
        return asset
