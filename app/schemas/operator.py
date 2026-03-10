from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OperatorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    employee_code: str = Field(min_length=1, max_length=64)
    role: str = Field(default="staff", min_length=1, max_length=64)
    store_code: str | None = Field(default=None, max_length=64)
    status: str = Field(default="active", min_length=1, max_length=32)
    notes: str | None = Field(default=None, max_length=2000)


class OperatorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    employee_code: str
    role: str
    store_code: str | None
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
