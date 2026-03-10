from app.repositories.data_asset import DataAssetRepository
from app.repositories.operations import StoreOperationSnapshotRepository
from app.repositories.production_event import ProductionEventRepository
from app.schemas.data_asset import (
    DataAssetBuildSummary,
    DataAssetCreate,
    DataAssetMaterializationPreview,
    DataAssetMaterializationRequest,
    DataAssetRead,
)


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

    def build_materialization_preview(
        self,
        request: DataAssetMaterializationRequest,
    ) -> DataAssetMaterializationPreview:
        summary = self.build_summary()
        payload = DataAssetCreate(
            asset_type=request.asset_type or summary.recommended_asset_type,
            source_domains=["production", "operations"],
            quality_summary=summary.generated_quality_summary,
            ops_summary=summary.generated_ops_summary,
            marketing_summary=request.marketing_summary,
            knowledge_refs=request.knowledge_refs,
            training_value_score=summary.suggested_training_value_score,
            api_export_ready=request.api_export_ready,
        )
        rationale = [
            f"Included {summary.production_event_count} production events.",
            f"Included {summary.operation_snapshot_count} operation snapshots.",
            f"Recommended asset type: {payload.asset_type}.",
        ]
        return DataAssetMaterializationPreview(
            asset_payload=payload,
            rationale=rationale,
        )

    def materialize_asset(
        self,
        request: DataAssetMaterializationRequest,
    ) -> DataAssetRead:
        preview = self.build_materialization_preview(request)
        asset = self.repository.create(preview.asset_payload)
        return DataAssetRead.model_validate(asset)
