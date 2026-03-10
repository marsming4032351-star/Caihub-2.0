from app.repositories.data_asset import DataAssetRepository
from app.repositories.operations import StoreOperationSnapshotRepository
from app.repositories.production_event import ProductionEventRepository
from app.schemas.data_asset import DataAssetBuildSummary, DataAssetCreate, DataAssetRead


class DataAssetService:
    def __init__(
        self,
        repository: DataAssetRepository,
        production_repository: ProductionEventRepository,
        operations_repository: StoreOperationSnapshotRepository,
    ) -> None:
        self.repository = repository
        self.production_repository = production_repository
        self.operations_repository = operations_repository

    def list_assets(self) -> list[DataAssetRead]:
        return [
            DataAssetRead.model_validate(asset)
            for asset in self.repository.list_all()
        ]

    def create_asset(self, payload: DataAssetCreate) -> DataAssetRead:
        asset = self.repository.create(payload)
        return DataAssetRead.model_validate(asset)

    def build_summary(self) -> DataAssetBuildSummary:
        production_events = self.production_repository.list_all()
        operation_snapshots = self.operations_repository.list_all()

        passed_count = sum(1 for event in production_events if event.pass_decision)
        total_events = len(production_events)
        quality_summary = (
            f"{passed_count}/{total_events} production events passed quality checks."
            if total_events > 0
            else "No production events available yet."
        )
        ops_summary = (
            f"{len(operation_snapshots)} operation snapshots available for SOP analysis."
            if operation_snapshots
            else "No operation snapshots available yet."
        )
        score = min(1.0, (total_events * 0.1) + (len(operation_snapshots) * 0.15))

        return DataAssetBuildSummary(
            production_event_count=total_events,
            operation_snapshot_count=len(operation_snapshots),
            recommended_asset_type="restaurant-knowledge-pack",
            generated_quality_summary=quality_summary,
            generated_ops_summary=ops_summary,
            suggested_training_value_score=round(score, 2),
        )
