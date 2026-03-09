from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class DishCatalogContractV1(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    is_available: bool = True
