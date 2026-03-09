from datetime import datetime

from pydantic import BaseModel, Field


class CaptureProfileV1(BaseModel):
    image_url: str
    lighting_profile: str
    camera_profile: str
    temperature_celsius: float | None = None
    weight_grams: float | None = Field(default=None, ge=0)


class QualityResultV1(BaseModel):
    model_version: str
    top_label: str
    confidence: float = Field(ge=0.0, le=1.0)
    plating_score: float | None = Field(default=None, ge=0.0, le=1.0)
    color_score: float | None = Field(default=None, ge=0.0, le=1.0)
    deviation_score: float | None = Field(default=None, ge=0.0, le=1.0)
    pass_decision: bool | None = None


class DishProductionEventContractV1(BaseModel):
    event_id: str
    timestamp: datetime
    store_id: str
    dish_id: str
    operator_id: str
    capture: CaptureProfileV1
    quality_result: QualityResultV1
    feedback: dict[str, str | bool | None] = Field(default_factory=dict)
