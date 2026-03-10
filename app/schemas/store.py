from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StoreCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    code: str = Field(min_length=1, max_length=64)
    city: str | None = Field(default=None, max_length=64)
    status: str = Field(default="active", min_length=1, max_length=32)
    manager_name: str | None = Field(default=None, max_length=64)
    notes: str | None = Field(default=None, max_length=2000)


class StoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    code: str
    city: str | None
    status: str
    manager_name: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
