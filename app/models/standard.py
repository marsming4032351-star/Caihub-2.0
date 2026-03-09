from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DishStandard(Base):
    __tablename__ = "dish_standards"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    dish_key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_weight_grams: Mapped[float] = mapped_column(Float, nullable=False)
    weight_tolerance_grams: Mapped[float] = mapped_column(Float, nullable=False)
    target_temperature_celsius: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_tolerance_celsius: Mapped[float] = mapped_column(Float, nullable=False)
    minimum_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    maximum_deviation_score: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
