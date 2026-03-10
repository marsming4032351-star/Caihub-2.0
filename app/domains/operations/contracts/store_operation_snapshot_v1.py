from datetime import datetime

from pydantic import BaseModel, Field


class StoreOperationSnapshotContractV1(BaseModel):
    snapshot_id: str
    store_code: str
    snapshot_time: datetime
    shift: str = Field(min_length=1, max_length=64)
    operator_count: int = Field(ge=0)
    quality_alert_count: int = Field(ge=0)
    sop_risk_items: list[str] = Field(default_factory=list)
    temperature_status: str = Field(min_length=1, max_length=32)
    throughput_score: float = Field(ge=0.0, le=1.0)
    notes: str | None = None
