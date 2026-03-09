from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductionCaptureInput(BaseModel):
    image_url: str = Field(min_length=1)
    lighting_profile: str = Field(min_length=1, max_length=120)
    camera_profile: str = Field(min_length=1, max_length=120)
    temperature_celsius: float | None = None
    weight_grams: float | None = Field(default=None, ge=0)


class ProductionRecognitionInput(BaseModel):
    model_version: str = Field(min_length=1, max_length=120)
    top_label: str = Field(min_length=1, max_length=120)
    confidence: float = Field(ge=0.0, le=1.0)


class ProductionFeedback(BaseModel):
    corrected: bool | None = None
    corrected_label: str | None = None
    reason: str | None = None


class ProductionEventCreate(BaseModel):
    store_id: str = Field(min_length=1, max_length=64)
    dish_id: str = Field(min_length=1, max_length=64)
    operator_id: str = Field(min_length=1, max_length=64)
    capture: ProductionCaptureInput
    recognition: ProductionRecognitionInput
    feedback: ProductionFeedback = Field(default_factory=ProductionFeedback)


class ProductionQualityResult(BaseModel):
    standard_dish_key: str
    model_version: str
    top_label: str
    confidence: float = Field(ge=0.0, le=1.0)
    plating_score: float = Field(ge=0.0, le=1.0)
    color_score: float = Field(ge=0.0, le=1.0)
    deviation_score: float = Field(ge=0.0, le=1.0)
    pass_decision: bool


class ProductionEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    store_id: str
    dish_id: str
    operator_id: str
    capture: ProductionCaptureInput
    quality_result: ProductionQualityResult
    feedback: ProductionFeedback
    created_at: datetime
