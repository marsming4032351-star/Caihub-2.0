from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DataAssetCreate(BaseModel):
    asset_type: str = Field(min_length=1, max_length=64)
    source_domains: list[str] = Field(default_factory=list)
    quality_summary: str = Field(min_length=1, max_length=4000)
    ops_summary: str = Field(min_length=1, max_length=4000)
    marketing_summary: str | None = Field(default=None, max_length=4000)
    knowledge_refs: list[str] = Field(default_factory=list)
    training_value_score: float = Field(ge=0.0, le=1.0)
    api_export_ready: bool = False


class DataAssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    asset_type: str
    source_domains: list[str]
    quality_summary: str
    ops_summary: str
    marketing_summary: str | None
    knowledge_refs: list[str]
    training_value_score: float
    api_export_ready: bool
    created_at: datetime
    updated_at: datetime


class DataAssetBuildSummary(BaseModel):
    production_event_count: int
    operation_snapshot_count: int
    recommended_asset_type: str
    generated_quality_summary: str
    generated_ops_summary: str
    suggested_training_value_score: float
