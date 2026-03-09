from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DishStandardBase(BaseModel):
    dish_key: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    target_weight_grams: float = Field(gt=0)
    weight_tolerance_grams: float = Field(ge=0)
    target_temperature_celsius: float = Field(gt=0)
    temperature_tolerance_celsius: float = Field(ge=0)
    minimum_confidence: float = Field(ge=0.0, le=1.0)
    maximum_deviation_score: float = Field(ge=0.0, le=1.0)
    is_active: bool = True


class DishStandardCreate(DishStandardBase):
    pass


class DishStandardRead(DishStandardBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
