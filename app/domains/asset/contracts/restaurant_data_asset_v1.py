from datetime import datetime

from pydantic import BaseModel, Field


class RestaurantDataAssetContractV1(BaseModel):
    asset_id: str
    generated_at: datetime
    asset_type: str = Field(min_length=1, max_length=64)
    source_domains: list[str] = Field(default_factory=list)
    quality_summary: str
    ops_summary: str
    marketing_summary: str | None = None
    knowledge_refs: list[str] = Field(default_factory=list)
    training_value_score: float = Field(ge=0.0, le=1.0)
    api_export_ready: bool = False
