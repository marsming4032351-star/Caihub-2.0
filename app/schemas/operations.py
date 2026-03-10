from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StoreOperationSnapshotCreate(BaseModel):
    store_code: str = Field(min_length=1, max_length=64)
    shift: str = Field(min_length=1, max_length=64)
    operator_count: int = Field(ge=0)
    quality_alert_count: int = Field(default=0, ge=0)
    sop_risk_items: list[str] = Field(default_factory=list)
    temperature_status: str = Field(min_length=1, max_length=32)
    throughput_score: float = Field(ge=0.0, le=1.0)
    notes: str | None = Field(default=None, max_length=2000)


class StoreOperationSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    store_code: str
    shift: str
    operator_count: int
    quality_alert_count: int
    sop_risk_items: list[str]
    temperature_status: str
    throughput_score: float
    notes: str | None
    created_at: datetime
    updated_at: datetime
