from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, JSON, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProductionEvent(Base):
    __tablename__ = "production_events"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    store_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    store_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True, default="")
    dish_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    operator_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    operator_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True, default="")
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    lighting_profile: Mapped[str] = mapped_column(String(120), nullable=False)
    camera_profile: Mapped[str] = mapped_column(String(120), nullable=False)
    temperature_celsius: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_grams: Mapped[float | None] = mapped_column(Float, nullable=True)
    standard_dish_key: Mapped[str] = mapped_column(String(64), nullable=False)
    model_version: Mapped[str] = mapped_column(String(120), nullable=False)
    top_label: Mapped[str] = mapped_column(String(120), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    plating_score: Mapped[float] = mapped_column(Float, nullable=False)
    color_score: Mapped[float] = mapped_column(Float, nullable=False)
    deviation_score: Mapped[float] = mapped_column(Float, nullable=False)
    pass_decision: Mapped[bool] = mapped_column(Boolean, nullable=False)
    feedback: Mapped[dict[str, str | bool | None]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
